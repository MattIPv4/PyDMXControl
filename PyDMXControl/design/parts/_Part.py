"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from .._screen import Screen


class Part:

    def __init__(self):
        self._x = 0
        self._y = 0

    def set_pos(self, x: int, y: int):
        self._x = int(x)
        self._y = int(y)

    def design_render(self, screen: Screen):
        pass
