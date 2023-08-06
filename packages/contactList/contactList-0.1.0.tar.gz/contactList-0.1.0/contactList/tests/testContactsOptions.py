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
Integration tests of command line argument parsing and contacts data.
"""

import unittest.mock

from ..contacts import \
    Contacts, \
    ContactsOperationError
from ..entry import main

# DO NOT DELETE! Used by unittest.mock.patch below.
import contactList


class TestClusterAddIntegration( unittest.TestCase ) :

    def setUp( self ) :
        self.mock_contacts = Contacts()


    def testAddNewCluster( self ) :
        inputValue = [
            '-d',
            '-f',
            'some/file',
            'cluster',
            'add',
            'myCluster',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertIn( inputValue[ 5 ], self.mock_contacts.data.clusters )


class TestClusterRemoveIntegration( unittest.TestCase ) :

    def setUp( self ) :
        self.mock_contacts = Contacts()

        self.mock_contacts.data.clusters = {
            'c1' : list(),
            'c2' : list(),
        }


    def testRemoveExistingCluster( self ) :
        inputValue = [
            '-d',
            '-f',
            'some/file',
            'cluster',
            'rm',
            'c1',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertNotIn( 'c1', self.mock_contacts.data.clusters )
            self.assertIn( 'c2', self.mock_contacts.data.clusters )


    def testRemoveExistingClusterGroupMembers( self ) :
        self.mock_contacts.data.clusters = {
            'c1' : [ 'g1' ],
            'c2' : [ 'g2' ],
        }
        self.mock_contacts.data.groups = {
            'g1' : [ 'a@b', 'c@d' ],
            'g2' : [ 'c@d', 'e@f' ],
        }

        inputValue = [
            '-d',
            '-f',
            'some/file',
            'cluster',
            'rm',
            'c1',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertNotIn( 'c1', self.mock_contacts.data.clusters )
            self.assertIn( 'c2', self.mock_contacts.data.clusters )


    def testRemoveClusterGroupMember( self ) :
        self.mock_contacts.data.clusters = {
            'c1' : [ 'g1' ],
            'c2' : [ 'g2' ],
        }
        self.mock_contacts.data.groups = {
            'g1' : [ 'a@b', 'c@d' ],
            'g2' : [ 'c@d', 'e@f' ],
        }

        inputValue = [
            '-d',
            '-f',
            'some/file',
            'cluster',
            'rm',
            'c1',
            '--group',
            'g1'
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertEqual( list(), self.mock_contacts.data.clusters[ 'c1' ] )
            self.assertIn( 'c2', self.mock_contacts.data.clusters )


    def testRemoveClusterMultipleGroupMembers( self ) :
        self.mock_contacts.data.clusters = {
            'c1' : [ 'g1', 'g2' ],
            'c2' : [ 'g2' ],
        }
        self.mock_contacts.data.groups = {
            'g1' : [ 'a@b', 'c@d' ],
            'g2' : [ 'c@d', 'e@f' ],
        }

        inputValue = [
            '-d',
            '-f',
            'some/file',
            'cluster',
            'rm',
            'c1',
            '--groups',
            'g1',
            'g2',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertEqual( list(), self.mock_contacts.data.clusters[ 'c1' ] )
            self.assertIn( 'c2', self.mock_contacts.data.clusters )


class TestEmailAddIntegration( unittest.TestCase ) :

    def setUp( self ) :
        self.mock_contacts = Contacts()

        self.mock_contacts.data.groups = {
            'g1' : list(),
            'g2' : list(),
        }


    def testAddNewEmail( self ) :
        inputValue = [
            '-d',
            '-f',
            'some/file',
            'email',
            'add',
            'a@b',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertEqual( [ 'a@b' ], self.mock_contacts.data.groups[ 'g1' ] )
            self.assertEqual( [ 'a@b' ], self.mock_contacts.data.groups[ 'g2' ] )


class TestEmailRemoveIntegration( unittest.TestCase ) :

    def setUp( self ) :
        self.mock_contacts = Contacts()

        self.mock_contacts.data.groups = {
            'g1' : [ 'a@b' ],
            'g2' : [ 'a@b', 'c@d' ],
        }


    def testRemoveExistingEmail( self ) :
        inputValue = [
            '-d',
            '-f',
            'some/file',
            'email',
            'rm',
            'a@b',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertEqual( list(), self.mock_contacts.data.groups[ 'g1' ] )
            self.assertEqual( [ 'c@d' ], self.mock_contacts.data.groups[ 'g2' ] )


class TestGroupAddIntegration( unittest.TestCase ) :

    def setUp( self ) :
        self.mock_contacts = Contacts()


    def testAddNewGroup( self ) :
        inputValue = [
            '-d',
            '-f',
            'some/file',
            'group',
            'add',
            'myGroup',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertIn( inputValue[ 5 ], self.mock_contacts.data.groups )


    def testAddNewGroupToNonexistentCluster( self ) :
        """
        Adding a new group to a non-existent cluster implicitly creates the cluster as well as adding the group to
        the cluster.
        """
        inputValue = [
            '-d',
            '-f',
            'some/file',
            'group',
            'add',
            'myGroup',
            '--cluster',
            'myCluster',
        ]

        self.assertNotIn( inputValue[ 7 ], self.mock_contacts.data.clusters )

        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertIn( inputValue[ 5 ], self.mock_contacts.data.groups )
            self.assertIn( inputValue[ 7 ], self.mock_contacts.data.clusters )
            self.assertIn( inputValue[ 5 ], self.mock_contacts.data.clusters[ inputValue[ 7 ] ] )


class TestGroupRemoveIntegration( unittest.TestCase ) :

    def setUp( self ) :
        self.mock_contacts = Contacts()

        self.mock_contacts.data.clusters = dict()
        self.mock_contacts.data.groups = {
            'g1' : list(),
            'g2' : list(),
        }


    def testRemoveExistingGroup( self ) :
        self.assertTrue( not self.mock_contacts.data.clusters )

        inputValue = [
            '-d',
            '-f',
            'some/file',
            'group',
            'rm',
            'g1',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertNotIn( 'g1', self.mock_contacts.data.groups )


    def testRemoveGroupFromCluster( self ) :
        self.mock_contacts.data.clusters = {
            'c1' : [ 'g1' ],
            'c2' : [ 'g2' ],
        }

        inputValue = [
            '-d',
            '-f',
            'some/file',
            'group',
            'rm',
            'g1',
            '--cluster',
            'c1',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertIn( 'g1', self.mock_contacts.data.groups )
            self.assertNotIn( 'g1', self.mock_contacts.data.clusters[ 'c1' ] )


    def testRemoveGroupFromMultipleClusters( self ) :
        self.mock_contacts.data.clusters = {
            'c1' : [ 'g1' ],
            'c2' : [ 'g2', 'g1' ],
        }

        inputValue = [
            '-d',
            '-f',
            'some/file',
            'group',
            'rm',
            'g1',
            '--clusters',
            'c1',
            'c2',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            main( inputValue )

            self.assertIn( 'g1', self.mock_contacts.data.groups )
            self.assertNotIn( 'g1', self.mock_contacts.data.clusters[ 'c1' ] )
            self.assertNotIn( 'g1', self.mock_contacts.data.clusters[ 'c2' ] )


    def testRemoveExistingGroupClusterMemberRaises( self ) :
        """
        Removing a group that is a member of a cluster removes the group and it's entry in the cluster.
        """
        self.mock_contacts.data.clusters = {
            'c1' : [ 'g1' ],
            'c2' : [ 'g2' ],
        }
        inputValue = [
            '-d',
            '-f',
            'some/file',
            'group',
            'rm',
            'g1',
        ]
        with unittest.mock.patch( 'contactList.entry.Contacts.from_yamlFile',
                                  return_value = self.mock_contacts ), \
             unittest.mock.patch( 'contactList.contacts.Contacts.to_yamlFile' ) :
            with self.assertRaisesRegex( ContactsOperationError, '^Remove group\(s\) from clusters before removing the '
                                                                 'group\(s\)' ) :
                main( inputValue )


if __name__ == '__main__' :
    unittest.main()
