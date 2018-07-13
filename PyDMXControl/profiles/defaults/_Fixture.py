"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from datetime import datetime
from threading import Thread
from time import sleep, time
from typing import Union, List, Tuple, Type
from warnings import warn

from PyDMXControl import Colors
from PyDMXControl.effects.defaults import Effect


class Channel:

    def __init__(self, name: str):
        self.name = name
        self.value = 0
        self.updated = datetime.utcnow()

    def set_value(self, value: int):
        self.value = value
        self.updated = datetime.utcnow()

    def get_value(self) -> Tuple[int, datetime]:
        return self.value, self.updated


class Fixture:

    def __init__(self, start_channel, *, name: str = ""):
        if start_channel < 1 or start_channel > 512:
            raise ValueError('Start Channel must be between 1 and 512.')

        self.__start_channel = start_channel
        self.__channels = []
        self.__effects = []
        self.__id = 0
        self.__name = name
        self.__channel_aliases = {}

    def __str__(self):
        return "Fixture #{} ('{}') of type {} using channels {}->{} ({}).".format(
            self.id,
            self.name,
            self.__class__.__name__,
            self.__start_channel,
            (self.__start_channel + len(self.__channels) - 1),
            len(self.__channels)
        )

    # Internal

    def _register_channel(self, name: str) -> int:
        if self.__start_channel + len(self.__channels) > 512:
            warn('Not enough space in universe for channel `{}`.'.format(name))
            return -1

        used_names = [f.name for f in self.__channels]
        used_names.extend([f for f in self.__channel_aliases.keys()])
        if name.lower().strip() in used_names:
            warn('Name `{}` already in use for channel (or alias).'.format(name))
            return -1

        self.__channels.append(Channel(name.lower().strip()))
        return len(self.__channels) - 1

    def _register_channel_aliases(self, channel: str, *aliases: str) -> bool:
        if not aliases:
            return False

        channel = channel.lower().strip()

        used_names = [f.name for f in self.__channels]
        if channel not in used_names:
            warn('Channel name `{}` is not registered.'.format(channel))
            return False

        for alias in aliases:
            if alias in self.__channel_aliases.keys():
                warn('Channel alias `{}` already in use for channel `{}`.'.format(alias, self.__channel_aliases[alias]))
                continue
            self.__channel_aliases[alias] = channel
        return True

    def _set_id(self, fixture_id: int) -> None:
        self.__id = fixture_id

    def _set_name(self, name: str) -> None:
        self.__name = name

    # Properties

    @staticmethod
    def _valid_channel_value(value: int) -> bool:
        if value < 0 or value > 255:
            warn('DMX value must be between 0 and 255.')
            return False
        return True

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def next_channel(self) -> int:
        return len(self.__channels) + 1

    @property
    def channels(self) -> dict:
        channels = {}
        for i, chan in enumerate(self.__channels):
            channels[self.__start_channel + i] = {'name': chan.name, 'value': self.get_channel_value(i)}
        return channels

    # Channels

    def get_channel_id(self, channel: Union[str, int]) -> int:
        channel = str(channel)

        if channel.isdigit():
            channel = int(channel)
            if channel < len(self.__channels):
                return channel

        channel = str(channel).lower().strip()
        if channel in self.__channel_aliases.keys():
            channel = self.__channel_aliases[channel]

        for i, chan in enumerate(self.__channels):
            if chan.name == channel:
                return i

        return -1

    def get_channel_value(self, channel: int) -> Tuple[int, datetime]:
        if channel >= len(self.__channels): return -1, datetime.utcnow()
        return self.__channels[channel].get_value()

    def set_channel(self, channel: [str, int], value: int) -> 'Fixture':
        if not self._valid_channel_value(value):
            return self

        channel = self.get_channel_id(channel)
        if channel == -1:
            return self

        self.__channels[channel].set_value(value)
        return self

    def set_channels(self, *args: Union[int, List[int], None], **kwargs) -> 'Fixture':
        channel = 0
        if 'start' in kwargs and str(kwargs['start']).isdigit() and int(kwargs['start']) > 0:
            channel = int(kwargs['start'])

        def apply_values(fixture, values, chan=1):
            for value in values:
                if value is not None:
                    if isinstance(value, list):
                        chan = apply_values(fixture, value, chan)
                    elif str(value).isdigit():
                        fixture.set_channel(chan, int(value))
                        chan += 1
            return chan - 1

        apply_values(self, args, channel)

        return self

    # Effects

    def add_effect(self, effect: Type[Effect], speed: float, *args, **kwargs) -> 'Fixture':
        # Instantiate
        effect = effect(self, speed, *args, **kwargs)
        # Start
        effect.start()
        # Save
        self.__effects.append(effect)

        return self

    def get_effect_by_effect(self, effect: Type[Effect]) -> List[Effect]:
        matches = []

        # Iterate over each effect
        for fx in self.__effects:
            # If it matches the given effect
            if isinstance(fx, effect):
                # Store
                matches.append(fx)

        # Return any matches
        return matches

    def remove_effect(self, effect: Effect) -> 'Fixture':
        if effect in self.__effects:
            effect.stop()
            self.__effects.remove(effect)

        return self

    def clear_effects(self) -> 'Fixture':
        # Stop
        for effect in self.__effects:
            effect.stop()
        # Clear
        self.__effects = []

        return self

    # Helpers

    def __dim(self, current, target, millis, channel):
        start = time() * 1000.0
        gap = target - current

        if millis > 0:
            while (time() * 1000.0) - start <= millis:
                diff = gap * (((time() * 1000.0) - start) / millis)
                self.set_channel(channel, int(current + diff))
                sleep(0.000001)
        self.set_channel(channel, int(target))

        return

    def dim(self, target_value: int, milliseconds: int = 0, channel: Union[str, int] = 'dimmer') -> 'Fixture':

        # Calculate what we need
        current = self.get_channel_value(self.get_channel_id(channel))[0]

        # Create the thread and run loop
        thread = Thread(target=self.__dim, args=(current, target_value, milliseconds, channel))
        thread.daemon = True
        thread.start()

        return self

    def anim(self, milliseconds: int, *channels_values: Tuple[Union[str, int], int]):
        for channel_value in channels_values:
            self.dim(channel_value[1], milliseconds, channel_value[0])

    def color(self, color: Union[Colors, List[int], Tuple[int], str], milliseconds: int = 0):
        # Handle string color names
        if type(color) is str:
            if color in Colors:
                color = Colors[color]
            else:
                raise ValueError("Color '" + color + "' not defined in Colors enum."
                                                     " Supply valid Colors enum or List/Tuple of integers.")

        # Get a tuple
        color = Colors.to_tuples(color)

        # Apply
        self.anim(milliseconds, *color)

    def locate(self):
        self.color([255, 255, 255, 255, 255])
        self.dim(255)
