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
Manage group properties in a contacts list.
"""

import logging

from contactList.arguments import ContactsOptions

from ..base import \
    ContactData, \
    ContactsOperationError, \
    OperationInterface


log = logging.getLogger( __name__ )


class GroupOperation( OperationInterface ) :
    """
    Manage group properties in a contacts list.
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
        groupCommand = contactsOptions.groupCommand

        (args, kwargs) = self.commands[ groupCommand ][ 'args' ]( contactData, contactsOptions )

        self.commands[ groupCommand ][ 'operation' ]( *args, **kwargs )


def extractAddArguments( contactData: ContactData, contactsOptions: ContactsOptions ) :
    args = [
        contactData,
        contactsOptions.group,
    ]
    kwargs = {
        'clusters' : contactsOptions.clusters,
    }

    return args, kwargs


def extractRemoveArguments( contactData: ContactData, contactsOptions: ContactsOptions ) :
    args = [
        contactData,
        contactsOptions.group,
    ]
    kwargs = {
        'clusters' : contactsOptions.clusters,
    }

    return args, kwargs


def add( contactData: ContactData, groups: list,
         clusters: list = None ) :
    """
    Add a list of groups to one or more clusters. Add to all clusters by specifying an empty cluster list.

    Adding an existing group doesn't change the group, but it will be added to any specified clusters.
    Specify an empty cluster list to create groups without adding them to any clusters.

    :param contactData:
    :param groups: List of groups to add.
    :param clusters: List of clusters to add the new groups to.

    :return: Modified contacts.
    """


    def addGroup( groupName ) :
        nonlocal contactData

        if thisGroup not in contactData.groups :
            contactData.groups[ groupName ] = list()

            log.info( 'Added new group, {0}'.format( groupName ) )


    def addGroupToClusters( groupName ) :
        nonlocal clusters, contactData

        if clusters is None :
            # Add group to all clusters.
            clusters = contactData.clusters.keys()

        addedToClusters = False
        for thisCluster in clusters :
            if thisCluster not in contactData.clusters :
                # Silently create the cluster
                contactData.clusters[ thisCluster ] = list()
                log.info( 'Created new cluster, {0}'.format( thisCluster ) )

            if groupName not in contactData.clusters[ thisCluster ] :
                contactData.clusters[ thisCluster ].append( groupName )

                addedToClusters = True

        if addedToClusters :
            log.info( 'Added group to clusters, {0}, {1}'.format( groupName, clusters ) )


    for thisGroup in groups :
        addGroup( thisGroup )

        addGroupToClusters( thisGroup )

    contactData.validate()

    return contactData


def remove( contactData: ContactData, groups: list,
            clusters: list = None ) :
    """
    Remove a list of groups.

    Exception raised if groups are members of clusters.

    :param contactData:
    :param groups: List of groups to add.
    :param clusters: List of clusters to add the new groups to.

    :return: Modified contacts.
    """


    def checkGroupsAreClusterMembers() :
        """
        Check if the groups are members of any cluster.

        :return: True if the groups are members of any cluster.
        """
        nonlocal contactData, groups

        groupIsMemberOfCluster = list()
        for thisGroup in groups :
            clusterMembers = [ x for x, y in contactData.clusters.items() if thisGroup in y ]

            if clusterMembers :
                log.error( 'Group cannot be removed while it is a member of clusters, {0}, {1}'.format( thisGroup,
                                                                                                        clusterMembers ) )

            groupIsMemberOfCluster.append( bool( clusterMembers ) )

        if any( groupIsMemberOfCluster ) :
            raise ContactsOperationError( 'Remove group(s) from clusters before removing the group(s). Check '
                                          'logging for details.' )


    def modifyClusters( groupName ) :
        nonlocal clusters, contactData

        modifiedCluster = False
        for thisCluster, clusterGroups in contactData.clusters.items() :
            if thisGroup in clusterGroups :
                clusterGroups.remove( thisGroup )
                modifiedCluster = True

        if modifiedCluster :
            log.info( 'Removed group from clusters, {0}, {1}'.format( groupName, clusters ) )


    def removeGroup( groupName ) :
        nonlocal contactData

        if thisGroup in contactData.groups :
            del contactData.groups[ groupName ]
        else :
            log.debug( 'Attempt to remove non-existent group, {0}'.format( thisGroup ) )


    for thisGroup in groups :
        if not clusters :
            checkGroupsAreClusterMembers()
            removeGroup( thisGroup )

            log.info( 'Removed group {0}'.format( thisGroup ) )
        else :
            modifyClusters( thisGroup )

    contactData.validate()

    return contactData
