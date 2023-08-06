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
Utilities to support tests.
"""

import sys
from contextlib import contextmanager


# Use a context manager to temporarily suppress spurious output from argparse.
# https://stackoverflow.com/questions/29935283/how-to-set-custom-output-handlers-for-argparse-in-python
@contextmanager
def redirect_stdout_stderr( stream ) :
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stream
    sys.stderr = stream
    try :
        yield
    finally :
        sys.stdout = old_stdout
        sys.stderr = old_stderr
