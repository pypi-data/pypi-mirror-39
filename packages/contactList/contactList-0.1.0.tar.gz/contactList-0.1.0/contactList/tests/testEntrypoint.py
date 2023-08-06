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
Test flit entrypoint.
"""

import io
import unittest.mock

from .utility import redirect_stdout_stderr

from ..entry import entryPoint

# DO NOT DELETE! Used unittest.mock.patch below
import contactList.entry


class TestEntrypoint( unittest.TestCase ) :

    def testCatchExceptions( self ) :
        """
        Exceptions are caught by the entry point and sys.exit is called.
        """
        with unittest.mock.patch( 'contactList.entry.main' ) as mock_main :
            # Temporarily suppress output from entry point.
            f = io.StringIO()
            with redirect_stdout_stderr( f ) :
                entryPoint()

            mock_main.assert_called_once()


if __name__ == '__main__' :
    unittest.main()
