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
Subcommand graph for `group rm`.
"""

GROUP_ARGUMENT = {
    'names' : [ 'group', ],
    'options' : {
        'help' : 'Group(s) to remove',
        'nargs' : '+',
        'type' : str,
    },
}

CLUSTER_ARGUMENT = {
    'names' : [ '--cluster', '-c', '--clusters' ],
    'options' : {
        'default' : list(),
        'dest' : 'clusters',
        'help' : 'Cluster(s) from which to remove the group',
        'nargs' : '+',
        'type' : str,
    },
}

KEEP_ARGUMENT = {
    'names' : [ '--no-keep', '-n', ],
    'options' : {
        'action' : 'store_false',
        'dest' : 'keep',
        'help' : 'Remove the group itself from contacts when removing from all clusters. Any email addresses unique '
                 'to the group will be lost.',
    },
}

RM_GROUP_SUBCOMMAND_GRAPH = {
    'names' : [ 'rm', ],
    'options' : {
        'dest' : 'remove',
        'help' : 'Remove a group from a selected cluster or clusters, or from all clusters.',
    },
    'specification' : {
        'subcommands' : list(),
        'arguments' : [
            GROUP_ARGUMENT,
            CLUSTER_ARGUMENT,
            KEEP_ARGUMENT,
        ],
    },
}
