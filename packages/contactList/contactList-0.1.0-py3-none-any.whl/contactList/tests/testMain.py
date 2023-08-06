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
Test main entry point.
"""

import io
import unittest.mock

from .utility import redirect_stdout_stderr

from ..entry import main

# DO NOT DELETE. Used by unittest.mock below.
import contactList.entry


class TestMain( unittest.TestCase ) :
    """
    Test main entry point.
    """


    def testArguments( self ) :
        inputArguments = [
            'add-cluster',
            'someName',
        ]

        mockOptions = unittest.mock.create_autospec( contactList.entry.ContactsOptions )
        mockOptions.contactsFile = inputArguments[ 1 ]
        mockOptions.debug = True

        mockContacts = unittest.mock.create_autospec( contactList.entry.Contacts )

        with unittest.mock.patch.object( contactList.entry.ContactsOptions, 'from_arguments' ) as mockFromArguments, \
                unittest.mock.patch.object( contactList.entry.Contacts, 'from_yamlFile' ) as mockContactsFromYamlFile :
            mockFromArguments.return_value = mockOptions
            mockContactsFromYamlFile.return_value = mockContacts

            main( inputArguments )

            mockFromArguments.assert_called_once_with( inputArguments )
            mockContactsFromYamlFile.assert_called_once_with( filename = inputArguments[ 1 ] )

            mockContacts.applyAction.assert_called_once_with( mockOptions )
            mockContacts.to_yamlFile.assert_called_once_with( filename = inputArguments[ 1 ] )


def mockFromYaml( *args, **kwargs ) :
    raise RuntimeError( 'This is an error' )


class TestExceptionsDebug( unittest.TestCase ) :

    def setUp( self ) :
        self.mockOptions = unittest.mock.create_autospec( contactList.entry.ContactsOptions )


    def testDisabledDebugModeCatchesExceptions( self ) :
        """
        Exceptions are caught by the entry point and sys.exit is called.
        """
        self.mockOptions.debug = False

        with unittest.mock.patch.object( contactList.entry.ContactsOptions, 'from_arguments',
                                         return_value = self.mockOptions ), \
             unittest.mock.patch( 'contactList.entry.sys.exit' ) \
                as mock_sysExit :
            # Temporarily suppress output from entry point.
            f = io.StringIO()
            with redirect_stdout_stderr( f ) :
                main( list() )

            mock_sysExit.assert_called_once_with( 1 )


    def testEnabledDebugModeRaises( self ) :
        """
        Exceptions are caught by the entry point and sys.exit is called.
        """
        self.mockOptions.debug = True

        with unittest.mock.patch.object( contactList.entry.ContactsOptions, 'from_arguments',
                                         return_value = self.mockOptions ), \
             unittest.mock.patch.object( contactList.entry.Contacts, 'from_yamlFile',
                                         side_effect = mockFromYaml ), \
             unittest.mock.patch( 'contactList.entry.sys.exit' ) as mock_sysExit :
            with self.assertRaises( Exception ) :
                # Temporarily suppress output from entry point.
                f = io.StringIO()
                with redirect_stdout_stderr( f ) :
                    main( list() )

            mock_sysExit.assert_not_called()


if __name__ == '__main__' :
    unittest.main()
