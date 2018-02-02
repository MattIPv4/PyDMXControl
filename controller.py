class Controller:

    def __init__(self, *, ltp=False):
        self.__fixtures = {}

        # LTP (default HTP) (Lowest not latest, tracking latest is far too much work)
        self.__ltp = ltp

    def add_fixture(self, fixture):
        fixture_id = (max(list(self.__fixtures.keys()) or [0])) + 1
        fixture._set_id(fixture_id)
        self.__fixtures[fixture_id] = fixture
        return self.__fixtures[fixture_id]

    def del_fixture(self, fixture_id: int) -> bool:
        if fixture_id in self.__fixtures.keys():
            del self.__fixtures[fixture_id]
            return True
        return False

    def get_fixture(self, fixture_id: int):
        if fixture_id in self.__fixtures.keys():
            return self.__fixtures[fixture_id]
        return None

    def get_fixture_by_profile(self, profile) -> list:
        matches = []
        for fixture_id in self.__fixtures.keys():
            if isinstance(self.__fixtures[fixture_id], profile):
                matches.append(self.__fixtures[fixture_id])
        return matches

    @property
    def channels(self):
        channels = {}
        for chans in [v.channels for v in self.__fixtures.values()]:
            for chanid,chanval in chans.items():
                chanval = chanval['value']
                if chanid in channels.keys():
                    if self.__ltp:
                        # LTP
                        if chanval < channels[chanid]:
                            channels[chanid] = chanval
                    else:
                        # HTP
                        if chanval > channels[chanid]:
                            channels[chanid] = chanval
                else:
                    channels[chanid] = chanval
        return channels

    @property
    def next_channel(self):
        channels = list(self.channels.keys())
        return max(channels or [0])+1