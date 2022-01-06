"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2020 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ..defaults import Fixture, Vdim


class Compact_LED_PAR_4Ch(Vdim):

    def __init__(self, *args, **kwargs):
        """
        These models can be configured to use 4 or 8 DMX channels. Use this
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


class Compact_LED_PAR_8Ch(Fixture):

    def __init__(self, *args, **kwargs):
        """
        These models can be configured to use 4 or 8 DMX channels. Use this
        class for the 8 channel configuration.
        """
        super().__init__(*args, **kwargs)

        self._register_channel('dimmer')
        self._register_channel_aliases('dimmer', 'dim', 'd')
        self._register_channel('red')
        self._register_channel_aliases('red', 'r')
        self._register_channel('green')
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue')
        self._register_channel_aliases('blue', 'b')
        self._register_channel('white')
        self._register_channel_aliases('white', 'w')
        self._register_channel('strobe')
        self._register_channel('function')
        self._register_channel('speed')


class Compact_LED_PAR(Fixture):

    def __init__(self, mode: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if mode == 4:
            new = Compact_LED_PAR_4Ch(*args, **kwargs)
        elif mode == 8:
            new = Compact_LED_PAR_8Ch(*args, **kwargs)
        else:
            raise ValueError('Number of channels (mode) has to be 4 or 8. You passed '
                             '{}.'.format(mode))

        self.__dict__ = new.__dict__
