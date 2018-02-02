from typing import TypeVar
T = TypeVar('T')


class Controller:

    def __init__(self):
        self.fixtures = {}

    def add_fixture(self, fixture: T) -> T:
        fixture_id = (max(list(self.fixtures.keys()) or [0])) + 1
        fixture._set_id(fixture_id)
        self.fixtures[fixture_id] = fixture
        return self.fixtures[fixture_id]

    def del_fixture(self, fixture_id: int) -> bool:
        if fixture_id in self.fixtures.keys():
            del self.fixtures[fixture_id]
            return True
        return False

    @property
    def channels(self):
        channels = {}
        for chans in [v.channels for v in self.fixtures.values()]:
            for chanid,chanval in chans.items():
                channels[chanid] = chanval['value']
        return channels

    @property
    def next_channel(self):
        channels = list(self.channels.keys())
        return max(channels or [0])+1