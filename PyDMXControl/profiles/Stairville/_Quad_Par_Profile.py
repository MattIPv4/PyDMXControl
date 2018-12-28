"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from warnings import warn

from ..defaults import Fixture, Vdim


class Quad_Par_Profile_4(Vdim):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('red', vdim=True)
        self._register_channel_aliases('red', 'r')
        self._register_channel('green', vdim=True)
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue', vdim=True)
        self._register_channel_aliases('blue', 'b')
        self._register_channel('white', vdim=True)
        self._register_channel_aliases('white', 'w')


class Quad_Par_Profile_6(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('red')
        self._register_channel_aliases('red', 'r')
        self._register_channel('green')
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue')
        self._register_channel_aliases('blue', 'b')
        self._register_channel('white')
        self._register_channel_aliases('white', 'w')
        self._register_channel('strobe')
        self._register_channel('dimmer')
        self._register_channel_aliases('dimmer', 'dim', 'd')


class Quad_Par_Profile_8(Fixture):

    def __init__(self, *args, **kwargs):
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
        self._register_channel('mode')
        self._register_channel('function')
        self._register_channel('strobe')


class Quad_Par_Profile(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        modes = [4, 6, 8]
        if 'mode' not in kwargs or kwargs['mode'] not in modes:
            kwargs['mode'] = modes[-1]
            warn('No/invalid mode keyword argument given, default mode {} applied.'.format(kwargs['mode']))

        if kwargs['mode'] == 4:
            new = Quad_Par_Profile_4(*args, **kwargs)
        elif kwargs['mode'] == 6:
            new = Quad_Par_Profile_6(*args, **kwargs)
        else:
            new = Quad_Par_Profile_8(*args, **kwargs)

        self.__dict__ = new.__dict__
