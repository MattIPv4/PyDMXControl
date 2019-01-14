"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
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

import glob
import os.path
from importlib.machinery import SourceFileLoader
from typing import Union, Tuple, List

dir_path = os.path.dirname(os.path.realpath(__file__))


def load(name: str) -> Union[Tuple[str, str, List[List[int]]], None]:
    full = "{}/{}.data.py".format(dir_path, name)
    if not os.path.isfile(full):
        return None
    try:
        module = SourceFileLoader(name, full).load_module()
    except:
        return None
    return module.name1, module.name2, module.points


def generate():
    import xml.etree.ElementTree as ET
    import string

    printable = set(string.printable)
    files = glob.glob("/Applications/LXSeries/LXFree.app/Contents/Resources/keys/*.lxkey")

    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        for fixture in root.findall("kentry"):
            try:
                # Get names
                name = fixture.find("fname").text
                full_name = fixture.find("name").text

                # Get points to numbers
                raw_points = fixture.find("custom").find("symbol").find("points")
                parsed_points = []
                for point in raw_points:
                    parsed_points.append([
                        float(point.find("x").text),
                        float(point.find("y").text),
                        int(point.find("op").text)
                    ])

                # Find the smallest x/y (often negative)
                minx = min([f[0] for f in parsed_points])
                minx = minx * -1 if minx < 0 else 0
                miny = min([f[1] for f in parsed_points])
                miny = miny * -1 if miny < 0 else 0

                # Force all points to be positive
                parsed_points = [[f[0] + minx, f[1] + miny, f[2]] for f in parsed_points]

                # Scale to reduce likelihood of decimal point and then make int
                parsed_points = [[f[0] * 4, f[1] * 4, f[2]] for f in parsed_points]
                parsed_points = [[int(f[0]), int(f[1]), f[2]] for f in parsed_points]

                # Output
                lines = [
                    "name1 = \"{}\"".format(name),
                    "name2 = \"{}\"".format(full_name),
                    "points = {}".format(parsed_points)
                ]
                file = name.replace(" ", "_").replace(".", "").replace("/", "") \
                       + "_" + full_name.replace(" ", "_").replace(".", "").replace("/", "")
                file = ''.join(filter(lambda x: x in printable, file))
                with open("{}/{}.data.py".format(dir_path, file), "w") as f:
                    f.write("\n".join(lines))
            except:
                pass
