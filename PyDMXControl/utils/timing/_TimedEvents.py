"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2019 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from collections import OrderedDict
from threading import Thread
from time import sleep, time
from typing import Dict, Any

from ._TimedEvent import TimedEvent
from ..exceptions import EventAlreadyExistsException
from ... import DMXMINWAIT


class TimedEvents:

    def __init__(self, debug_messages: bool = False):
        self.__events = {}
        self.__started = None
        self.__messages = debug_messages
        self.__run_cbs = []
        self.__stop_cbs = []

    def __run(self, start_millis):
        # Don't allow to run more that once simultaneously
        if self.__started is not None:
            return

        # Set starting params
        self.__started = (time() * 1000.0) - start_millis
        events_left = OrderedDict(sorted(self.__events.items()))

        # Skip events in the past
        for timestamp, event in events_left.copy().items():
            if timestamp < start_millis:
                del events_left[timestamp]

        # Keep looping until last event timestamp
        end = self.__started + max(self.__events.keys()) + 1000
        while end > time() * 1000.0 and self.__started is not None:
            # Find all events to run
            for timestamp, event in events_left.copy().items():
                # Look into the past so we don't ever miss any
                if timestamp <= self.progress:
                    msg = event.run(self.__started)  # Run
                    if self.__messages:  # Debug if needed
                        print(msg)
                    del events_left[timestamp]  # Remove - we're done with it
                else:
                    # We're into the future
                    break
            sleep(0.000001)

        # Let everyone know we're done
        self.__started = None
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
        self.__started = None

        for cb in self.__stop_cbs:
            thread = Thread(target=cb)
            thread.daemon = True
            thread.start()

        for event in self.__events.values():
            event.reset_fired()

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

    def add_stop_callback(self, callback: callable):
        self.__stop_cbs.append(callback)

    def clear_stop_callbacks(self):
        self.__stop_cbs = []

    @property
    def progress(self) -> float:
        if self.__started is None:
            return 0
        return (time() * 1000.0) - self.__started

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "events": {k: v.data for k, v in OrderedDict(sorted(self.__events.items())).items()},
            "progress": "{}ms".format("{:,.4f}".format(self.progress).rstrip("0").rstrip(".")),
            "progress_raw": self.progress
        }

    @property
    def running(self) -> bool:
        return self.__started is not None

    def sleep_till_done(self):
        # Hold until all events completed
        while self.__running:
            sleep(DMXMINWAIT)
