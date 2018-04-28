from DMX.profiles.defaults.Fixture import Fixture


class Vdim(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__vdims = []
        self.__vdim = 255

    def _register_channel(self, name: str, *, vdim: bool = False) -> int:
        super_call = super()._register_channel(name)
        if super_call == -1: return -1

        # Register vdim if applicable
        if vdim: self.__vdims.append(super_call)
        return super_call

    def get_channel_value(self, channel: int) -> int:
        super_call = super().get_channel_value(channel)
        if super_call == -1: return -1

        # Apply vdim to value if applicable
        if channel in self.__vdims: super_call = super_call * (self.__vdim / 255)
        return int(super_call)

    def set_channel(self, channel: [str, int], value: int) -> bool:
        super_call = super().set_channel(channel, value)
        if super_call is True: return True

        # Allow setting of vdim
        channel = str(channel).lower().strip()
        if channel == "dimmer" or channel == "vdim" or channel == str(len(self.channels) + 1):
            return self.set_vdim(value)

        return False

    def set_vdim(self, value: int) -> bool:
        # Update the vdim value
        if not self._valid_channel_value(value): return False
        self.__vdim = value
        return True
