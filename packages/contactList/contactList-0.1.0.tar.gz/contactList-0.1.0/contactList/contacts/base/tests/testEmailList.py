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
Test email list extractions from contacts list.
"""

import unittest

from .. import ContactData


class TestContactEmails( unittest.TestCase ) :

    def setUp( self ) :
        groups = {
            'group1' : [ 'a@g1.com', 'b@g2.ca', ],
            'group2' : [ 'c@g3.co.uk', ],
        }

        clusters = {
            'c1' : [ 'group1', 'group2' ],
            'c2' : [ 'group1' ],
        }

        self.contactsUnderTest = ContactData()
        self.contactsUnderTest.groups = groups
        self.contactsUnderTest.clusters = clusters


    def testEmailsC1( self ) :
        """
        Multiple groups of emails are correctly aggregated in a cluster.
        """
        expectedEmails = set( self.contactsUnderTest.groups[ 'group1' ] ) | set(
            self.contactsUnderTest.groups[ 'group2' ] )

        actualEmails = self.contactsUnderTest.emails( 'c1' )

        self.assertEqual( expectedEmails, actualEmails )


    def testEmailsC2( self ) :
        """
        A single group of emails is correctly extracted from a cluster.
        """
        expectedEmails = set( self.contactsUnderTest.groups[ 'group1' ] )

        actualEmails = self.contactsUnderTest.emails( 'c2' )

        self.assertEqual( expectedEmails, actualEmails )


if __name__ == '__main__' :
    unittest.main()
