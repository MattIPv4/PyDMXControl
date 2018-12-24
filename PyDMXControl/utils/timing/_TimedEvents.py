"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from collections import OrderedDict
from threading import Thread
from time import sleep, time
from typing import Dict

from ... import DMXMINWAIT
from ._TimedEvent import TimedEvent
from ..exceptions import EventAlreadyExistsException


class TimedEvents:

    def __init__(self, debug_messages: bool = False):
        self.__events = {}
        self.__running = False
        self.__messages = debug_messages
        self.__run_cbs = []

    def __run(self, start_millis):
        # Don't allow to run more that once simultaneously
        if self.__running:
            return

        # Set starting params
        start = (time() * 1000.0) - start_millis
        events_left = OrderedDict(sorted(self.__events.items()))
        self.__running = True

        # Skip events in the past
        for timestamp, event in events_left.copy().items():
            if timestamp < start_millis:
                del events_left[timestamp]

        # Keep looping until last event timestamp
        end = start + max(self.__events.keys()) + 1000
        while end > time() * 1000.0 and self.__running:
            # Find all events to run
            for timestamp, event in events_left.copy().items():
                # Look into the past so we don't ever miss any
                if timestamp <= (time() * 1000.0) - start:
                    msg = event.run(start)  # Run
                    if self.__messages:  # Debug if needed
                        print(msg)
                    del events_left[timestamp]  # Remove - we're done with it
                else:
                    # We're into the future
                    break
            sleep(0.000001)

        # Let debug know we're done
        if self.__messages:
            print("Timed events playback completed")

    def run(self, start_millis: int = 0):
        # Create the thread and run loop
        thread = Thread(target=self.__run, args=[start_millis])
        thread.daemon = True
        thread.start()

        for cb in self.__run_cbs:
            thread = Thread(target=cb)
            thread.daemon = True
            thread.start()

    def stop(self):
        self.__running = False

    def toggle_debug_messages(self) -> bool:
        self.__messages = not self.__messages
        return self.__messages

    def add_event(self, milliseconds_in: int, callback: callable, *args, name: str = ""):
        milliseconds_in = int(milliseconds_in)
        if milliseconds_in in self.__events:
            raise EventAlreadyExistsException(milliseconds_in)
        self.__events[milliseconds_in] = TimedEvent(milliseconds_in, callback, args, name)

    def remove_event(self, milliseconds_in: int):
        milliseconds_in = int(milliseconds_in)
        if milliseconds_in in self.__events:
            del self.__events[milliseconds_in]

    def add_run_callback(self, callback: callable):
        self.__run_cbs.append(callback)

    def clear_run_callbacks(self):
        self.__run_cbs = []

    @property
    def data(self) -> Dict[int, Dict[str, str]]:
        return {k: v.data for k, v in self.__events.items()}

    def sleep_till_done(self):
        # Hold until all events completed
        while self.__running:
            sleep(DMXMINWAIT)
