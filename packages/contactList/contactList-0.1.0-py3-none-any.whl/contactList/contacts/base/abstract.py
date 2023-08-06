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
Abstract interfaces.
"""

import abc

from contactList.arguments import ContactsOptions


class OperationInterface( metaclass = abc.ABCMeta ) :
    """
    Abstract interface to any class performing a command line operation on contact data.
    """

    @abc.abstractmethod
    def applyOperation( self, contactData, contactsOptions: ContactsOptions ) :
        """
        Redirect the command line subcommand to the specific requested subcommand to take action on contacts data.

        :param contactData:
        :param contactsOptions:
        """
        pass
