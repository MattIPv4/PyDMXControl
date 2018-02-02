from profiles.Fixture import Fixture


class Generic(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('dimmer')