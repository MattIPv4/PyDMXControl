"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from typing import List

from ._TransmittingController import TransmittingController


class PrintController(TransmittingController):

    def _transmit(self, frame: List[int], first: int):
        print(first, frame)
