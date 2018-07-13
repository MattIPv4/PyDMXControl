from ..defaults import Vdim


class RGB_Vdim(Vdim):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('red', vdim=True)
        self._register_channel_aliases('red', 'r')
        self._register_channel('green', vdim=True)
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue', vdim=True)
        self._register_channel_aliases('blue', 'b')
