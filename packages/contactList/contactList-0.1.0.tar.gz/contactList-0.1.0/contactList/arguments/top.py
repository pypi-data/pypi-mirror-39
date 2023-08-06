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
Top level command line argument parsing configuration.
"""

from .base import BadArgument, CommandTree
from .cluster import CLUSTER_SUBCOMMAND_GRAPH
from .email import EMAIL_SUBCOMMAND_GRAPH
from .group import GROUP_SUBCOMMAND_GRAPH


class ContactsOptions :
    """
    Top level command line argument parsing configuration.
    """

    __DEFAULT_FILE = 'contacts.yml'

    __CONTACTSFILE_ARGUMENT_GRAPH = {
        'names' : [ '--file', '-f', ],
        'options' : {
            'default' : __DEFAULT_FILE,
            'dest' : 'contactsFile',
            'help' : 'Contacts file to manage (default ''{0}'')'.format( __DEFAULT_FILE ),
            'type' : str
        }
    }

    __DEBUG_ARGUMENT_GRAPH = {
        'names' : [ '--debug', '-d', ],
        'options' : {
            'action' : 'store_true',
            'help' : 'Enable exception stack trace reporting to command line',
        }
    }

    __CONTACTS_COMMAND_GRAPH = {
        'arguments' : [
            __CONTACTSFILE_ARGUMENT_GRAPH,
            __DEBUG_ARGUMENT_GRAPH,
        ],
        'options' : {
            'dest' : 'activeSubcommand',
        },
        'subcommands' : [
            CLUSTER_SUBCOMMAND_GRAPH,
            EMAIL_SUBCOMMAND_GRAPH,
            GROUP_SUBCOMMAND_GRAPH,
        ],
    }


    def __init__( self ) :
        self.__commandTree = CommandTree( specification = self.__CONTACTS_COMMAND_GRAPH )
        self.__parsedArguments = None


    def parse( self, commandLineArguments: list ) :
        """
        Parse command line arguments.

        :param commandLineArguments:
        :return:
        """
        self.__parsedArguments = self.__commandTree.parse( commandLineArguments )

        if not self.__parsedArguments.activeSubcommand :
            raise BadArgument( 'Must specify a contact list operation' )


    def __getattr__( self, item ) :
        """
        From parsed arguments, recover the items from an `argparse.Namespace` object.

        :param item: parsed argument item name.

        :return: Parsed argument item.
        """
        return getattr( self.__parsedArguments, item )


    @classmethod
    def from_arguments( cls, commandLineArguments: list ) :
        options = cls()

        options.parse( commandLineArguments )

        return options
