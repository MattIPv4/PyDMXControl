"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2023 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from datetime import datetime
from typing import Union, Tuple, List

from ._Fixture import Fixture


class Vdim(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__vdims = []
        self.__vdim = 255
        self.__vdim_timestamp = datetime.utcnow()
        self.__vdim_parked = False

    def __vdim_updated(self):
        self.__vdim_timestamp = datetime.utcnow()

    def _register_channel(self, name: str, *, parked: Union[bool, int] = False, vdim: bool = False) -> int:
        super_call = super()._register_channel(name, parked=parked)

        # Register vdim if applicable
        if vdim:
            self.__vdims.append(super_call)

        return super_call

    def __is_vdim_channel(self, channel: Union[str, int]) -> bool:
        return str(channel).lower().strip() in ["dimmer", "vdim", "dim", "d"] \
               or str(channel) == str(self.next_channel - 1)

    def get_channel_id(self, channel: Union[str, int]) -> int:
        # Look for vdim channel
        if self.__is_vdim_channel(channel):
            return self.next_channel - 1

        # Get normal channel
        return super().get_channel_id(channel)

    def get_channel_value(self, channel: Union[str, int], apply_vdim: bool = True, apply_parking: bool = True) -> Tuple[int, datetime]:
        # Look for vdim channel
        if self.__is_vdim_channel(channel):
            return (self.__vdim if (not apply_parking) or (self.__vdim_parked is False) else self.__vdim_parked), self.__vdim_timestamp

        # Get normal channel
        super_call = super().get_channel_value(channel, apply_parking)
        new_val = super_call[0]
        new_time = super_call[1]

        # Apply vdim if applicable
        if apply_vdim and self.get_channel_id(channel) in self.__vdims:
            new_val = int(new_val * (self.__vdim / 255))
            if self.__vdim_timestamp > new_time:
                new_time = self.__vdim_timestamp

        return new_val, new_time

    def set_channel(self, channel: Union[str, int], value: int) -> Fixture:
        # Allow setting of vdim
        if self.__is_vdim_channel(channel):
            return self.set_vdim(value)

        # Set normal channel
        return super().set_channel(channel, value)

    def set_vdim(self, value: int) -> Fixture:
        # Update the vdim value
        if not self._valid_channel_value(value, 'vdim'):
            return self
        self.__vdim = value

        # If not parked, bump the timestamp
        if self.__vdim_parked is False:
            self.__vdim_updated()

        return self

    def get_color(self) -> Union[None, List[int]]:
        if not self.has_channel('r') or not self.has_channel('g') or not self.has_channel('b'):
            return None

        color = [
            self.get_channel_value('r', False, False)[0],
            self.get_channel_value('g', False, False)[0],
            self.get_channel_value('b', False, False)[0],
        ]

        if self.has_channel('w'):
            color.append(self.get_channel_value('w', False, False)[0])

            if self.has_channel('a'):
                color.append(self.get_channel_value('a', False, False)[0])

        return color

    def park(self) -> Fixture:
        self.__vdim_parked = self.__vdim
        self.__vdim_updated()

        return super().park()

    def unpark(self) -> Fixture:
        if self.__vdim_parked is not False:
            self.__vdim_parked = False
            self.__vdim_updated()

        return super().unpark()
