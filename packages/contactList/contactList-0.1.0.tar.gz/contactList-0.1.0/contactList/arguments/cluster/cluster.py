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
Subcommand graph for `cluster`.
"""

from .add import ADD_CLUSTER_SUBCOMMAND_GRAPH
from .rm import RM_CLUSTER_SUBCOMMAND_GRAPH


CLUSTER_SUBCOMMAND_GRAPH = {
    'names' : [ 'cluster', ],
    'specification' : {
        'arguments' : list(),
        'options' : {
            'dest' : 'clusterCommand',
            'help' : 'Add/remove operations',
            'title': 'Cluster management',
        },
        'subcommands' : [
            ADD_CLUSTER_SUBCOMMAND_GRAPH,
            RM_CLUSTER_SUBCOMMAND_GRAPH,
        ],
    },
}
