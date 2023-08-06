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
Test contacts email remove operation.
"""

import unittest.mock

from ..operation import \
    ContactData, \
    remove


class TestContactsRemoveEmail( unittest.TestCase ) :
    """
    Test contacts email remove operation.
    """

    def setUp( self ) :
        self.contacts = ContactData()


    def testRemoveFromSingleGroup( self ) :
        """
        Specify a single group and only that group has the email removed.
        """
        groups = [ 'g1' ]
        emailsToRemove = [ 'a@b' ]

        self.assertEqual( 0, len( self.contacts.clusters ) )
        self.assertEqual( 0, len( self.contacts.groups ) )

        self.contacts.groups = {
            'g1' : [ 'a@b', 'c@d' ],
            'g2' : [ 'e@f', 'a@b' ],
        }

        self.assertEqual( 2, len( self.contacts.groups[ 'g1' ] ) )

        remove( self.contacts, emailsToRemove, groups )

        self.assertEqual( 1, len( self.contacts.groups[ 'g1' ] ) )
        self.assertEqual( [ 'c@d' ], self.contacts.groups[ 'g1' ] )
        self.assertEqual( 2, len( self.contacts.groups[ 'g2' ] ) )
        self.assertEqual( [ 'e@f', 'a@b' ], self.contacts.groups[ 'g2' ] )


    def testRemoveFromAllGroups( self ) :
        """
        Empty groups option (default) implies remove the email from all groups.
        """
        self.assertEqual( 0, len( self.contacts.clusters ) )
        self.assertEqual( 0, len( self.contacts.groups ) )

        emailsToRemove = [ 'a@b' ]

        self.contacts.groups = {
            'g1' : [ 'a@b', 'c@d' ],
            'g2' : [ 'e@f', 'a@b' ],
        }

        self.assertEqual( 2, len( self.contacts.groups[ 'g1' ] ) )
        self.assertEqual( 2, len( self.contacts.groups[ 'g2' ] ) )

        remove( self.contacts, emailsToRemove )

        self.assertEqual( 1, len( self.contacts.groups[ 'g1' ] ) )
        self.assertEqual( [ 'c@d' ], self.contacts.groups[ 'g1' ] )
        self.assertEqual( 1, len( self.contacts.groups[ 'g2' ] ) )
        self.assertEqual( [ 'e@f' ], self.contacts.groups[ 'g2' ] )


if __name__ == '__main__' :
    unittest.main()
