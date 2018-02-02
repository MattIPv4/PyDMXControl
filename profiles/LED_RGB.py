from profiles.defaults.Vdim import Vdim


class LED_RGB(Vdim):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('red', vdim=True)
        self._register_channel('green', vdim=True)
        self._register_channel('blue', vdim=True)