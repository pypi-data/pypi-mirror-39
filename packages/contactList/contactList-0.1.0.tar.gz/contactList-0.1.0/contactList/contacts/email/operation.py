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
Manage email properties in a contacts list.
"""

import logging

from contactList.arguments import ContactsOptions

from ..base import \
    ContactData, \
    OperationInterface


log = logging.getLogger( __name__ )


class EmailOperation( OperationInterface ) :
    """
    Manage email properties in a contacts list.
    """


    def __init__( self ) :
        self.commands = {
            'add' : {
                'alias': 'add',
                'args' : extractArguments,
                'operation' : add,
            },
            'rm' : {
                'alias':'remove',
                'args' : extractArguments,
                'operation' : remove,
            },
        }


    def applyOperation( self, contactData: ContactData, contactsOptions: ContactsOptions ) :
        """
        Redirect the command line subcommand to the specific requested subcommand to take group related actions on
        contacts data.

        :param contactData:
        :param contactsOptions:
        """
        emailCommand = contactsOptions.emailCommand

        (args, kwargs) = self.commands[ emailCommand ][ 'args' ]( contactData, contactsOptions )

        self.commands[ emailCommand ][ 'operation' ]( *args, **kwargs )


def extractArguments( contactData: ContactData, contactsOptions: ContactsOptions ) :
    args = [
        contactData,
        contactsOptions.email,
    ]
    kwargs = {
        'groups' : contactsOptions.groups,
    }

    return args, kwargs


def add( contactData: ContactData, emails: list,
         groups: list = None ) -> ContactData :
    """
    Add an email to one or more groups. Add to all groups by specifying an empty group list.

    Adding an existing email is ignored.

    :param contactData:
    :param emails: List of emails to be added.
    :param groups: List of groups to add to.

    :return: Modified contacts.
    """
    for thisGroup in contactData.groups :
        if (not groups) or (thisGroup in groups) :
            for thisEmail in emails :
                if thisEmail not in contactData.groups[ thisGroup ]:
                    contactData.groups[ thisGroup ].append( thisEmail )

                log.info( 'Added email to group, {0}, {1}'.format( thisEmail, thisGroup ) )

    contactData.validate()

    return contactData


def remove( contactData: ContactData, emails: list,
            groups: list = None ) -> ContactData :
    """
    Remove an email from one or more groups. Remove from all groups by specifying an empty group list.

    Removing a non-existent email is ignored.

    :param contactData:
    :param emails: List of emails to be added.
    :param groups: List of groups to add to.

    :return: Modified contacts.
    """
    for thisGroup in contactData.groups.keys() :
        if (not groups) or (thisGroup in groups) :
            for thisEmail in emails :
                contactData.groups[ thisGroup ].remove( thisEmail )

                log.info( 'Removed email from group, {0}, {1}'.format( thisEmail, thisGroup ) )

    contactData.validate()

    return contactData
