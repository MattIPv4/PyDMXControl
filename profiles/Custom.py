from profiles.defaults.Fixture import Fixture


class Custom(Fixture):

    def __init__(self, *args, **kwargs):
        chans = args[0]
        args = args[1:]
        super().__init__(*args, **kwargs)

        for _ in range(chans):
            self._register_channel(str(_+1))