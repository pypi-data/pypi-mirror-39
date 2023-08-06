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
Test contact data YAML export.
"""

import io
import unittest.mock

from contactList.contacts import Contacts

# DO NOT DELETE! Used by unittest.mock.patch below.
import contactList.contacts.contact


class TestContactsYamlExport( unittest.TestCase ) :

    def setUp( self ) :
        self.yamlData = {
            'clusters' : {
                'c1' : [ 'g1' ],
                'c2' : [ 'g2', 'g3' ],
            },
            'groups' : {
                'g1' : [ 'a', 'b' ],
                'g2' : [ 'c', 'd' ],
                'g3' : [ 'a', 'e', 'f' ],
            },
        }

        self.contactsUnderTest = Contacts.from_yamlData( self.yamlData )


    def testFileObjectSave( self ) :
        with unittest.mock.patch( 'contactList.contacts.contact.yaml.dump' ) as mockYamlDump :
            with io.StringIO() as fileObject :
                self.contactsUnderTest.to_yamlFile( fileObject = fileObject )

            mockYamlDump.assert_called_once_with( self.yamlData, fileObject )


    def testFilenameSave( self ) :
        expectedFilename = 'some/file.name'

        # https://docs.python.org/3/library/unittest.mock.html?highlight=mock_open#unittest.mock.mock_open
        mockOpen = unittest.mock.mock_open()
        with unittest.mock.patch( 'contactList.contacts.contact.open', mockOpen ), \
             unittest.mock.patch( 'contactList.contacts.contact.yaml.dump' ) as mockYamlDump :
            self.contactsUnderTest.to_yamlFile( filename = expectedFilename )

            mockOpen.assert_called_once_with( expectedFilename, 'w' )

            mockFileObject = mockOpen.return_value.__enter__.return_value

            mockYamlDump.assert_called_once_with( self.yamlData, mockFileObject )


    def testDefaultFilenameSave( self ) :
        expectedFilename = 'contacts.yml'
        mockOpen = unittest.mock.mock_open()
        with unittest.mock.patch( 'contactList.contacts.contact.open', mockOpen ), \
             unittest.mock.patch( 'contactList.contacts.contact.yaml.dump' ) as mockYamlDump :
            self.contactsUnderTest.to_yamlFile()

            mockOpen.assert_called_once_with( expectedFilename, 'w' )

            mockFileObject = mockOpen.return_value.__enter__.return_value

            mockYamlDump.assert_called_once_with( self.yamlData, mockFileObject )


if __name__ == '__main__' :
    unittest.main()
