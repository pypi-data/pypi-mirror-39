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
Test contacts cluster add operation.
"""

import unittest.mock

from ..operation import \
    ContactData, \
    add

# DO NOT DELETE! Use by unittest.mock below
import contactList.contacts.contact


class TestContactsAddCluster( unittest.TestCase ) :
    """
    Test contacts cluster add operation.
    """


    def setUp( self ) :
        self.contacts = ContactData()


    def testSingleCluster( self ) :
        """
        Adding a single cluster results in the cluster being added.
        """
        clustersToAdd = [ 'someName' ]

        self.assertEqual( 0, len( self.contacts.clusters ) )

        contactsResult = add( self.contacts, clustersToAdd )

        self.assertEqual( 1, len( contactsResult.clusters ) )
        self.assertEqual( set(clustersToAdd), contactsResult.clusters.keys() )


    def testMultipleClusters( self ) :
        """
        Adding multiple clusters results in the clusters being added.
        """
        clustersToAdd = [ 'someName', 'otherName' ]

        self.assertEqual( 0, len( self.contacts.clusters ) )

        contactsResult = add( self.contacts, clustersToAdd )

        self.assertEqual( 2, len( contactsResult.clusters ) )
        self.assertEqual( set( clustersToAdd ), contactsResult.clusters.keys() )


    def testMixedClusters( self ) :
        """
        Adding a combination of clusters that exist and don't results in the non-existent clusters being added and
        the existing clusters being ignored.
        """
        clustersToAdd = [ 'someName', 'otherName' ]

        self.contacts.clusters[ 'otherName' ] = list()

        self.assertEqual( 1, len( self.contacts.clusters ) )

        contactsResult = add( self.contacts, clustersToAdd )

        self.assertEqual( 2, len( contactsResult.clusters ) )
        self.assertEqual( set( clustersToAdd ), contactsResult.clusters.keys() )


    def testNoClustersExistingGroupNoChange( self ) :
        """
        Adding an existing cluster with content silently makes no change to the existing cluster (no error).
        """
        clustersToAdd = [ 'someName' ]

        expectedClusterContents = [ 'g1', 'g2' ]

        self.contacts.clusters[ clustersToAdd[ 0 ] ] = expectedClusterContents
        self.assertEqual( 1, len( self.contacts.clusters ) )

        # mock validate method because we are deliberately using invalid contacts data.
        with unittest.mock.patch.object( contactList.contacts.contact.ContactData, 'validate' ) as mockValidate :
            mockValidate.return_value = None

            contactsResult = add( self.contacts, clustersToAdd )

        self.assertEqual( 1, len( contactsResult.clusters ) )
        self.assertIn( clustersToAdd[ 0 ], contactsResult.clusters )
        self.assertEqual( expectedClusterContents, contactsResult.clusters[ clustersToAdd[ 0 ] ] )


if __name__ == '__main__' :
    unittest.main()
