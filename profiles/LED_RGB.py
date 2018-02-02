from profiles.Fixture import Fixture


class LED_RGB(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('red')
        self._register_channel('green')
        self._register_channel('blue')