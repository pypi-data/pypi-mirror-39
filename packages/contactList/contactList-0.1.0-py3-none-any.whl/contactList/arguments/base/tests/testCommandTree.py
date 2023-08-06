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
Test command tree construction.
"""

import unittest

from ..tree import CommandTree


class TestSingleOptionTree( unittest.TestCase ) :
    """
    Test generating a parse tree for a single optional, top level argument.
    """


    def setUp( self ) :
        self.optionsSpecification = {
            # A single, optional argument
            'arguments' : [
                {
                    'names' : [ '--option' ],
                    'options' : {
                        'default' : 5,
                        'dest' : 'thisOption',
                        'type' : int,
                    },
                },
            ],
            'options' : dict(),
            # No subcommands
            'subcommands' : list(),
        }


    def testDefault( self ) :
        """
        Test that the default value is correctly parsed.
        """
        expectedValue = self.optionsSpecification[ 'arguments' ][ 0 ][ 'options' ][ 'default' ]
        inputValue = list()

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )

        self.assertEqual( expectedValue, parsedArguments.thisOption )
        self.assertTrue( isinstance( parsedArguments.thisOption, int ) )


    def testSpecified( self ) :
        """
        Test that a specified value for the argument is correctly parsed.
        """
        expectedValue = 10
        inputValue = [
            '--option',
            '{0}'.format( expectedValue ),
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )

        self.assertEqual( expectedValue, parsedArguments.thisOption )
        self.assertTrue( isinstance( parsedArguments.thisOption, int ) )


class TestSingleSubcommandTree( unittest.TestCase ) :
    """
    Test a single subcommand with a single optional argument.
    """


    def setUp( self ) :
        self.optionsSpecification = {
            'options' : dict(),
            'subcommands' : [
                {
                    'names' : [ 'subc' ],
                    'specification' : {
                        # A single, optional argument
                        'arguments' : [
                            {
                                'names' : [ '--option' ],
                                'options' : {
                                    'default' : 5,
                                    'dest' : 'thisOption',
                                    'type' : int,
                                },
                            },
                        ],
                        'options' : dict(),
                        # No subcommands of 'subc'
                        'subcommands' : list(),
                    },
                },
            ],
            'arguments' : list(),
        }


    def testDefault( self ) :
        """
        Test that the default value is correctly parsed.
        """
        thisSpecification = self.optionsSpecification[ 'subcommands' ][ 0 ][ 'specification' ]
        expectedValue = thisSpecification[ 'arguments' ][ 0 ][ 'options' ][ 'default' ]
        inputValue = [
            'subc',
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )

        self.assertEqual( expectedValue, parsedArguments.thisOption )
        self.assertTrue( isinstance( parsedArguments.thisOption, int ) )


    def testSpecified( self ) :
        """
        Test that the default value is correctly parsed.
        """
        expectedValue = 10
        inputValue = [
            'subc',
            '--option',
            '{0}'.format( expectedValue ),
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )

        self.assertEqual( expectedValue, parsedArguments.thisOption )
        self.assertTrue( isinstance( parsedArguments.thisOption, int ) )


class TestAliasedSubcommandTree( unittest.TestCase ) :
    """
    Test a single subcommand with a subcommand alias.
    """


    def setUp( self ) :
        self.optionsSpecification = {
            'arguments' : list(),
            'options' : dict(),
            'subcommands' : [
                {
                    'names' : [ 'subc', 'sc' ],
                    'specification' : {
                        # A single, optional argument
                        'arguments' : [
                            {
                                'names' : [ '--option' ],
                                'options' : {
                                    'default' : 5,
                                    'dest' : 'thisOption',
                                    'type' : int,
                                },
                            },
                        ],
                        'options' : dict(),
                        # No subcommands of 'subc'
                        'subcommands' : list(),
                    },
                },
            ],
        }


    def testDefault( self ) :
        """
        Test that the default value is correctly parsed.
        """
        thisSpecification = self.optionsSpecification[ 'subcommands' ][ 0 ][ 'specification' ]
        expectedValue = thisSpecification[ 'arguments' ][ 0 ][ 'options' ][ 'default' ]
        inputValue = [
            'sc',
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )

        self.assertEqual( expectedValue, parsedArguments.thisOption )
        self.assertTrue( isinstance( parsedArguments.thisOption, int ) )


class TestSubcommandDestOption( unittest.TestCase ) :
    """
    Test specifying subcommand options.
    """


    def setUp( self ) :
        self.optionsSpecification = {
            'arguments' : list(),
            'subcommands' : [
                {
                    'names' : [ 'subc' ],
                    'specification' : {
                        # No arguments
                        'arguments' : list(),
                        'options' : {
                            'dest' : 'subcCommand',
                        },
                        # A single subcommand
                        'subcommands' : [
                            {
                                'names' : [ 'subsub' ],
                                'options' : dict(),
                                'specification' : {
                                    'subcommands' : list(),
                                    'arguments' : list(),
                                },
                            },
                        ],
                    },
                },
            ],
        }


    def testDefault( self ) :
        """
        Test that the default value is correctly parsed.
        """
        inputValue = [
            'subc',
            'subsub',
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )

        self.assertEqual( 'subsub', parsedArguments.subcCommand )


class TestMissingParameters( unittest.TestCase ) :
    """
    Missing parameters must be assumed empty.
    """


    def testMissingArguments( self ) :
        """
        No exceptions raised with missing arguments parameter.
        """
        self.optionsSpecification = {
            # arguments missing at this level.
            'subcommands' : [
                {
                    'names' : [ 'subc' ],
                    'specification' : {
                        'arguments' : list(),
                        'options' : dict(),
                        'subcommands' : list(),
                    },
                },
            ],
        }
        inputValue = [
            'subc',
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )


    def testMissingOptions( self ) :
        """
        No exceptions raised with missing options parameter.
        """
        self.optionsSpecification = {
            'arguments' : list(),
            'subcommands' : [
                {
                    'names' : [ 'subc' ],
                    'specification' : {
                        'arguments' : list(),
                        # Missing options at this level.
                        'subcommands' : list(),
                    },
                },
            ],
        }
        inputValue = [
            'subc',
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )


    def testMissingSubcommands( self ) :
        """
        No exceptions raised with missing subcommands parameter.
        """
        self.optionsSpecification = {
            'arguments' : list(),
            'subcommands' : [
                {
                    'names' : [ 'subc' ],
                    'specification' : {
                        'arguments' : list(),
                        'options' : dict(),
                        # Missing subcommands at this level.
                    },
                },
            ],
        }
        inputValue = [
            'subc',
        ]

        thisTree = CommandTree( self.optionsSpecification )
        parsedArguments = thisTree.parse( inputValue )


if __name__ == '__main__' :
    unittest.main()
