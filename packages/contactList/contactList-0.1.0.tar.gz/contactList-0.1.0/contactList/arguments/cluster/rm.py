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
Subcommand graph for `cluster rm`.
"""

CLUSTER_ARGUMENT = {
    'names' : [ 'cluster', ],
    'options' : {
        'help' : 'Cluster to remove or modify',
        'nargs' : '+',
        'type' : str,
    },
}

GROUP_ARGUMENT = {
    'names' : [ '--group', '-g', '--groups' ],
    'options' : {
        'default' : list(),
        'dest' : 'groups',
        'help' : 'Group to remove from cluster',
        'nargs' : '+',
        'type' : str,
    },
}

RM_CLUSTER_SUBCOMMAND_GRAPH = {
    'names' : [ 'rm', ],
    'options' : {
        'dest' : 'remove',
        'help' : 'Remove a cluster or group from cluster.',
    },
    'specification' : {
        'subcommands' : list(),
        'arguments' : [
            CLUSTER_ARGUMENT,
            GROUP_ARGUMENT,
        ],
    },
}
