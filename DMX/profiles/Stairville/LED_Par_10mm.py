from DMX.profiles.defaults.Fixture import Fixture


class Stairville_LED_Par_10mm(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('red')
        self._register_channel('green')
        self._register_channel('blue')
        self._register_channel('macro')
        self._register_channel('speed/strobe')
        self._register_channel('mode')
        self._register_channel('dimmer')