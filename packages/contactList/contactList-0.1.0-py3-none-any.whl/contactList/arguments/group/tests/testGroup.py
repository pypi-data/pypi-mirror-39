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
Test the `group` subcommand.
"""

import io
import logging
import unittest

from contactList.arguments.base import CommandTree
from contactList.tests.utility import redirect_stdout_stderr

from ..group import GROUP_SUBCOMMAND_GRAPH



class TestGroupCommand( unittest.TestCase ) :
    MOCK_COMMAND_GRAPH = {
        'subcommands' : [
            GROUP_SUBCOMMAND_GRAPH,
        ]
    }


    def setUp( self ) :
        logging.disable( logging.CRITICAL )

        self.commandUnderTest = CommandTree( specification = self.MOCK_COMMAND_GRAPH )


    def tearDown( self ) :
        logging.disable( logging.NOTSET )


    def processArguments( self, inputValue ) :
        parsedArguments = self.commandUnderTest.parse( inputValue )

        return parsedArguments


    def testBadGroupRaises( self ) :
        inputValue = [
            'group',
            'badcommand'
        ]

        # Some gymnastics to suppress spurious logging in unittest output.
        file = io.StringIO()
        with redirect_stdout_stderr( file ) :
            with self.assertRaises( SystemExit ) :
                self.processArguments( inputValue )


    def testGroupAdd( self ) :
        inputValue = [
            'group',
            'add',
            'myGroup',
        ]

        parsedArguments = self.processArguments( inputValue )

        self.assertEqual( inputValue[ 1 ], parsedArguments.groupCommand )
        self.assertEqual( [inputValue[ 2 ]], parsedArguments.group )
        self.assertEqual( list(), parsedArguments.clusters )


    def testGroupRm( self ) :
        inputValue = [
            'group',
            'rm',
            'myGroup',
        ]

        parsedArguments = self.processArguments( inputValue )

        self.assertEqual( inputValue[ 1 ], parsedArguments.groupCommand )
        self.assertEqual( [inputValue[ 2 ]], parsedArguments.group )
        self.assertEqual( list(), parsedArguments.clusters )


if __name__ == '__main__' :
    unittest.main()
