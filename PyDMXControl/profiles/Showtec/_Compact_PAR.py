"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ..defaults import Fixture, Vdim


class Compact_PAR_7_Q4_4Ch(Vdim):

    def __init__(self, *args, **kwargs):
        """
        These models can be configured to use 4, 6, or 11 DMX channels. Use this
        class for the 4 channel configuration.
        """
        super().__init__(*args, **kwargs)

        self._register_channel('red', vdim=True)
        self._register_channel_aliases('red', 'r')
        self._register_channel('green', vdim=True)
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue', vdim=True)
        self._register_channel_aliases('blue', 'b')
        self._register_channel('white', vdim=True)
        self._register_channel_aliases('white', 'w')


class Compact_PAR_7_Q4_6Ch(Fixture):

    def __init__(self, *args, **kwargs):
        """
        These models can be configured to use 4, 6, or 11 DMX channels. Use this
        class for the 6 channel configuration.
        """
        super().__init__(*args, **kwargs)

        self._register_channel('dimmer')
        self._register_channel_aliases('dimmer', 'dim', 'd')
        self._register_channel('strobe')
        self._register_channel('red')
        self._register_channel_aliases('red', 'r')
        self._register_channel('green')
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue')
        self._register_channel_aliases('blue', 'b')
        self._register_channel('white')
        self._register_channel_aliases('white', 'w')


class Compact_PAR_7_Q4_11Ch(Fixture):

    def __init__(self, *args, **kwargs):
        """
        These models can be configured to use 4, 6, or 11 DMX channels. Use this
        class for the 11 channel configuration.
        """
        super().__init__(*args, **kwargs)

        self._register_channel('dimmer')
        self._register_channel_aliases('dimmer', 'dim', 'd')
        self._register_channel('strobe')
        self._register_channel('random strobe')
        self._register_channel('color presets')
        self._register_channel('color running')
        self._register_channel('color running speed')
        self._register_channel('sound mode')
        self._register_channel('red')
        self._register_channel_aliases('red', 'r')
        self._register_channel('green')
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue')
        self._register_channel_aliases('blue', 'b')
        self._register_channel('white')
        self._register_channel_aliases('white', 'w')


class Compact_PAR_7_Q4(Fixture):

    def __init__(self, mode: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if mode == 4:
            new = Compact_PAR_7_Q4_4Ch(*args, **kwargs)
        elif mode == 6:
            new = Compact_PAR_7_Q4_6Ch(*args, **kwargs)
        elif mode == 11:
            new = Compact_PAR_7_Q4_11Ch(*args, **kwargs)
        else:
            raise ValueError('Number of channels (mode) has to be 4, 6, or 11. You passed '
                             '{}.'.format(mode))

        self.__dict__ = new.__dict__
