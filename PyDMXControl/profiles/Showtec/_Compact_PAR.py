"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ..defaults import Fixture


class Compact_PAR_7_Q4(Fixture):

    def __init__(self, n_channels, *args, **kwargs):
        """
        These models can be configured to use 4, 6, or 11 DMX channels, so the number
        of channels has to be supplied when creating the Fixture objects.

        Parameters
        ----------
        n_channels: Number of channel configured in the PAR 7 Q4.
        """
        super().__init__(*args, **kwargs)

        if n_channels == 4:
            self._register_channel('red')
            self._register_channel_aliases('red', 'r')
            self._register_channel('green')
            self._register_channel_aliases('green', 'g')
            self._register_channel('blue')
            self._register_channel_aliases('blue', 'b')
            self._register_channel('white')
            self._register_channel_aliases('white', 'w')

        elif n_channels == 6:
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

        elif n_channels == 11:
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

        else:
            raise ValueError('Number of channels (n_channels) has to be 4, 6, or 11. You passed '
                             '{}.'.format(n_channels))
