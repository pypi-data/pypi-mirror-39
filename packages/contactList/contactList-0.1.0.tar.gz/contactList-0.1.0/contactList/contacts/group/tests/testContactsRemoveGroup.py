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
Test contacts group remove operation.
"""

import unittest.mock

from ..operation import \
    ContactData, \
    ContactsOperationError, \
    remove


class TestContactsRemoveGroup( unittest.TestCase ) :
    """
    Test basic contacts group remove operation.
    """


    def setUp( self ) :
        self.contacts = ContactData()
        self.contacts.groups = {
            'g1' : [ 'a@b', 'c@d' ],
            'g2' : [ 'e@f', 'g@h' ],
            'g3' : [ 'i@j', 'k@l' ],
        }


    def testSingleGroup( self ) :
        """
        Removing a single group removes the group and leaves other groups untouched.
        """
        groupsToRemove = [ 'g1' ]

        self.assertEqual( 0, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        contactsResult = remove( self.contacts, groupsToRemove )

        self.assertEqual( 0, len( contactsResult.clusters ) )
        self.assertEqual( 2, len( contactsResult.groups ) )

        self.assertEqual( { 'g2', 'g3' }, contactsResult.groups.keys() )

        self.assertEqual( [ 'e@f', 'g@h' ], contactsResult.groups[ 'g2' ] )
        self.assertEqual( [ 'i@j', 'k@l' ], contactsResult.groups[ 'g3' ] )


    def testMultipleGroups( self ) :
        """
        Specifying an array of group names removes each group.
        """
        groupsToRemove = [ 'g1', 'g3' ]

        self.assertEqual( 0, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        contactsResult = remove( self.contacts, groupsToRemove )

        self.assertEqual( 0, len( contactsResult.clusters ) )
        self.assertEqual( 1, len( contactsResult.groups ) )

        self.assertIn( 'g2', contactsResult.groups )

        self.assertEqual( [ 'e@f', 'g@h' ], contactsResult.groups[ 'g2' ] )


    def testGroupsClusterMembersRaises( self ) :
        """
        Exception raised if the group being removed is still a member of any clusters.
        """
        groupsToRemove = [ 'g1', 'g3' ]

        # Create a cluster with an existing group as a member.
        self.contacts.clusters = {
            'c1' : [ 'g3' ],
        }

        self.assertEqual( 1, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        with self.assertRaisesRegex( ContactsOperationError, '^Remove group\(s\) from clusters before removing the '
                                                             'group\(s\)' ) :
            remove( self.contacts, groupsToRemove )


    def testModifyClusters( self ) :
        """
        Specifying an array of clusters with an array of groups removes each group from each cluster,
        silently ignoring missing groups.
        """
        groupsToModify = [ 'g1', 'g3' ]
        clustersToModify = [ 'c1' ]

        self.contacts.clusters = {
            'c1' : [ 'g1', 'g2', 'g3' ],
            'c2' : [ 'g2' ],
        }

        self.assertEqual( 2, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        contactsResult = remove( self.contacts, groupsToModify,
                                 clusters = clustersToModify )

        self.assertNotIn( 'g1', contactsResult.clusters[ 'c1' ] )
        self.assertNotIn( 'g3', contactsResult.clusters[ 'c1' ] )
        self.assertIn( 'g2', contactsResult.clusters[ 'c1' ] )
        self.assertIn( 'g2', contactsResult.groups )
        self.assertIn( 'g3', contactsResult.groups )


if __name__ == '__main__' :
    unittest.main()
