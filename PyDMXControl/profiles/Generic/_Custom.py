"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ..defaults import Fixture


class Custom(Fixture):

    def __init__(self, *args, **kwargs):
        if "channels" not in kwargs:
            raise TypeError("__init__() missing 1 required keyword-only argument: 'channels'")

        super().__init__(*args, **kwargs)

        for _ in range(kwargs["channels"]):
            self._register_channel(str(_ + 1))
