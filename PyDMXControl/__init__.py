"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2019 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
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

# DMXMINWAIT = 0.000001 * 92
DMXMINWAIT = 0.01  # Provides far smoother animation

__title__ = 'PyDMXControl'
__author__ = 'Matt Cowley (MattIPv4)'
__maintainer__ = 'Matt Cowley (MattIPv4)'
__email__ = 'me@mattcowley.co.uk'
__license__ = 'GPLv3'
__copyright__ = 'Copyright (C) 2019 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)'
__version__ = '1.6.2'
__status__ = 'Production'

name = "PyDMXControl"

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=1, minor=6, micro=2, releaselevel='final', serial=0)
