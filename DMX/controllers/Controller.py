from threading import Thread
from time import sleep
from time import time
from typing import Type, Callable, List, Union, Dict

from DMX.profiles.defaults import Fixture


class Ticker:

    def __millis_now(self) -> float:
        return time() * 1000.0

    def __init__(self):
        self.__interval = 1000.0
        self.__last = self.__millis_now()
        self.__callbacks = []
        self.__ticking = False
        self.thread = None

    def __ticker(self):
        # If diff in milliseconds is interval
        if self.__millis_now() - self.__last >= self.__interval:
            # If have any callbacks
            if self.__callbacks:
                # Loop over each callback
                for callback in self.__callbacks:
                    # Check is valid callback
                    if callback and callable(callback):
                        callback()
            # Finished, update last tick time
            self.__last = self.__millis_now()

    def __ticker__loop(self):
        # Use a variable so loop can be stopped
        self.__ticking = True
        while self.__ticking:
            # Call ticker and sleep DMX delay time
            self.__ticker()
            sleep(Controller.DMX_min_wait)

        return

    def set_interval(self, milliseconds: float):
        self.__interval = milliseconds

    def get_interval(self) -> float:
        return self.__interval

    def set_callback(self, callback: Callable):
        self.__callbacks = [callback]

    def add_callback(self, callback: Callable):
        self.__callbacks.append(callback)

    def remove_callback(self, callback: Callable):
        if callback in self.__callbacks:
            self.__callbacks.remove(callback)

    def stop(self):
        # Stop the threaded loop
        self.__ticking = False

    def start(self):
        # Create the thread and run loop
        self.thread = Thread(target=self.__ticker__loop)
        self.thread.daemon = True
        self.thread.start()


class Controller:
    DMX_min_wait = 0.000001 * 92

    def __init__(self, *, ltp=False, dynamic_frame=False):
        # Store all registered fixtures
        self.__fixtures = {}

        # LTP (default HTP) (Lowest not latest, tracking latest is far too much work)
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

    def sleep(self, seconds: float = 1) -> None:
        # Hold
        sleep(seconds)

        # We're done
        return None

    def sleep_till_enter(self) -> None:
        # Hold
        input("Press Enter to end sleep...")

        # We're done
        return None

    def sleep_till_interrupt(self) -> None:
        # Hold
        try:
            while True:
                sleep(Controller.DMX_min_wait)
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
                self.__frame[key - 1] = val

        # Return populated frame
        return self.__frame

    @property
    def channels(self) -> Dict[int, int]:
        channels = {}

        # Channels for each registered fixture
        for chans in [v.channels for v in self.__fixtures.values()]:
            # Channels in this fixture
            for chanid, chanval in chans.items():
                chanval = chanval['value']
                # If channel id already set
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

        # Return all the channels
        return channels

    @property
    def next_channel(self) -> int:
        # Get all channels
        channels = list(self.channels.keys())

        # Return next channel
        return max(channels or [0]) + 1

    def run(self, *args, **kwargs):
        # Method used in transmitting controllers
        pass

    def close(self, *args, **kwargs):
        # Stop the ticker
        self.ticker.stop()
        print("CLOSE: ticker stopped")

        return
