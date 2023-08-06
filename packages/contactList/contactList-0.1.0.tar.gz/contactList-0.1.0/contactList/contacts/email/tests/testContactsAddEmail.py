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
Test contacts email add operation.
"""

import unittest.mock

from ..operation import \
    ContactData, \
    add


class TestContactsAddEmail( unittest.TestCase ) :
    """
    Test contacts email add operation.
    """


    def setUp( self ) :
        self.emailsToAdd = [ 'e@f', 'g@h' ]

        self.contacts = ContactData()
        self.contacts.groups = {
            'g1' : [
                'a@b',
            ],
            'g2' : [
                'c@d',
                'i@j',
            ],
        }


    def testAddEmailAllGroups( self ) :
        """
        Adding an email to all groups adds the email to all groups.
        """
        expectedGroups = {
            'g1' : self.contacts.groups[ 'g1' ] + self.emailsToAdd,
            'g2' : self.contacts.groups[ 'g2' ] + self.emailsToAdd,
        }

        contactsResult = add( self.contacts, self.emailsToAdd )

        self.assertEqual( expectedGroups, contactsResult.groups )


    def testAddEmailSpecificGroups( self ) :
        """
        Adding an email to specific groups only adds the email to those groups.
        """
        groupsToAdd = [ 'g2' ]

        expectedGroups = {
            'g1' : self.contacts.groups[ 'g1' ],
            'g2' : self.contacts.groups[ 'g2' ] + self.emailsToAdd,
        }

        contactsResult = add( self.contacts, self.emailsToAdd,
                              groups = groupsToAdd )

        self.assertEqual( expectedGroups, contactsResult.groups )


    def testAddExistingEmail( self ) :
        """
        Adding an existing email is silently ignored.
        """
        emailsToAdd = [ 'c@d' ]

        expectedGroups = self.contacts.groups

        contactsResult = add( self.contacts, emailsToAdd )

        self.assertEqual( expectedGroups, contactsResult.groups )


    def testAddExistingEmailSomeGroups( self ) :
        """
        Adding an email that exists in some groups but not all adds the email to the groups where it is missing.
        """
        emailsToAdd = [ 'c@d' ]

        expectedGroups = {
            'g1' : self.contacts.groups[ 'g1' ] + emailsToAdd,
            'g2' : self.contacts.groups[ 'g2' ],
        }

        contactsResult = add( self.contacts, emailsToAdd )

        self.assertEqual( expectedGroups, contactsResult.groups )


    def testMultipleAddsDoesNothing( self ) :
        """
        Adding the same email multiple times has no effect..
        """
        emailsToAdd = [ 'c@d' ]
        groups = [ 'g1' ]

        expectedGroups = {
            'g1' : [
                'a@b',
                'c@d',
            ],
            'g2' : [
                'c@d',
                'i@j',
            ],
        }

        interimResult = add( self.contacts, emailsToAdd,
                             groups = groups )
        contactsResult = add( interimResult, emailsToAdd,
                              groups = groups )

        self.assertEqual( expectedGroups, contactsResult.groups )


if __name__ == '__main__' :
    unittest.main()
