"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
 *
 *  This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published
 *   by the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *  This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *  You should have received a copy of the GNU General Public License
 *   along with this program. If not, please see
 *   <https://github.com/MattIPv4/PyDMXControl/blob/master/LICENSE> or <http://www.gnu.org/licenses/>.
"""

from collections import namedtuple

from ._Colors import Colors

__title__ = 'PyDMXControl'
__author__ = 'Matt Cowley (MattIPv4)'
__maintainer__ = 'Matt Cowley (MattIPv4)'
__email__ = 'me@mattcowley.co.uk'
__license__ = 'GPL'
__copyright__ = 'Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)'
__version__ = '1.4.4'
__status__ = 'Production'

name = "PyDMXControl"

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=1, minor=4, micro=4, releaselevel='final', serial=0)
