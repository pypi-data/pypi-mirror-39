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

"""A Python 3 framework for constructing, managing and organising email addresses in YAML format.
"""

import os


here = os.path.dirname( __file__ )

with open( os.path.join( here, 'VERSION' ) ) as versionFile :
    version = versionFile.read()

__version__ = version.strip()

from contactList.contacts.contact import ContactData
