"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

import re
from importlib import import_module
from json import load, dumps, JSONDecodeError
from time import sleep
from typing import Type, List, Union, Dict, Tuple, Callable
from warnings import warn

from .utils.debug import Debugger
from .. import Colors, name, DMXMINWAIT
from ..profiles.defaults import Fixture_Channel, Fixture
from ..utils.exceptions import JSONConfigLoadException, LTPCollisionException
from ..utils.timing import Ticker
from ..web import WebController


class ControllerHelpers:

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


class Controller(ControllerHelpers):

    def __init__(self, *, ltp: bool = True, dynamic_frame: bool = False, suppress_dmx_value_warnings: bool = False):
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

        # JSON load/save
        self.json = JSONLoadSave(self)

        # Warning data
        self.dmx_value_warnings = not suppress_dmx_value_warnings

    def add_fixture(self, fixture: Union[Fixture, Type[Fixture]], *args, **kwargs) -> Fixture:
        # Handle auto inserting
        if isinstance(fixture, type):
            if "start_channel" not in kwargs:
                kwargs["start_channel"] = self.next_channel
            fixture = fixture(*args, **kwargs)

        # Get the next id
        fixture_id = (max(list(self.__fixtures.keys()) or [0])) + 1

        # Tell the fixture its id
        fixture.set_id(fixture_id)

        # Give the fixture this controller
        fixture.set_controller(self)

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

    def get_fixtures_by_name(self, fixture_name: str) -> List[Fixture]:
        matches = []

        # Iterate over each fixture id
        for fixture_id in self.__fixtures:
            # If it matches the given name
            if self.__fixtures[fixture_id].name.lower() == fixture_name.lower():
                # Store
                matches.append(self.__fixtures[fixture_id])

        # Return any matches
        return matches

    def get_all_fixtures(self) -> List[Fixture]:
        # Return all the fixtures
        return list(self.__fixtures.values())

    @staticmethod
    def sleep_till_enter():
        # Hold
        input("Press Enter to end sleep...")

    @staticmethod
    def sleep_till_interrupt():
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
        if hasattr(self, "web") and self.web:
            self.web.stop()
            print("CLOSE: web controller stopped")


class JSONLoadSave:

    def __init__(self, controller: Controller):
        self.controller = controller

    @staticmethod
    def validate_item(index: int, item) -> Tuple[bool, Union[None, Fixture]]:
        if not isinstance(item, dict):
            warn("Failed to load item {} from JSON, expected dict, got {}".format(index, type(item)))
            return False, None

        if 'type' not in item:
            warn("Failed to load item {} from JSON, expected a type property".format(index))
            return False, None

        pattern = re.compile(r"^(([\w\d.]+)\.)*([\w\d]+)$", re.IGNORECASE)
        match = pattern.match(item['type'])
        if not match:
            warn("Failed to load item {} from JSON, failed to parse type '{}'".format(index, item['type']))
            return False, None

        try:
            module = import_module(".{}".format(match.group(2)), name + '.profiles')
        except ModuleNotFoundError:
            warn("Failed to load item {} from JSON, profile module '{}' not found".format(index, match.group(2)))
            return False, None

        try:
            module = getattr(module, match.group(3))
        except AttributeError:
            warn("Failed to load item {} from JSON, profile type '{}' not found in '{}'".format(
                index, match.group(3), match.group(2)))
            return False, None

        return True, module

    def load_config(self, filename: str) -> List[Fixture]:
        # Get data
        try:
            with open(filename) as f:
                data = load(f)
        except (FileNotFoundError, OSError):
            raise JSONConfigLoadException(filename)
        except JSONDecodeError:
            raise JSONConfigLoadException(filename, "unable to parse contents")

        if not isinstance(data, list):
            raise JSONConfigLoadException(filename, "expected list of dicts, got {}".format(type(data)))

        # Parse data
        fixtures = []
        for index, item in enumerate(data):
            # Validate entry
            success, module = self.validate_item(index, item)
            if not success or not module:
                continue

            # Parse args
            del item['type']
            args = []
            if 'args' in item:
                args = item['args']
                del item['args']

            # Create
            fixtures.append(self.controller.add_fixture(module, *args, **dict(item)))

        return fixtures

    def save_config(self, filename: Union[str, None] = None, pretty_print: bool = True) -> str:
        # Generate data
        data = []
        for fixture in self.controller.get_all_fixtures():
            data.append(fixture.json_data)

        # JSON-ify
        if pretty_print:
            data = dumps(data, indent=4)
        else:
            data = dumps(data)

        # Save
        if filename:
            with open(filename, "w+") as f:
                f.write(data)
        return data
