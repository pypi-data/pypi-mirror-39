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
Define contact management entrypoint.
"""

import sys

from .arguments import ContactsOptions
from .contacts import Contacts


def main( commandLineArguments ) :
    debugMode = False
    try :
        managerOptions = ContactsOptions.from_arguments( commandLineArguments )

        debugMode = managerOptions.debug

        contacts = Contacts.from_yamlFile( filename = managerOptions.contactsFile )

        contacts.applyAction( managerOptions )
        contacts.to_yamlFile( filename = managerOptions.contactsFile )
    except Exception as e :
        if not debugMode :
            print( str( e ), file = sys.stderr )

            # Exit with non-zero status (dirty).
            sys.exit( 1 )
        else :
            raise


def entryPoint() :
    """
    Flit entrypoint. The flit entrypoint must not have any arguments, so here it just calls ``main`` with
    ``sys.argv`` argument.
    """
    main( sys.argv[ 1 : ] )


if __name__ == '__main__' :
    main( sys.argv[ 1 : ] )
