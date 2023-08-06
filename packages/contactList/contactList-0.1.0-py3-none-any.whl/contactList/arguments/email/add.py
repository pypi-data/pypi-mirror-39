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
Subcommand graph for `email add`.
"""

EMAIL_ARGUMENT = {
    'names' : [ 'email', ],
    'options' : {
        'help' : 'Email address(es) to add',
        'nargs' : '+',
        'type' : str,
    },
}

GROUP_ARGUMENT = {
    'names' : [ '--group', '-g', '--groups' ],
    'options' : {
        'default' : list(),
        'dest' : 'groups',
        'help' : 'Group to add email to (optional, default all).',
        'nargs' : '+',
        'type' : str,
    },
}

ADD_EMAIL_SUBCOMMAND_GRAPH = {
    'names' : [ 'add', ],
    'options' : {
        'help' : 'Remove a group from a selected cluster or clusters, or from all clusters.',
    },
    'specification' : {
        'subcommands' : list(),
        'arguments' : [
            EMAIL_ARGUMENT,
            GROUP_ARGUMENT,
        ],
    },
}
