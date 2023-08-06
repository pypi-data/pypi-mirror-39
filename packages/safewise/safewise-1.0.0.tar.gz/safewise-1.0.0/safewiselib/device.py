#
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import warnings

from .transport import enumerate_devices, get_transport


class SafeWISEDevice:
    '''
    This class is deprecated. (There is no reason for it to exist in the first
    place, it is nothing but a collection of two functions.)
    Instead, please use functions from the ``safewiselib.transport`` module.
    '''

    @classmethod
    def enumerate(cls):
        warnings.warn('SafeWISEDevice is deprecated.', DeprecationWarning)
        return enumerate_devices()

    @classmethod
    def find_by_path(cls, path):
        warnings.warn('SafeWISEDevice is deprecated.', DeprecationWarning)
        return get_transport(path, prefix_search=False)
