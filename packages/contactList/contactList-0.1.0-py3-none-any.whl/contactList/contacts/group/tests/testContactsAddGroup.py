#
# Copyright 2018 Russell Smiley
#
# This file is part of contactList.
#
# contactList is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# contactList is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with contactList.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Test contacts group add operation.
"""

import unittest.mock

from ..operation import \
    ContactData, \
    add


class TestContactsAddGroup( unittest.TestCase ) :
    """
    Test contacts group add operation creating groups.
    """


    def setUp( self ) :
        self.contacts = ContactData()


    def testSingleGroupEmptyClusters( self ) :
        """
        Adding a group that doesn't exist adds the group, and if there are no clusters there is no change to the
        clusters.
        """
        self.assertEqual( 0, len( self.contacts.groups ) )
        self.assertEqual( 0, len( self.contacts.clusters ) )

        groupsToAdd = [ 'someName' ]

        add( self.contacts, groupsToAdd )

        self.assertEqual( 1, len( self.contacts.groups ) )
        self.assertIn( groupsToAdd[ 0 ], self.contacts.groups )

        self.assertEqual( 0, len( self.contacts.clusters ) )


    def testNoGroupsExistingGroupNoChange( self ) :
        """
        Adding an existing group makes no change to the group.
        """
        self.assertEqual( 0, len( self.contacts.groups ) )
        self.assertEqual( 0, len( self.contacts.clusters ) )

        groupsToAdd = [ 'someName' ]
        expectedGroupContents = [ 'a@b', 'c@d' ]

        self.contacts.groups[ groupsToAdd[ 0 ] ] = expectedGroupContents
        self.assertEqual( 1, len( self.contacts.groups ) )

        add( self.contacts, groupsToAdd )

        self.assertEqual( 1, len( self.contacts.groups ) )
        self.assertIn( groupsToAdd[ 0 ], self.contacts.groups )
        self.assertEqual( expectedGroupContents, self.contacts.groups[ groupsToAdd[ 0 ] ] )
        self.assertEqual( 0, len( self.contacts.clusters ) )


class TestContactsGroupAddClusters( unittest.TestCase ) :
    """
    Test contacts group add operation adding to clusters.
    """


    def setUp( self ) :
        self.contacts = ContactData()
        self.contacts.groups = {
            'g1' : [ 'a@b', 'c@d' ],
            'g2' : [ 'e@f', 'a@b' ],
            'g3' : [ 'a@b', 'c@d', 'e@f' ],
        }
        self.contacts.clusters = {
            'c1' : [ 'g3' ],
            'c2' : [ 'g2' ],
        }


    def testSingleClusterSpecified( self ) :
        """
        Specifying a cluster that exists to add the group to adds only to that group.
        """
        self.assertEqual( 1, len( self.contacts.clusters[ 'c1' ] ) )
        self.assertEqual( 1, len( self.contacts.clusters[ 'c2' ] ) )

        groupsToAdd = [ 'g1' ]
        clustersToAdd = [ 'c2' ]

        add( self.contacts, groupsToAdd,
                                     clusters = clustersToAdd )

        self.assertEqual( 1, len( self.contacts.clusters[ 'c1' ] ) )
        self.assertEqual( 2, len( self.contacts.clusters[ 'c2' ] ) )
        self.assertEqual( [ 'g2', 'g1' ], self.contacts.clusters[ 'c2' ] )


    def testExistingClusterNoChange( self ) :
        """
        Specifying a cluster that already contains the group doesn't change the cluster.
        """
        self.assertEqual( 1, len( self.contacts.clusters[ 'c1' ] ) )
        self.assertEqual( 1, len( self.contacts.clusters[ 'c2' ] ) )

        groupsToAdd = [ 'g2' ]
        clustersToAdd = [ 'c2' ]

        add( self.contacts, groupsToAdd,
                                     clusters = clustersToAdd )

        self.assertEqual( 1, len( self.contacts.clusters[ 'c1' ] ) )
        self.assertEqual( 1, len( self.contacts.clusters[ 'c2' ] ) )
        self.assertEqual( [ 'g2' ], self.contacts.clusters[ 'c2' ] )


    def testMultipleClustersSpecified( self ) :
        """
        Specifying multiple clusters adds the group to all specified clusters.
        """
        self.contacts.clusters[ 'c3' ] = list()

        groupsToAdd = [ 'g1' ]
        clustersToAdd = [ 'c3', 'c2' ]

        add( self.contacts, groupsToAdd,
                                     clusters = clustersToAdd )

        self.assertEqual( 1, len( self.contacts.clusters[ 'c1' ] ) )
        self.assertEqual( [ 'g3' ], self.contacts.clusters[ 'c1' ] )

        self.assertEqual( 2, len( self.contacts.clusters[ 'c2' ] ) )
        self.assertEqual( [ 'g2', 'g1' ], self.contacts.clusters[ 'c2' ] )

        self.assertEqual( 1, len( self.contacts.clusters[ 'c3' ] ) )
        self.assertEqual( [ 'g1' ], self.contacts.clusters[ 'c3' ] )


    def testAllClustersSpecified( self ) :
        """
        Specifying ``None`` clusters (default) adds group to all clusters.
        """
        self.assertEqual( 1, len( self.contacts.clusters[ 'c1' ] ) )
        self.assertEqual( 1, len( self.contacts.clusters[ 'c2' ] ) )

        groupsToAdd = [ 'g1' ]

        add( self.contacts, groupsToAdd )

        self.assertEqual( 2, len( self.contacts.clusters[ 'c1' ] ) )
        self.assertEqual( [ 'g3', 'g1' ], self.contacts.clusters[ 'c1' ] )
        self.assertEqual( 2, len( self.contacts.clusters[ 'c2' ] ) )
        self.assertEqual( [ 'g2', 'g1' ], self.contacts.clusters[ 'c2' ] )


if __name__ == '__main__' :
    unittest.main()
