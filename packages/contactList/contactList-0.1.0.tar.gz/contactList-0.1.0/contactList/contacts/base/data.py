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
Core representation of contacts data.
"""

import logging

from .exception import ContactsError


log = logging.getLogger( __name__ )


class ContactData :
    """
    Core representation of contacts list.
    """

    __DEFAULT_FILE = 'contacts.yml'
    __KEYS = {
        'cluster' : 'clusters',
        'group' : 'groups',
    }


    def __init__( self ) :
        self.groups = dict()
        self.clusters = dict()


    def emails( self, clusterName ) :
        """
        Aggregate the emails from the named cluster.

        :param clusterName: Cluster name to get emails from.

        :return: set of emails.
        """
        collectedEmails = set()
        for thisGroupName in self.clusters[ clusterName ] :
            collectedEmails |= set( self.groups[ thisGroupName ] )

        return collectedEmails


    def validate( self ) :
        """
        Check that the group and cluster declarations are sane.

        Log errors found and raise ``ContactsError`` on completion of a review with errors.
        """
        groupsOkay = True
        for thisCluster, groups in self.clusters.items() :
            for thisGroup in groups :
                if thisGroup not in self.groups :
                    groupsOkay &= False

                    log.error( 'Group not defined, {0} (cluster, {1})'.format( thisGroup, thisCluster ) )

        if not groupsOkay :
            raise ContactsError( 'Group(s) in cluster not defined' )
