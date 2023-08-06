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
Manage cluster properties in a contacts list.
"""

import logging

from contactList.arguments import ContactsOptions

from ..base import \
    ContactData, \
    OperationInterface


log = logging.getLogger( __name__ )


class ClusterOperation( OperationInterface ) :
    """
    Manage cluster properties in a contacts list.
    """


    def __init__( self ) :
        self.commands = {
            'add' : {
                'args' : extractAddArguments,
                'operation' : add,
            },
            'rm' : {
                'args' : extractRemoveArguments,
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
        emailCommand = contactsOptions.clusterCommand

        (args, kwargs) = self.commands[ emailCommand ][ 'args' ]( contactData, contactsOptions )

        self.commands[ emailCommand ][ 'operation' ]( *args, **kwargs )


def extractAddArguments( contactData: ContactData, contactsOptions: ContactsOptions ) :
    args = [
        contactData,
        contactsOptions.cluster,
    ]
    kwargs = dict()

    return args, kwargs


def extractRemoveArguments( contactData: ContactData, contactsOptions: ContactsOptions ) :
    args = [
        contactData,
        contactsOptions.cluster,
    ]
    kwargs = {
        'groups' : contactsOptions.groups,
    }

    return args, kwargs


def add( contactData: ContactData, clusters: list ) -> ContactData :
    """
    Add groups to specified clusters. If groups is ``None`` then add the cluster.

    Attempting to add an existing cluster is silently ignored, and the existing cluster is unmodified.

    :param contactData:
    :param clusters: List of cluster names to add groups to.

    :return: Modified contacts.
    """
    for thisCluster in clusters :
        if thisCluster not in contactData.clusters :
            contactData.clusters[ thisCluster ] = list()

            log.info( 'Added new cluster, {0}'.format( thisCluster ) )
        else :
            # Warn the user that this is being ignored.
            log.warning( 'Cannot add a cluster that already exists, {0}'.format( thisCluster ) )

    contactData.validate()

    return contactData


def remove( contactData: ContactData, clusters: list,
            groups: list = None ) -> ContactData :
    """
    Remove groups from specified clusters. If groups is ``None`` then remove the cluster.

    Removing a non-existent cluster is silently ignored.

    :param contactData:
    :param clusters: List of cluster names to remove.
    :param groups: List of group names to remove.

    :return: Modified contacts.
    """


    def removeCluster( clusterName ) :
        """
        Remove cluster from contacts data.

        :param clusterName:
        """
        nonlocal contactData

        if thisCluster in contactData.clusters :
            del contactData.clusters[ clusterName ]

            log.info( 'Removed cluster, {0}'.format( clusterName ) )
        else :
            log.warning( 'Cannot remove a cluster that does not exist, {0}'.format( clusterName ) )


    def removeGroupsFromCluster( clusterName, groupList ) :
        nonlocal contactData

        removedFromGroups = False
        for thisGroup in groupList :
            if thisGroup in contactData.clusters[ clusterName ] :
                contactData.clusters[ clusterName ].remove( thisGroup )

                removedFromGroups = True

        if removedFromGroups:
            log.info( 'Removed group(s) from cluster, {0}, {1}'.format( clusterName, groupList ) )


    for thisCluster in clusters :
        if not groups :
            removeCluster( thisCluster )
        else :
            removeGroupsFromCluster( thisCluster, groups )

    contactData.validate()

    return contactData
