import warnings

class Fixture:

    def __init__(self, start_channel):
        if start_channel < 1 or start_channel > 512:
            raise ValueError('Start Channel must be between 1 and 512.')

        self.__start_channel = start_channel
        self.__channels = []
        self.__id = 0

    def _register_channel(self, name: str) -> bool:
        if self.__start_channel + len(self.__channels) > 512:
            warnings.warn('Not enough space in universe for channel `{}`'.format(name))
            return False

        self.__channels.append({'name': name, 'value': 0})
        return True

    def _set_id(self, id: int) -> None:
        self.__id = id

    @property
    def id(self):
        return self.__id

    @property
    def channels(self):
        channels = {}
        for i, chan in enumerate(self.__channels):
            channels[self.__start_channel + i] = chan
        return channels

    def __get_channel(self, channel: [str, int]) -> int:
        if str(channel).isdigit():
            channel = int(channel)-1
            if channel < len(self.__channels):
                return channel
        for i, chan in enumerate(self.__channels):
            if chan['name'] == str(channel).lower().strip():
                return i
        return False

    def set_channel(self, channel: [str, int], value: int) -> bool:
        if value < 0 or value > 255:
            warnings.warn('DMX value for channel `{}` must be between 0 and 255.'.format(channel))
            return False

        channel = self.__get_channel(channel)
        if channel == -1:
            return False

        self.__channels[channel]['value'] = value
        return True

    def set_channels(self, *args, **kwargs) -> None:
        channel = 1
        if 'start' in kwargs and str(kwargs['start']).isdigit() and int(kwargs['start']) > 0: channel = int(kwargs['start'])
        for value in args:
            if str(value).isdigit():
                self.set_channel(channel, int(value))
            channel += 1