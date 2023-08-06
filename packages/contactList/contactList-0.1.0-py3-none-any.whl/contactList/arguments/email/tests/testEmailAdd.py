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
Test `email add` subcommand.
"""

import unittest

from contactList.arguments.base import CommandTree

from ..add import ADD_EMAIL_SUBCOMMAND_GRAPH


class TestAddEmailSubcommand( unittest.TestCase ) :
    MOCK_COMMAND_GRAPH = {
        'subcommands' : [
            ADD_EMAIL_SUBCOMMAND_GRAPH,
        ]
    }


    def setUp( self ) :
        self.commandUnderTest = CommandTree( specification = self.MOCK_COMMAND_GRAPH )


    def processArguments( self, inputValue ) :
        return self.commandUnderTest.parse( inputValue )


    def testAddEmail( self ) :
        inputValue = [
            'add',
            'someone@somewhere.com',
        ]

        parsedArguments = self.processArguments( inputValue )

        self.assertEqual( [ inputValue[ 1 ] ], parsedArguments.email )
        self.assertEqual( list(), parsedArguments.groups )


    def testAddEmailInGroupShortForm( self ) :
        inputValue = [
            'add',
            'someone@somewhere.com',
            '-g',
            'myGroup',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], [ inputValue[ 3 ] ] )


    def testAddEmailInGroupLongForm( self ) :
        inputValue = [
            'add',
            'someone@somewhere.com',
            '--group',
            'myGroup',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], [ inputValue[ 3 ] ] )


    def doEmailInGroupTest( self, inputValue, expectedEmail, expectedGroups ) :
        parsedArguments = self.processArguments( inputValue )

        self.assertEqual( expectedEmail, parsedArguments.email )
        self.assertEqual( expectedGroups, parsedArguments.groups )


    def testAddEmailInGroupsShortForm( self ) :
        expectedList = [ 'group1', 'group2' ]

        inputValue = [
            'add',
            'someone@somewhere.com',
            '-g',
            'group1',
            'group2',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], expectedList )


    def testAddEmailInGroupsLongForm( self ) :
        expectedList = [ 'group1', 'group2' ]

        inputValue = [
            'add',
            'someone@somewhere.com',
            '--group',
            'group1',
            'group2',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], expectedList )


if __name__ == '__main__' :
    unittest.main()
