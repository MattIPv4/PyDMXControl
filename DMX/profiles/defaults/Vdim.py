from typing import Union, Tuple
from datetime import datetime

from DMX.profiles.defaults.Fixture import Fixture


class Vdim(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__vdims = []
        self.__vdim = 255
        self.__vdimUpdated = datetime.utcnow()

    def _register_channel(self, name: str, *, vdim: bool = False) -> int:
        super_call = super()._register_channel(name)
        if super_call == -1: return -1

        # Register vdim if applicable
        if vdim: self.__vdims.append(super_call)
        return super_call

    def get_channel_value(self, channel: Union[str, int]) -> Tuple[int, datetime]:
        super_call = super().get_channel_value(channel)
        if super_call[0] == -1:
            channel = str(channel).lower().strip()
            if channel in ["dimmer", "vdim", "dim", "d"] or channel == str(self.next_channel - 1):
                return (self.__vdim, self.__vdimUpdated)
            return (-1, datetime.utcnow())

        # Apply vdim to value if applicable
        newVal = super_call[0]
        newTime = super_call[1]
        if channel in self.__vdims:
            newVal = int(newVal * (self.__vdim / 255))
            if self.__vdimUpdated > newTime: newTime = self.__vdimUpdated

        return (newVal, newTime)

    def set_channel(self, channel: Union[str, int], value: int) -> bool:
        super_call = super().set_channel(channel, value)
        if super_call is True: return True

        # Allow setting of vdim
        channel = str(channel).lower().strip()
        if channel in ["dimmer", "vdim", "dim", "d"] or channel == str(self.next_channel):
            return self.set_vdim(value)

        return False

    def set_vdim(self, value: int) -> bool:
        # Update the vdim value
        if not self._valid_channel_value(value): return False
        self.__vdim = value
        self.__vdimUpdated = datetime.utcnow()
        return True
