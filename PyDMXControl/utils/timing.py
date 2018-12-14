"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from threading import Thread
from time import sleep, time
from typing import Callable

from .exceptions import EventAlreadyExistsException

# DMXMINWAIT = 0.000001 * 92
DMXMINWAIT = 0.01  # Provides far smoother animation


class Ticker:

    @staticmethod
    def millis_now() -> float:
        return time() * 1000.0

    def __init__(self):
        self.__interval = 1000.0
        self.__last = None
        self.__callbacks = []
        self.__paused = False
        self.__ticking = False
        self.thread = None

    def __ticker(self):
        # New
        if self.__last is None:
            self.__last = self.millis_now()

        # If diff in milliseconds is interval
        if self.millis_now() - self.__last >= self.__interval:
            # If have any callbacks
            if self.__callbacks:
                # Loop over each callback
                for callback in self.__callbacks:
                    # Check is valid callback
                    if callback and callable(callback):
                        callback()
            # Finished, update last tick time
            self.__last = self.millis_now()

    def __ticker__loop(self):
        # Reset
        self.__last = None
        self.__paused = False
        # Use a variable so loop can be stopped
        self.__ticking = True
        while self.__ticking:
            # Allow for pausing
            if not self.__paused:
                # Call ticker
                self.__ticker()
            # Sleep DMX delay time
            sleep(DMXMINWAIT)

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

    def clear_callbacks(self):
        self.__callbacks = []

    def stop(self):
        # Stop the threaded loop
        self.__ticking = False

    @property
    def paused(self) -> bool:
        return self.__paused

    def pause(self) -> bool:
        # Toggle pause state
        self.__paused = not self.__paused
        return self.paused

    def start(self):
        if not self.__ticking:
            # Create the thread and run loop
            self.thread = Thread(target=self.__ticker__loop)
            self.thread.daemon = True
            self.thread.start()


class TimedEvents:

    def __init__(self, debug_messages: bool = False):
        self.__events = {}
        self.__running = False
        self.__messages = debug_messages

    def __run(self, start_millis):
        # Don't allow to run more that once simultaneously
        if self.__running:
            return

        # Set starting params
        start = (time() * 1000.0) - start_millis
        events_left = self.__events.copy()
        self.__running = True

        # Skip events in the past
        for timestamp, event in events_left.copy().items():
            if timestamp < start_millis:
                del events_left[timestamp]

        # Keep looping until last event timestamp
        while start + max(self.__events.keys()) + 1000 > time() * 1000.0 and self.__running:
            # Find all events to run
            for timestamp, event in events_left.copy().items():
                # Look into the past so we don't ever miss any
                if timestamp <= (time() * 1000.0) - start:
                    event[0](*event[1], **event[2])  # Run
                    if self.__messages:  # Debug if needed
                        print("Event {} fired at timestamp {}ms: {}".format(
                            timestamp, (time() * 1000.0) - start, event[0]))
                    del events_left[timestamp]  # Remove - we're done with it
            sleep(0.000001)

        # Let debug know we're done
        if self.__messages:
            print("Timed events playback completed")

    def run(self, start_millis: int = 0):
        # Create the thread and run loop
        thread = Thread(target=self.__run, args=[start_millis])
        thread.daemon = True
        thread.start()

    def stop(self):
        self.__running = False

    def toggle_debug_messages(self) -> bool:
        self.__messages = not self.__messages
        return self.__messages

    def add_event(self, milliseconds_in: int, callback: callable, *args, **kwargs):
        milliseconds_in = int(milliseconds_in)
        if milliseconds_in in self.__events:
            raise EventAlreadyExistsException(milliseconds_in)
        self.__events[milliseconds_in] = [callback, args, kwargs]

    def remove_event(self, milliseconds_in: int):
        milliseconds_in = int(milliseconds_in)
        if milliseconds_in in self.__events:
            del self.__events[milliseconds_in]

    def sleep_till_done(self):
        # Hold until all events completed
        while self.__running:
            sleep(DMXMINWAIT)
