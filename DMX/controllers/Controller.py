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
                self.__frame[key - 1] = val[0]

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
                if chanval[0] == -1: chanval[0] = 0

                # If channel id already set
                if chanid in channels.keys():
                    if self.__ltp:
                        # LTP
                        if chanval[1] >= channels[chanid][1]:
                            # HTP if set at identical times
                            if chanval[1] == channels[chanid][1]:
                                if chanval[0] > channels[chanid][0]:
                                    channels[chanid] = chanval
                            else:
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
        # Some default callbacks
        if not 'all_on' in callbacks: callbacks['all_on'] = self.all_on
        if not 'on' in callbacks: callbacks['on'] = self.all_on
        if not 'all_off' in callbacks: callbacks['all_of'] = self.all_off
        if not 'off' in callbacks: callbacks['off'] = self.all_off

        # DMX debug control
        print("[DMX Debug] Currently operating in channels: 1->{}.".format(self.next_channel - 1))
        while True:

            # Fixture selection / callbacks / exit dmx debug
            fixture = input("[DMX Debug] Fixture ID/Name or 'callbacks' (or 'exit'): ").strip()
            if fixture == 'exit':
                break
            if fixture == 'callbacks':
                # Give callbacks
                print("[Callbacks Debug] Available callbacks:",
                      ", ".join(["'" + f + "'" for f in callbacks.keys()]))
                while True:
                    # Callback selection / exit callback debug
                    callback = input("[Callbacks Debug] Callback Name (or 'exit'): ").strip()
                    if callback == 'exit':
                        break
                    if callback not in callbacks:
                        continue
                    try:
                        res = callbacks[callback]()
                    except:
                        print("[Callbacks Debug] '" + callback + "' failed.")
                    else:
                        print("[Callbacks Debug] Callback '" + callback + "' succeed and returned:", res)

                continue

            if not fixture.isdigit():
                fixture = self.get_fixtures_by_name(fixture)
                if fixture: fixture = fixture[0]
            else:
                fixture = self.get_fixture(int(fixture))
            if not fixture:
                continue

            # Fixture debug control
            print("[Fixture Debug] Fixture selected:", fixture)
            while True:

                # Channel selection / exit fixture debug
                channel = input("[Fixture Debug] Channel Number/Name (or 'exit'): ").strip()
                if channel == 'exit':
                    break
                value = input("[Fixture Debug] Channel Value: ").strip()
                if not value.isdigit():
                    continue
                value = int(value)
                fixture.set_channel(channel, value)

    def run(self, *args, **kwargs):
        # Method used in transmitting controllers
        pass

    def close(self, *args, **kwargs):
        # Stop the ticker
        self.ticker.stop()
        print("CLOSE: ticker stopped")

        return
