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
Test the group add subcommand.
"""

import unittest

from contactList.arguments.base import CommandTree

from ..add import ADD_GROUP_SUBCOMMAND_GRAPH


class TestAddGroupSubcommand( unittest.TestCase ) :
    MOCK_COMMAND_GRAPH = {
        'subcommands' : [
            ADD_GROUP_SUBCOMMAND_GRAPH,
        ]
    }


    def setUp( self ) :
        self.commandUnderTest = CommandTree( specification = self.MOCK_COMMAND_GRAPH )


    def testAddGroup( self ) :
        inputValue = [
            'add',
            'myGroup',
        ]

        parsedArguments = self.processArguments( inputValue )

        self.assertEqual( [ inputValue[ 1 ] ], parsedArguments.group )
        self.assertEqual( list(), parsedArguments.clusters )


    def processArguments( self, inputValue ) :
        return self.commandUnderTest.parse( inputValue )


    def testAddGroupInGroupShortForm( self ) :
        inputValue = [
            'add',
            'myGroup',
            '-c',
            'myCluster',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], [ inputValue[ 3 ] ] )


    def testAddGroupInGroupLongForm( self ) :
        inputValue = [
            'add',
            'myGroup',
            '--cluster',
            'myCluster',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], [ inputValue[ 3 ] ] )


    def doEmailInGroupTest( self, inputValue, expectedGroup, expectedClusters ) :
        parsedArguments = self.processArguments( inputValue )

        self.assertEqual( expectedGroup, parsedArguments.group )
        self.assertEqual( expectedClusters, parsedArguments.clusters )


    def testAddGroupInGroupsShortForm( self ) :
        expectedList = [ 'cluster1', 'cluster2' ]

        inputValue = [
            'add',
            'myGroup',
            '-c',
            'cluster1',
            'cluster2',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], expectedList )


    def testAddGroupInGroupsLongForm( self ) :
        expectedList = [ 'cluster1', 'cluster2' ]

        inputValue = [
            'add',
            'myGroup',
            '--cluster',
            'cluster1',
            'cluster2',
        ]

        self.doEmailInGroupTest( inputValue, [ inputValue[ 1 ] ], expectedList )


if __name__ == '__main__' :
    unittest.main()
