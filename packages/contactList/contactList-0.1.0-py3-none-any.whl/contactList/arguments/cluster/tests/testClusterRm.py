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
Test `cluster rm` subcommand.
"""

import unittest

from contactList.arguments.base import CommandTree

from ..rm import RM_CLUSTER_SUBCOMMAND_GRAPH


class TestRmClusterSubcommand( unittest.TestCase ) :
    MOCK_COMMAND_GRAPH = {
        'subcommands' : [
            RM_CLUSTER_SUBCOMMAND_GRAPH,
        ]
    }


    def setUp( self ) :
        self.commandUnderTest = CommandTree( specification = self.MOCK_COMMAND_GRAPH )


    def processArguments( self, inputValue ) :
        return self.commandUnderTest.parse( inputValue )


    def testRemoveCluster( self ) :
        inputValue = [
            'rm',
            'myCluster',
        ]

        parseArguments = self.processArguments( inputValue )

        self.assertEqual( [ inputValue[ 1 ] ], parseArguments.cluster )
        self.assertEqual( list(), parseArguments.groups )


    def testRemoveClusterGroupLongForm( self ) :
        inputValue = [
            'rm',
            'myCluster',
            '--group',
            'myGroup'
        ]

        parseArguments = self.processArguments( inputValue )

        self.assertEqual( [ inputValue[ 1 ] ], parseArguments.cluster )
        self.assertEqual( [ inputValue[ 3 ] ], parseArguments.groups )


    def testRemoveClusterGroupShortForm( self ) :
        inputValue = [
            'rm',
            'myCluster',
            '-g',
            'myGroup'
        ]

        parseArguments = self.processArguments( inputValue )

        self.assertEqual( [ inputValue[ 1 ] ], parseArguments.cluster )
        self.assertEqual( [ inputValue[ 3 ] ], parseArguments.groups )


    def testRemoveClusterGroupPluralForm( self ) :
        inputValue = [
            'rm',
            'myCluster',
            '--groups',
            'myGroup'
        ]

        parseArguments = self.processArguments( inputValue )

        self.assertEqual( [ inputValue[ 1 ] ], parseArguments.cluster )
        self.assertEqual( [ inputValue[ 3 ] ], parseArguments.groups )


if __name__ == '__main__' :
    unittest.main()
