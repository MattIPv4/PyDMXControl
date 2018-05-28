from datetime import datetime
from threading import Thread
from time import sleep
from time import time
from typing import Union, List, Tuple
from warnings import warn


class Channel:

    def __init__(self, name: str):
        self.name = name
        self.value = 0
        self.updated = datetime.utcnow()

    def set_value(self, value: int):
        self.value = value
        self.updated = datetime.utcnow()

    def get_value(self) -> Tuple[int, datetime]:
        return (self.value, self.updated)


class Fixture:

    def __init__(self, start_channel, *, name: str = ""):
        if start_channel < 1 or start_channel > 512:
            raise ValueError('Start Channel must be between 1 and 512.')

        self.__start_channel = start_channel
        self.__channels = []
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

    def _set_id(self, id: int) -> None:
        self.__id = id

    def _set_name(self, name: str) -> None:
        self.__name = name

    def _valid_channel_value(self, value: int) -> bool:
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
            channels[self.__start_channel + i] = {'name': chan.name, 'value': chan.get_value()}
        return channels

    def _get_channel_id(self, channel: Union[str, int]) -> int:
        channel = str(channel)

        if channel.isdigit():
            channel = int(channel) - 1
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
        if channel >= len(self.__channels): return (-1, datetime.utcnow())
        return self.__channels[channel].get_value()

    def set_channel(self, channel: [str, int], value: int) -> 'Fixture':
        if not self._valid_channel_value(value):
            return self

        channel = self._get_channel_id(channel)
        if channel == -1:
            return self

        self.__channels[channel].set_value(value)
        return self

    def set_channels(self, *args: Union[int, List[int], None], **kwargs) -> 'Fixture':
        channel = 1
        if 'start' in kwargs and str(kwargs['start']).isdigit() and int(kwargs['start']) > 0:
            channel = int(kwargs['start'])

        def apply_values(self, values, channel=1):
            for value in values:
                if value is not None:
                    if isinstance(value, list):
                        channel = apply_values(self, value, channel)
                    elif str(value).isdigit():
                        self.set_channel(channel, int(value))
                channel += 1
            return channel - 1

        apply_values(self, args, channel)

        return self

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

    def dim(self, target_value: int, milliseconds: int, channel: Union[str, int] = 'dimmer') -> 'Fixture':

        # Calculate what we need
        current = self.get_channel_value(self._get_channel_id(channel))[0]

        # Create the thread and run loop
        thread = Thread(target=self.__dim, args=(current, target_value, milliseconds, channel))
        thread.daemon = True
        thread.start()

        return self

    def anim(self, milliseconds: int, *channels_values: Tuple[Union[str, int], int]):
        for channel_value in channels_values:
            self.dim(channel_value[1], milliseconds, channel_value[0])
