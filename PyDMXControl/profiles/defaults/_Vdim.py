"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from datetime import datetime
from typing import Union, Tuple, List

from ._Fixture import Fixture


class Vdim(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__vdims = []
        self.__vdim = 255
        self.__vdimUpdated = datetime.utcnow()

    def _register_channel(self, name: str, *, parked: Union[bool, int] = False, vdim: bool = False) -> int:
        super_call = super()._register_channel(name, parked=parked)
        if super_call == -1:
            return -1

        # Register vdim if applicable
        if vdim:
            self.__vdims.append(super_call)
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
        new_val = super_call[0]
        new_time = super_call[1]
        if apply_vdim and self.get_channel_id(channel) in self.__vdims:
            new_val = int(new_val * (self.__vdim / 255))
            if self.__vdimUpdated > new_time:
                new_time = self.__vdimUpdated

        return new_val, new_time

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
        if not self._valid_channel_value(value, 'vdim'):
            return self
        self.__vdim = value
        self.__vdimUpdated = datetime.utcnow()
        return self

    def get_color(self) -> Union[None, List[int]]:
        red = self.get_channel_value(self.get_channel_id("r"), False)
        green = self.get_channel_value(self.get_channel_id("g"), False)
        blue = self.get_channel_value(self.get_channel_id("b"), False)
        white = self.get_channel_value(self.get_channel_id("w"), False)
        amber = self.get_channel_value(self.get_channel_id("a"), False)
        if red[0] == -1 or green[0] == -1 or blue[0] == -1:
            return None
        color = [red[0], green[0], blue[0]]
        if white[0] != -1:
            color.append(white[0])
            if amber[0] != -1:
                color.append(amber[0])
        return color
