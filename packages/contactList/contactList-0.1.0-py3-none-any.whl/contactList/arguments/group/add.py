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
Subcommand graph for `group add`.
"""

GROUP_ARGUMENT = {
    'names' : [ 'group', ],
    'options' : {
        'help' : 'Group(s) to add.',
        'nargs' : '+',
        'type' : str,
    },
}

CLUSTER_ARGUMENT = {
    'names' : [ '--cluster', '-c', '--clusters' ],
    'options' : {
        'default' : list(),
        'dest' : 'clusters',
        'help' : 'Cluster to add group to (optional, default all).',
        'nargs' : '+',
        'type' : str,
    },
}

ADD_GROUP_SUBCOMMAND_GRAPH = {
    'names' : [ 'add', ],
    'options' : {
        'help' : 'Add a group to a cluster or clusters, or to all clusters.',
    },
    'specification' : {
        'subcommands' : list(),
        'arguments' : [
            GROUP_ARGUMENT,
            CLUSTER_ARGUMENT,
        ],
    },
}
