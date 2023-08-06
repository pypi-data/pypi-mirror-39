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
High level integration tests of contacts operations with contacts data.
"""

import unittest.mock

from ..contact import \
    Contacts, \
    ContactsOptions


class TestContacts( unittest.TestCase ) :
    """
    Test high level contacts instantiation.
    """


    def testEmptyContacts( self ) :
        contactsUnderTest = Contacts()

        self.assertEqual( dict(), contactsUnderTest.data.clusters )
        self.assertEqual( dict(), contactsUnderTest.data.groups )


class TestGroupAdd( unittest.TestCase ) :
    """
    Test integration of group add command.
    """


    def setUp( self ) :
        self.contactsUnderTest = Contacts()

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )
        self.mockOptions.activeSubcommand = 'group'
        self.mockOptions.clusters = list()


    def testAddGroups( self ) :
        self.mockOptions.groupCommand = 'add'

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 0, len( self.contactsUnderTest.data.groups ) )

        self.mockOptions.group = [ 'g1', 'g2' ]

        self.contactsUnderTest.applyAction( self.mockOptions )

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 2, len( self.contactsUnderTest.data.groups ) )

        self.assertEqual( set( self.mockOptions.group ), self.contactsUnderTest.data.groups.keys() )


class TestGroupRemove( unittest.TestCase ) :
    """
    Test integration of group remove command.
    """


    def setUp( self ) :
        self.contactsUnderTest = Contacts()

        # Add some groups to work with
        self.contactsUnderTest.data.groups = {
            'g1' : list(),
            'g2' : list(),
        }

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )
        self.mockOptions.activeSubcommand = 'group'
        self.mockOptions.clusters = list()

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 2, len( self.contactsUnderTest.data.groups ) )


    def testRemoveGroups( self ) :
        self.mockOptions.groupCommand = 'rm'
        self.mockOptions.group = [ 'g1', 'g2' ]

        self.contactsUnderTest.applyAction( self.mockOptions )

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 0, len( self.contactsUnderTest.data.groups ) )


class TestClusterAdd( unittest.TestCase ) :
    """
    Test integration of cluster add command.
    """


    def setUp( self ) :
        self.contactsUnderTest = Contacts()

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )
        self.mockOptions.activeSubcommand = 'cluster'
        self.mockOptions.clusters = list()


    def testAddCluster( self ) :
        self.mockOptions.clusterCommand = 'add'

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 0, len( self.contactsUnderTest.data.groups ) )

        self.mockOptions.cluster = [ 'c1', 'c2' ]

        self.contactsUnderTest.applyAction( self.mockOptions )

        self.assertEqual( 2, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 0, len( self.contactsUnderTest.data.groups ) )

        self.assertEqual( set( self.mockOptions.cluster ), self.contactsUnderTest.data.clusters.keys() )


class TestClusterRemove( unittest.TestCase ) :
    """
    Test integration of cluster remove command.
    """


    def setUp( self ) :
        self.contactsUnderTest = Contacts()

        # Add some clusters to work with
        self.contactsUnderTest.data.clusters = {
            'c1' : list(),
            'c2' : list(),
        }

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )
        self.mockOptions.activeSubcommand = 'cluster'
        self.mockOptions.cluster = list()
        self.mockOptions.groups = None

        self.assertEqual( 2, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 0, len( self.contactsUnderTest.data.groups ) )


    def testRemoveClusters( self ) :
        self.mockOptions.clusterCommand = 'rm'

        self.mockOptions.cluster = [ 'c1', 'c2' ]

        self.contactsUnderTest.applyAction( self.mockOptions )

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 0, len( self.contactsUnderTest.data.groups ) )


class TestEmailAdd( unittest.TestCase ) :
    """
    Test integration of email add command.
    """


    def setUp( self ) :
        self.contactsUnderTest = Contacts()

        # Add some groups to work with
        self.contactsUnderTest.data.groups = {
            'g1' : list(),
            'g2' : list(),
        }

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )
        self.mockOptions.activeSubcommand = 'email'
        self.mockOptions.groups = list()

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 2, len( self.contactsUnderTest.data.groups ) )


    def testAddEmails( self ) :
        self.mockOptions.emailCommand = 'add'

        self.mockOptions.email = [ 'a@b', 'c@d' ]
        self.mockOptions.groups = [ 'g1', 'g2' ]

        self.contactsUnderTest.applyAction( self.mockOptions )

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 2, len( self.contactsUnderTest.data.groups ) )

        self.assertEqual( self.mockOptions.email, self.contactsUnderTest.data.groups[ 'g1' ] )
        self.assertEqual( self.mockOptions.email, self.contactsUnderTest.data.groups[ 'g2' ] )


class TestEmailRemove( unittest.TestCase ) :
    """
    Test integration of email remove command.
    """


    def setUp( self ) :
        self.contactsUnderTest = Contacts()

        # Add some groups to work with
        self.contactsUnderTest.data.groups = {
            'g1' : [ 'a@b', 'c@d', ],
            'g2' : [ 'c@d', 'e@f', ],
        }

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )

        self.mockOptions = unittest.mock.create_autospec( ContactsOptions )
        self.mockOptions.activeSubcommand = 'email'
        self.mockOptions.groups = list()

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 2, len( self.contactsUnderTest.data.groups ) )


    def testRemoveEmail( self ) :
        self.mockOptions.emailCommand = 'rm'

        self.mockOptions.email = [ 'c@d' ]

        self.contactsUnderTest.applyAction( self.mockOptions )

        self.assertEqual( 0, len( self.contactsUnderTest.data.clusters ) )
        self.assertEqual( 2, len( self.contactsUnderTest.data.groups ) )

        self.assertEqual( [ 'a@b' ], self.contactsUnderTest.data.groups[ 'g1' ] )
        self.assertEqual( [ 'e@f' ], self.contactsUnderTest.data.groups[ 'g2' ] )


if __name__ == '__main__' :
    unittest.main()
