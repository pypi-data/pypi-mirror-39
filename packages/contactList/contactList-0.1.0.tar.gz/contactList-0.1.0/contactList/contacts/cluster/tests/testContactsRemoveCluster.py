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
Test contacts cluster remove operation.
"""

import unittest.mock

from ..operation import \
    ContactData, \
    remove

import contactList.contacts.contact


class TestContactsRemoveCluster( unittest.TestCase ) :
    """
    Test contacts cluster remove operation.
    """


    def setUp( self ) :
        self.contacts = ContactData()
        self.contacts.clusters[ 'otherName' ] = [
            'g1', 'g2',
        ]


    def testRemoveSingleCluster( self ) :
        """
        Removing an existing cluster removes the cluster and doesn't affect any other clusters.
        """
        clustersToRemove = [ 'someName' ]

        self.contacts.clusters[ 'someName' ] = [
            'g1', 'g2',
        ]

        self.assertEqual( 2, len( self.contacts.clusters ) )
        self.assertIn( clustersToRemove[ 0 ], self.contacts.clusters )

        # disable validation because we don't care about group validity in this case.
        with unittest.mock.patch.object( contactList.contacts.contact.ContactData, 'validate',
                                         return_value = None ) :
            contactsResult = remove( self.contacts, clustersToRemove )

        self.assertEqual( 1, len( contactsResult.clusters ) )
        self.assertIn( 'otherName', self.contacts.clusters )
        self.assertEqual( { 'g1', 'g2' }, set( self.contacts.clusters[ 'otherName' ] ) )


    def testRemoveMultipleClusters( self ) :
        """
        Removing multiple clusters removes them and doesn't affect any other clusters.
        """
        clustersToRemove = [ 'someName', 'otherName' ]

        self.contacts.clusters[ 'another' ] = [
            'g3', 'g4',
        ]
        self.contacts.clusters[ 'someName' ] = [
            'g5', 'g6',
        ]

        self.assertEqual( 3, len( self.contacts.clusters ) )
        self.assertEqual( set( clustersToRemove + [ 'another' ] ), self.contacts.clusters.keys() )

        # disable validation because we don't care about group validity in this case.
        with unittest.mock.patch.object( contactList.contacts.contact.ContactData, 'validate',
                                         return_value = None ) :
            contactsResult = remove( self.contacts, clustersToRemove )

        self.assertEqual( 1, len( contactsResult.clusters ) )
        self.assertIn( 'another', self.contacts.clusters )
        self.assertEqual( { 'g3', 'g4' }, set( self.contacts.clusters[ 'another' ] ) )


    def testRemoveNonExistentNoChange( self ) :
        """
        Removing a non-existent module silently does nothing (no error).
        """
        clustersToRemove = [ 'someName' ]

        self.assertEqual( 1, len( self.contacts.clusters ) )

        # disable validation because we don't care about group validity in this case.
        with unittest.mock.patch.object( contactList.contacts.contact.ContactData, 'validate',
                                         return_value = None ) :
            contactsResult = remove( self.contacts, clustersToRemove )

        self.assertEqual( 1, len( contactsResult.clusters ) )


class TestContactsRemoveGroupFromClusters( unittest.TestCase ) :
    """
    Test contacts remove group from clusters operation.
    """


    def setUp( self ) :
        self.contacts = ContactData()


    def testRemoveFromSingleCluster( self ) :
        """
        Specifying one cluster means to remove the group(s) from those clusters.
        """
        clustersToModify = [ 'c1' ]
        groupsToRemove = [ 'g1', 'g2' ]

        self.contacts.clusters = {
            'c1' : [ 'g1', 'g2' ],
            'c2' : [ 'g1', 'g3' ],
        }
        self.contacts.groups = {
            'g1' : [ 'a', 'b' ],
            'g2' : [ 'c', 'd' ],
            'g3' : [ 'e', 'f' ],
        }

        self.assertEqual( 2, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        remove( self.contacts, clustersToModify, groupsToRemove )

        self.assertEqual( 2, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        # group g1 is unchanged
        self.assertEqual( [ 'a', 'b' ], self.contacts.groups['g1'] )
        # group g2 is unchanged
        self.assertEqual( [ 'c', 'd' ], self.contacts.groups['g2'] )

        # cluster c1 is changed
        self.assertEqual( list(), self.contacts.clusters[ 'c1' ] )
        # cluster c2 is unchanged
        self.assertEqual( [ 'g1', 'g3' ], self.contacts.clusters[ 'c2' ] )


    def testRemoveFromMultipleClusters( self ) :
        """
        Removing groups from multiple clusters removes the groups from those clusters. Groups not in a cluster are
        silently ignored.
        """
        clustersToModify = [ 'c1', 'c2' ]
        groupsToRemove = [ 'g1', 'g2' ]

        self.contacts.clusters = {
            'c1' : [ 'g1', 'g2' ],
            'c2' : [ 'g1', 'g3' ],
        }
        self.contacts.groups = {
            'g1' : [ 'a', 'b' ],
            'g2' : [ 'c', 'd' ],
            'g3' : [ 'e', 'f' ],
        }

        self.assertEqual( 2, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        remove( self.contacts, clustersToModify, groupsToRemove )

        self.assertEqual( 2, len( self.contacts.clusters ) )
        self.assertEqual( 3, len( self.contacts.groups ) )

        # group g1 is unchanged
        self.assertEqual( [ 'a', 'b' ], self.contacts.groups['g1'] )
        # group g2 is unchanged
        self.assertEqual( [ 'c', 'd' ], self.contacts.groups['g2'] )

        # cluster c1 is changed
        self.assertEqual( list(), self.contacts.clusters[ 'c1' ] )
        # cluster c2 is changed
        self.assertEqual( [ 'g3' ], self.contacts.clusters[ 'c2' ] )


if __name__ == '__main__' :
    unittest.main()
