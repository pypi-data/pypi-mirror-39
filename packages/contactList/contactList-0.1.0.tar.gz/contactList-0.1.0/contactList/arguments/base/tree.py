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
Command tree construction.
"""

import argparse
import logging


log = logging.getLogger( __name__ )


class CommandTreeNode :
    """
    Construct a command tree node (command) from a specification dictionary.
    """


    def __init__( self, name, parser,
                  specification = None ) :
        self.specification = specification

        self.name = name
        self.parser = parser
        self.subparsers = None
        self.subcommands = list()

        self.__addArguments()
        self.__addSubcommands()


    def __addArguments( self ) :
        """
        Add arguments to the parser.
        """
        if 'arguments' in self.specification :
            for thisArgument in self.specification[ 'arguments' ] :
                log.debug( 'Adding argument, {0}'.format( thisArgument[ 'names' ][ 0 ] ) )

                self.parser.add_argument( *thisArgument[ 'names' ], **thisArgument[ 'options' ] )


    def __addSubcommands( self ) :
        """
        Add sub-commands to the parser.
        """
        if 'subcommands' in self.specification :
            if self.specification[ 'subcommands' ] :
                if 'options' in self.specification :
                    self.subparsers = self.parser.add_subparsers( **self.specification[ 'options' ] )
                else :
                    self.subparsers = self.parser.add_subparsers()

            for thisSubcommand in self.specification[ 'subcommands' ] :
                thisName = thisSubcommand[ 'names' ][ 0 ]
                thisSpecification = thisSubcommand[ 'specification' ]

                thisAliases = list()
                if len( thisSubcommand[ 'names' ] ) > 1 :
                    thisAliases = thisSubcommand[ 'names' ][ 1 : ]

                thisParser = self.subparsers.add_parser( thisName,
                                                         aliases = thisAliases )

                log.debug( 'Adding subcommand, {0}'.format( thisName ) )

                self.subcommands.append( CommandTreeNode( thisName, thisParser,
                                                          specification = thisSpecification ) )
        else :
            log.debug( 'No subcommands in node' )


class CommandTree( CommandTreeNode ) :
    """
    Construct the command tree from a specification dictionary.
    """


    def __init__( self,
                  specification = None ) :
        parser = argparse.ArgumentParser()

        super().__init__( 'top', parser,
                          specification = specification )


    def parse( self, commandLineArguments: list ) -> argparse.Namespace :
        return self.parser.parse_args( commandLineArguments )
