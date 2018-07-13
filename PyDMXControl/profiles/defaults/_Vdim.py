"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from datetime import datetime
from typing import Union, Tuple

from ._Fixture import Fixture


class Vdim(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__vdims = []
        self.__vdim = 255
        self.__vdimUpdated = datetime.utcnow()

    # noinspection PyMethodOverriding
    def _register_channel(self, name: str, *, vdim: bool = False) -> int:
        super_call = super()._register_channel(name)
        if super_call == -1: return -1

        # Register vdim if applicable
        if vdim: self.__vdims.append(super_call)
        return super_call

    def get_channel_id(self, channel: Union[str, int]) -> int:
        super_call = super().get_channel_id(channel)
        if super_call == -1:
            if channel in ["dimmer", "vdim", "dim", "d"] or channel == str(self.next_channel - 1) or channel == (
                    self.next_channel - 1):
                return self.next_channel - 1
        return super_call

    def get_channel_value(self, channel: Union[str, int], apply_vdim: bool = True) -> Tuple[int, datetime]:
        super_call = super().get_channel_value(channel)
        if super_call[0] == -1:
            channel = str(channel).lower().strip()
            if channel in ["dimmer", "vdim", "dim", "d"] or channel == str(self.next_channel - 1):
                return self.__vdim, self.__vdimUpdated
            return -1, datetime.utcnow()

        # Apply vdim to value if applicable
        newVal = super_call[0]
        newTime = super_call[1]
        if apply_vdim and self.get_channel_id(channel) in self.__vdims:
            newVal = int(newVal * (self.__vdim / 255))
            if self.__vdimUpdated > newTime: newTime = self.__vdimUpdated

        return newVal, newTime

    def set_channel(self, channel: Union[str, int], value: int) -> Fixture:
        # Allow setting of vdim
        if str(channel).lower().strip() in ["dimmer", "vdim", "dim", "d"] or str(channel).lower().strip() == str(
                self.next_channel - 1):
            return self.set_vdim(value)

        # Normal
        super_call = super().set_channel(channel, value)
        return super_call

    def set_vdim(self, value: int) -> Fixture:
        # Update the vdim value
        if not self._valid_channel_value(value): return self
        self.__vdim = value
        self.__vdimUpdated = datetime.utcnow()
        return self
