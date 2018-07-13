"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""


class LTPCollisionException(Exception):

    def __init__(self, channel_id: int):
        super().__init__("Channel {} has two different values assigned at the same timestamp.".format(channel_id))


class MissingArgumentException(ValueError):

    def __init__(self, argument: str, kwarg: bool = False):
        super().__init__("Argument '{}' ({}) missing from call.".format(
            argument, "Positional" if not kwarg else "Keyword"))
