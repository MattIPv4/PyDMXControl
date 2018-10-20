"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from time import sleep
from typing import Type, List, Union, Dict, Tuple, Callable

from .utils.debug import Debugger
from .. import Colors
from ..profiles.defaults import Fixture_Channel, Fixture
from ..utils.exceptions import LTPCollisionException
from ..utils.timing import DMXMINWAIT, Ticker
from ..web import WebController


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

        # Web control attr
        self.web = None

    def add_fixture(self, fixture: Union[Fixture, Type[Fixture]], *args, **kwargs) -> Fixture:
        # Handle auto inserting
        if isinstance(fixture, type):
            fixture = fixture(self.next_channel, *args, **kwargs)

        # Get the next id
        fixture_id = (max(list(self.__fixtures.keys()) or [0])) + 1

        # Tell the fixture its id
        fixture.set_id(fixture_id)

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
        for fixture_id in self.__fixtures:
            # If it matches the given profile
            if isinstance(self.__fixtures[fixture_id], profile):
                # Store
                matches.append(self.__fixtures[fixture_id])

        # Return any matches
        return matches

    def get_fixtures_by_name(self, name: str) -> List[Fixture]:
        matches = []

        # Iterate over each fixture id
        for fixture_id in self.__fixtures:
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
    def channels(self) -> Dict[int, Fixture_Channel]:
        channels = {}

        # Channels for each registered fixture
        for chans in [v.channels for v in self.__fixtures.values()]:
            # Channels in this fixture
            for chanid, chanval in chans.items():
                chanval = chanval['value']
                if chanval[0] == -1:
                    chanval[0] = 0

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

    def all_locate(self):
        for fixture in self.get_all_fixtures():
            fixture.locate()

    def all_dim(self, value: int, milliseconds: int = 0):
        for fixture in self.get_all_fixtures():
            fixture.dim(value, milliseconds)

    def all_color(self, color: Union[Colors, List[int], Tuple[int], str], milliseconds: int = 0):
        for fixture in self.get_all_fixtures():
            fixture.color(color, milliseconds)

    def clear_all_effects(self):
        for fixture in self.get_all_fixtures():
            fixture.clear_effects()

    def debug_control(self, callbacks: Dict[str, Callable] = None):
        if callbacks is None:
            callbacks = {}
        Debugger(self, callbacks).run()

    def web_control(self, *args, **kwargs):
        if self.web is not None:
            self.web.stop()
        self.web = WebController(self, *args, **kwargs)

    def run(self):
        # Method used in transmitting controllers
        pass

    def close(self):
        # Stop the ticker
        self.ticker.stop()
        print("CLOSE: ticker stopped")

        # Stop any effect tickers
        for fixture in self.__fixtures.values():
            fixture.clear_effects()
        print("CLOSE: all effects cleared")

        # Stop web
        if hasattr(self, "web"):
            self.web.stop()
            print("CLOSE: web controller stopped")
