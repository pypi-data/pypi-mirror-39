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
Test contact data YAML import.
"""

import io
import unittest.mock
import yaml.constructor

from contactList.contacts import Contacts

# DO NOT DELETE. Used by unittest.mock below.
import contactList.contacts.contact


class TestContactsFromYamlData( unittest.TestCase ) :
    """
    Test constructing contacts object from a YAML data structure.
    """


    def testClusters( self ) :
        yamlData = {
            'clusters' : {
                'one' : [ 'a', 'b' ],
                'two' : [ 'c', 'd' ],
            },
        }

        contactsUnderTest = Contacts.from_yamlData( yamlData )

        self.assertIn( 'one', contactsUnderTest.data.clusters )
        self.assertIn( 'two', contactsUnderTest.data.clusters )
        self.assertTrue( isinstance( contactsUnderTest.data.clusters, dict ) )


    def testImportEmpty( self ) :
        yamlData = dict()

        contactsUnderTest = Contacts.from_yamlData( yamlData )

        self.assertTrue( isinstance( contactsUnderTest, Contacts ) )

        self.assertEqual( dict(), contactsUnderTest.data.groups )
        self.assertEqual( dict(), contactsUnderTest.data.clusters )


    def testImportNone( self ) :
        """
        Construct an empty contacts object for ``None`` input.
        """
        yamlData = None

        contactsUnderTest = Contacts.from_yamlData( yamlData )

        self.assertTrue( isinstance( contactsUnderTest, Contacts ) )

        self.assertEqual( dict(), contactsUnderTest.data.groups )
        self.assertEqual( dict(), contactsUnderTest.data.clusters )


    def testGroups( self ) :
        yamlData = {
            'groups' : {
                'one' : [ 'a', 'b' ],
                'two' : [ 'c', 'd' ],
            },
        }

        contactsUnderTest = Contacts.from_yamlData( yamlData )

        self.assertIn( 'one', contactsUnderTest.data.groups )
        self.assertIn( 'two', contactsUnderTest.data.groups )
        self.assertTrue( isinstance( contactsUnderTest.data.groups, dict ) )


    def testGroupsOk( self ) :
        yamlData = {
            'clusters' : {
                'c1' : [ 'g1', 'g2' ],
            },
            'groups' : {
                'g1' : [ 'a', 'b' ],
                'g2' : [ 'c', 'd' ],
            },
        }

        contactsUnderTest = Contacts.from_yamlData( yamlData )


class TestContactsFromYamlFile( unittest.TestCase ) :

    def testFilenameDefaultArgument( self ) :
        yamlData = """{
  'groups' : {
    'one' : [ 'a', 'b' ],
    'two' : [ 'c', 'd' ],
  },
}"""

        expectedFilename = 'someFile'

        with unittest.mock.patch( 'contactList.contacts.contact.os.path.isfile',
                                  return_value = True ), \
             unittest.mock.patch( 'contactList.contacts.contact.open',
                                  unittest.mock.mock_open( read_data = yamlData ) )  as mockOpen :
            contactsUnderTest = Contacts.from_yamlFile( expectedFilename )

            mockOpen.assert_called_once_with( expectedFilename, 'r' )

            self.assertIn( 'one', contactsUnderTest.data.groups )
            self.assertIn( 'two', contactsUnderTest.data.groups )


    def testFileNotExistRaises( self ) :
        """
        ``FileNotFoundError`` is raised on attempting to load from a file that doesn't exist.
        """
        with unittest.mock.patch( 'contactList.contacts.contact.os.path.isfile',
                                  return_value = False ) :
            with self.assertRaisesRegex( FileNotFoundError, '^File does not exist' ) :
                Contacts.from_yamlFile( 'some/file' )


class TestContactSafeLoad( unittest.TestCase ) :

    def setUp( self ) :
        self.unsafeYamlData = """
'groups' : 
  'one': !!python/object:Exception
  'two' : [ 'c', 'd' ]
        """


    def testFileObjectLoad( self ) :
        functionUnderTest = Contacts.from_yamlFile

        with io.StringIO( initial_value = self.unsafeYamlData ) as fileObject :
            functionArgument = { 'fileObject' : fileObject }

            self.doTest( functionUnderTest, functionArgument )


    def testYamlFileLoad( self ) :
        expectedFilename = 'someFile.yml'

        with unittest.mock.patch( 'contactList.contacts.contact.os.path.isfile',
                                  return_value = True ), \
             unittest.mock.patch( 'contactList.contacts.contact.open',
                                  unittest.mock.mock_open( read_data = self.unsafeYamlData ) ) as mockOpen :
            functionUnderTest = Contacts.from_yamlFile
            functionArgument = { 'filename' : expectedFilename }

            self.doTest( functionUnderTest, functionArgument )

            # mock_open.assert_called_once_with( expectedFilename )
            mockOpen.assert_called_once_with( expectedFilename, 'r' )


    def doTest( self, functionUnderTest, functionArgument ) :
        with self.assertRaises(
                yaml.constructor.ConstructorError,
                msg = 'could not determine a constructor for the tag ''tag:yaml.org, 2002:python/object:Exception'''
        ) :
            functionUnderTest( **functionArgument )


if __name__ == '__main__' :
    unittest.main()
