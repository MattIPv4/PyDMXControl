"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2023 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

import re
from datetime import datetime
from time import sleep, time
from typing import Union, List, Tuple, Type
from warnings import warn

from ... import Colors
from ...effects.defaults import Effect
from ...utils.exceptions import FixtureCreationException, JSONConfigSaveException, ChannelNotFoundException


class Channel:

    def __init__(self, name: str, parked: Union[bool, int]):
        self.name = name
        self.__value = 0
        self.__timestamp = datetime.utcnow()
        self.__parked = parked if parked is False else (0 if parked is True else parked)

    def __updated(self):
        self.__timestamp = datetime.utcnow()

    def set(self, value: int):
        self.__value = value
        if self.parked is False:
            self.__updated()

    @property
    def value(self) -> Tuple[int, datetime]:
        return (self.__value if self.__parked is False else self.__parked), self.__timestamp

    @property
    def value_unparked(self) -> Tuple[int, datetime]:
        return self.__value, self.__timestamp

    @property
    def parked(self) -> bool:
        return self.__parked is not False

    def park(self, value: int = 0):
        self.__parked = value
        self.__updated()

    def unpark(self):
        if self.__parked is not False:
            self.__parked = False
            self.__updated()


class FixtureHelpers:

    # Store the callbacks
    __callbacks = []

    def dim(self, target_value: int, milliseconds: int = 0, channel: Union[str, int] = 'dimmer') -> 'Fixture':
        # Handle instant edge-case
        millis = max(milliseconds, 0)
        if millis == 0:
            self.set_channel(channel, int(target_value))
            return self

        # Calculate what we need
        current = self.get_channel_value(self.get_channel_id(channel))[0]
        start = time() * 1000.0
        gap = target_value - current

        # Create the callback for ticker
        def callback():
            if (time() * 1000.0) - start <= millis:
                diff = gap * (((time() * 1000.0) - start) / millis)
                self.set_channel(channel, int(current + diff))
            else:
                self.set_channel(channel, int(target_value))
                self.controller.ticker.remove_callback(callback)
                self.__callbacks.remove(callback)

        # Append to the tracking list
        self.__callbacks.append(callback)

        # Start the callback
        self.controller.ticker.add_callback(callback, 0)

        return self

    def anim(self, milliseconds: int, *channels_values: Tuple[Union[str, int], int]):
        for channel_value in channels_values:
            self.dim(channel_value[1], milliseconds, channel_value[0])

    def color(self, color: Union[Colors, List[int], Tuple[int], str], milliseconds: int = 0):
        # Handle string color names
        if isinstance(color, str):
            if color in Colors.__members__:
                color = Colors[color]
            else:
                raise ValueError("Color '" + color + "' not defined in Colors enum."
                                                     " Supply valid Colors enum or List/Tuple of integers.")

        # Get a tuple
        color = [f for f in Colors.to_tuples(color) if self.has_channel(f[0])]

        # Apply
        self.anim(milliseconds, *color)

    def get_color(self) -> Union[None, List[int]]:
        if not self.has_channel('r') or not self.has_channel('g') or not self.has_channel('b'):
            return None

        color = [
            self.get_channel_value('r', False)[0],
            self.get_channel_value('g', False)[0],
            self.get_channel_value('b', False)[0]
        ]

        if self.has_channel('w'):
            color.append(self.get_channel_value('w', False)[0])

            if self.has_channel('a'):
                color.append(self.get_channel_value('a', False)[0])

        return color

    def on(self):
        self.dim(255)

    def off(self):
        self.dim(0)

    def locate(self):
        self.color([255, 255, 255, 255, 255])
        self.dim(255)

    def clear_callbacks(self):
        for callback in self.__callbacks:
            self.controller.ticker.remove_callback(callback)
        self.__callbacks = []
            


class Fixture(FixtureHelpers):

    def __init__(self, *args, **kwargs):
        if "start_channel" not in kwargs:
            raise TypeError("__init__() missing 1 required keyword-only argument: 'start_channel'")

        if kwargs["start_channel"] < 1 or kwargs["start_channel"] > 512:
            raise ValueError('Start Channel must be between 1 and 512.')

        if "name" not in kwargs:
            kwargs["name"] = ""

        self.__start_channel = kwargs["start_channel"]
        self.__channels = []
        self.__effects = []
        self.__id = None
        self.__controller = None
        self.__name = kwargs["name"]
        self.__channel_aliases = {}
        self.__kwargs = kwargs
        self.__args = args

    def __str__(self):
        return self.title

    # Internal

    def _register_channel(self, name: str, *, parked: Union[bool, int] = False) -> int:
        if self.__start_channel + len(self.__channels) > 512:
            raise FixtureCreationException(self, 'Not enough space in universe for channel `{}`.'.format(name))

        used_names = [f.name for f in self.__channels]
        used_names.extend([f for f in self.__channel_aliases])
        if name.lower().strip() in used_names:
            raise FixtureCreationException(self, 'Name `{}` already in use for channel (or alias).'.format(name))

        self.__channels.append(Channel(name.lower().strip(), parked))
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

    def set_id(self, fixture_id: int):
        # Only ever set once
        if self.__id is None:
            self.__id = fixture_id

    def set_controller(self, controller: 'Controller'):
        # Only ever set once
        if self.__controller is None:
            self.__controller = controller

    def _set_name(self, name: str):
        self.__name = name

    # Properties

    def _valid_channel_value(self, value: int, channel: Union[str, int]) -> bool:
        if value < 0 or value > 255:
            if self.__controller.dmx_value_warnings:
                warn('{} DMX value must be between 0 and 255. Received value {} for channel {}'.format(
                    self.title, value, channel))
            return False
        return True

    @property
    def id(self) -> int:
        return self.__id if self.__id is not None else 0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def start_channel(self) -> int:
        return self.__start_channel

    @property
    def next_channel(self) -> int:
        return len(self.__channels) + 1

    @property
    def parked(self) -> bool:
        for chan in self.__channels:
            if chan.parked:
                return True
        return False

    @property
    def controller(self) -> 'Controller':
        return self.__controller

    @property
    def channels(self) -> dict:
        channels = {}
        for i, chan in enumerate(self.__channels):
            channels[self.start_channel + i] = {'name': chan.name, 'value': self.get_channel_value(i)}
        return channels

    @property
    def channel_usage(self) -> str:
        return "{}->{} ({})".format(
            self.start_channel,
            (self.start_channel + len(self.__channels) - 1),
            len(self.__channels)
        )

    @property
    def title(self) -> str:
        return "Fixture #{} {} of type {} using channels {}.".format(
            self.id,
            "('{}')".format(self.name) if self.name else "",
            self.__class__.__name__,
            self.channel_usage
        )

    @property
    def json_data(self) -> dict:
        pattern = re.compile(r"^PyDMXControl\.profiles\.(([\w\d.]+)\.)*_[\w\d]+$", re.IGNORECASE)
        match = pattern.match(self.__class__.__module__)
        if not match:
            raise JSONConfigSaveException(self.id)
        base = {
            "type": "{}.{}".format(match.group(2), self.__class__.__name__),
            "args": self.__args
        }
        for kwarg, val in self.__kwargs.items():
            if kwarg not in base:
                if kwarg == "name":
                    val = self.name
                base[kwarg] = val
        return base

    # Channels

    def get_channel_id(self, channel: Union[str, int]) -> int:
        channel = str(channel)

        if channel.isdigit():
            channel_int = int(channel)
            if channel_int < len(self.__channels):
                return channel_int

        channel = channel.lower().strip()
        if channel in self.__channel_aliases.keys():
            channel = self.__channel_aliases[channel]

        for i, chan in enumerate(self.__channels):
            if chan.name == channel:
                return i

        raise ChannelNotFoundException(channel, self.id)

    def has_channel(self, channel: Union[str, int]) -> bool:
        try:
            self.get_channel_id(channel)
            return True
        except ChannelNotFoundException:
            return False

    def get_channel_value(self, channel: Union[str, int], apply_parking: bool = True) -> Tuple[int, datetime]:
        if not apply_parking:
            return self.__channels[self.get_channel_id(channel)].value_unparked
        return self.__channels[self.get_channel_id(channel)].value

    def set_channel(self, channel: Union[str, int], value: int) -> 'Fixture':
        if not self._valid_channel_value(value, channel):
            return self

        self.__channels[self.get_channel_id(channel)].set(value)
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

    # Parking

    def park(self) -> 'Fixture':
        for chan in self.__channels:
            chan.park(chan.value[0])

        return self

    def unpark(self) -> 'Fixture':
        for chan in self.__channels:
            chan.unpark()

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
        for this_effect in self.__effects:
            # If it matches the given effect
            if isinstance(this_effect, effect):
                # Store
                matches.append(this_effect)

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
