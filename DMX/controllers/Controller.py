from time import sleep
from typing import Type, List, Union, Dict

from DMX.profiles.defaults import Fixture
from .utils.exceptions import LTPCollisionException
from .utils.debug import Debugger
from .utils.timing import DMXMINWAIT, Ticker
from ..profiles.defaults.Fixture import Channel


class Controller:

    def __init__(self, *, ltp=True, dynamic_frame=False):
        # Store all registered fixtures
        self.__fixtures = {}

        # LTP (default) (Latest takes priority, disable for Highest takes priority)
        self.__ltp = ltp

        # Frame data
        self.__frame = []
        self.__dynamic_frame = dynamic_frame

        # Ticker for callback
        self.ticker = Ticker()
        self.ticker.start()

    def add_fixture(self, fixture: Union[Fixture, Type[Fixture]], *args, **kwargs) -> Fixture:
        # Handle auto inserting
        if isinstance(fixture, type):
            fixture = fixture(self.next_channel, *args, **kwargs)

        # Get the next id
        fixture_id = (max(list(self.__fixtures.keys()) or [0])) + 1

        # Tell the fixture its id
        fixture._set_id(fixture_id)

        # Store the fixture
        self.__fixtures[fixture_id] = fixture

        # Return the updated fixture
        return self.__fixtures[fixture_id]

    def del_fixture(self, fixture_id: int) -> bool:
        # Check if the id exists
        if fixture_id in self.__fixtures.keys():
            # Delete the found fixture
            del self.__fixtures[fixture_id]
            # Return it was found
            return True

        # Return it wasn't found
        return False

    def get_fixture(self, fixture_id: int) -> Union[Fixture, None]:
        # Check if the id exists
        if fixture_id in self.__fixtures.keys():
            # Return the found fixture
            return self.__fixtures[fixture_id]

        # Give up
        return None

    def get_fixtures_by_profile(self, profile: Type[Fixture]) -> List[Fixture]:
        matches = []

        # Iterate over each fixture id
        for fixture_id in self.__fixtures.keys():
            # If it matches the given profile
            if isinstance(self.__fixtures[fixture_id], profile):
                # Store
                matches.append(self.__fixtures[fixture_id])

        # Return any matches
        return matches

    def get_fixtures_by_name(self, name: str) -> List[Fixture]:
        matches = []

        # Iterate over each fixture id
        for fixture_id in self.__fixtures.keys():
            # If it matches the given name
            if self.__fixtures[fixture_id].name.lower() == name.lower():
                # Store
                matches.append(self.__fixtures[fixture_id])

        # Return any matches
        return matches

    def get_all_fixtures(self) -> List[Fixture]:
        # Return all the fixtures
        return list(self.__fixtures.values())

    @staticmethod
    def sleep_till_enter() -> None:
        # Hold
        input("Press Enter to end sleep...")

        # We're done
        return None

    @staticmethod
    def sleep_till_interrupt() -> None:
        # Hold
        try:
            while True:
                sleep(DMXMINWAIT)
        except KeyboardInterrupt:
            # We're done
            return None

    def get_frame(self) -> List[int]:
        # Generate frame
        self.__frame = [0] * 512
        if self.__dynamic_frame:
            self.__frame = [0] * (self.next_channel - 1)

        # Get all channels values
        for key, val in self.channels.items():
            # If channel in frame
            if key - 1 < len(self.__frame):
                self.__frame[key - 1] = val[0]

        # Return populated frame
        return self.__frame

    @property
    def channels(self) -> Dict[int, Channel]:
        channels = {}

        # Channels for each registered fixture
        for chans in [v.channels for v in self.__fixtures.values()]:
            # Channels in this fixture
            for chanid, chanval in chans.items():
                chanval = chanval['value']
                if chanval[0] == -1: chanval[0] = 0

                # If channel id already set
                if chanid in channels.keys():
                    if self.__ltp:
                        # Handle collision
                        if chanval[1] == channels[chanid][1] and chanval[0] != channels[chanid][0]:
                            raise LTPCollisionException(chanid)

                        # LTP
                        if chanval[1] > channels[chanid][1]:
                            channels[chanid] = chanval
                    else:
                        # HTP
                        if chanval[0] > channels[chanid][0]:
                            channels[chanid] = chanval
                else:
                    channels[chanid] = chanval

        # Return all the channels
        return channels

    @property
    def next_channel(self) -> int:
        # Get all channels
        channels = list(self.channels.keys())

        # Return next channel
        return max(channels or [0]) + 1

    def all_on(self, milliseconds: int = 0):
        for fixture in self.get_all_fixtures():
            fixture.dim(255, milliseconds)

    def all_off(self, milliseconds: int = 0):
        for fixture in self.get_all_fixtures():
            fixture.dim(0, milliseconds)

    def debug_control(self, callbacks: dict = {}):
        Debugger(self, callbacks).run()

    def run(self, *args, **kwargs):
        # Method used in transmitting controllers
        pass

    def close(self, *args, **kwargs):
        # Stop the ticker
        self.ticker.stop()
        print("CLOSE: ticker stopped")

        return
