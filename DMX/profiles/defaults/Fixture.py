from warnings import warn


class Fixture:

    def __init__(self, start_channel):
        if start_channel < 1 or start_channel > 512:
            raise ValueError('Start Channel must be between 1 and 512.')

        self.__start_channel = start_channel
        self.__channels = []
        self.__id = 0

    def __str__(self):
        return "Fixture of type {} using channels {}->{} ({}).".format(
            self.__class__.__name__,
            self.__start_channel,
            (self.__start_channel + len(self.__channels) - 1),
            len(self.__channels)
        )

    def _register_channel(self, name: str) -> int:
        if self.__start_channel + len(self.__channels) > 512:
            warn('Not enough space in universe for channel `{}`.'.format(name))
            return -1

        used_names = [f['name'] for f in self.__channels]
        if name.lower().strip() in used_names:
            warn('Name `{}` already in use for channel.'.format(name))
            return -1

        self.__channels.append({'name': name, 'value': 0})
        return len(self.__channels) - 1

    def _set_id(self, id: int) -> None:
        self.__id = id

    def _valid_channel_value(self, value: int) -> bool:
        if value < 0 or value > 255:
            warn('DMX value must be between 0 and 255.')
            return False
        return True

    @property
    def id(self):
        return self.__id

    @property
    def channels(self):
        channels = {}
        for i, chan in enumerate(self.__channels):
            channels[self.__start_channel + i] = {'name': chan['name'], 'value': self.get_channel_value(i)}
        return channels

    def __get_channel_id(self, channel: [str, int]) -> int:
        channel = str(channel)

        if channel.isdigit():
            channel = int(channel) - 1
            if channel < len(self.__channels):
                return channel

        for i, chan in enumerate(self.__channels):
            if chan['name'] == str(channel).lower().strip():
                return i

        return -1

    def get_channel_value(self, channel: int) -> int:
        if channel >= len(self.__channels): return -1
        return self.__channels[channel]['value']

    def set_channel(self, channel: [str, int], value: int) -> bool:
        if not self._valid_channel_value(value): return False

        channel = self.__get_channel_id(channel)
        if channel == -1:
            return False

        self.__channels[channel]['value'] = value
        return True

    def set_channels(self, *args, **kwargs) -> None:
        channel = 1
        if 'start' in kwargs and str(kwargs['start']).isdigit() and int(kwargs['start']) > 0: channel = int(
            kwargs['start'])

        def apply_values(values, channel = 1):
            for value in values:
                if value is not None:
                    if isinstance(value, list):
                        channel = apply_values(value, channel)
                    if str(value).isdigit():
                        self.set_channel(channel, int(value))
                channel += 1
            return channel

        apply_values(args)
