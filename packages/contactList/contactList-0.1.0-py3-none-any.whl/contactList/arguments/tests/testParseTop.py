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
Test the top level command line argument parser.
"""

import unittest

from ..base import BadArgument
from ..top import ContactsOptions


class TestParseArguments( unittest.TestCase ) :

    def testNoSubcommandRaises( self ) :
        inputValue = [
        ]

        with self.assertRaisesRegex( BadArgument, '^Must specify a contact list operation' ) :
            ContactsOptions.from_arguments( inputValue )


    def testContactsFileShortForm( self ) :
        inputValue = [
            '-f',
            'someFile.yml',
            'cluster',
            'add',
            'someName',
        ]

        self.doContactsFileTest( inputValue )


    def doContactsFileTest( self, inputValue ) :
        actualOptions = ContactsOptions.from_arguments( inputValue )

        self.assertEqual( inputValue[ 1 ], actualOptions.contactsFile )

        return actualOptions


    def testContactsFileLongForm( self ) :
        inputValue = [
            '--file',
            'someFile.yml',
            'cluster',
            'add',
            'someName',
        ]

        self.doContactsFileTest( inputValue )


    def testAddCluster( self ) :
        inputValue = [
            'cluster',
            'add',
            'someName',
        ]
        actualOptions = ContactsOptions.from_arguments( inputValue )

        self.assertEqual( inputValue[ 0 ], actualOptions.activeSubcommand )
        self.assertEqual( 'contacts.yml', actualOptions.contactsFile )


    def testAddEmail( self ) :
        inputValue = [
            'email',
            'add',
            'someName',
        ]
        actualOptions = ContactsOptions.from_arguments( inputValue )

        self.assertEqual( inputValue[ 0 ], actualOptions.activeSubcommand )
        self.assertEqual( 'contacts.yml', actualOptions.contactsFile )


    def testAddGroup( self ) :
        inputValue = [
            'group',
            'add',
            'someName',
        ]
        actualOptions = ContactsOptions.from_arguments( inputValue )

        self.assertEqual( inputValue[ 0 ], actualOptions.activeSubcommand )
        self.assertEqual( 'contacts.yml', actualOptions.contactsFile )


    def testRmCluster( self ) :
        inputValue = [
            'cluster',
            'rm',
            'someName',
        ]
        actualOptions = ContactsOptions.from_arguments( inputValue )

        self.assertEqual( inputValue[ 0 ], actualOptions.activeSubcommand )
        self.assertEqual( 'contacts.yml', actualOptions.contactsFile )


    def testRmEmail( self ) :
        inputValue = [
            'email',
            'rm',
            'someName',
        ]
        actualOptions = ContactsOptions.from_arguments( inputValue )

        self.assertEqual( inputValue[ 0 ], actualOptions.activeSubcommand )
        self.assertEqual( 'contacts.yml', actualOptions.contactsFile )


    def testRmGroup( self ) :
        inputValue = [
            'group',
            'rm',
            'someName',
        ]
        actualOptions = ContactsOptions.from_arguments( inputValue )

        self.assertEqual( inputValue[ 0 ], actualOptions.activeSubcommand )
        self.assertEqual( 'contacts.yml', actualOptions.contactsFile )


if __name__ == '__main__' :
    unittest.main()
