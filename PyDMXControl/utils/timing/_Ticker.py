"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from inspect import getframeinfo, stack
from threading import Thread
from time import sleep, time
from typing import Callable
from warnings import warn

from ..exceptions import InvalidArgumentException
from ... import DEFAULT_INTERVAL


class Callback:

    def __init__(self, callback, interval, last, source):
        if not callable(callback):
            raise InvalidArgumentException('callback', 'Not callable')

        self.callback = callback
        self.interval = interval
        self.last = last
        self.source = source


class Ticker:

    @staticmethod
    def millis_now() -> float:
        return time() * 1000.0

    def __init__(self, interval_millis: float = DEFAULT_INTERVAL * 1000.0, warn_on_behind: bool = True):
        self.__callbacks = []
        self.__paused = False
        self.__ticking = False
        self.__interval = interval_millis
        self.__warn_on_behind = warn_on_behind

    def __ticker(self):
        # Loop over each callback
        for callback in self.__callbacks:
            # New
            if callback.last is None:
                callback.last = self.millis_now()

            # If diff in milliseconds is interval, run
            if self.millis_now() - callback.last >= callback.interval:
                callback.callback()
                callback.last = self.millis_now()

    def __ticker__loop(self):
        # Reset
        for callback in self.__callbacks:
            callback.last = None
        self.__paused = False

        # Use a variable so loop can be stopped
        self.__ticking = True
        while self.__ticking:
            # Track start time
            loop_start = self.millis_now()

            # Call ticker
            if not self.__paused:
                self.__ticker()

            # Get end time and duration
            loop_end = self.millis_now()
            loop_dur = loop_end - loop_start
            wait_dur = self.__interval - loop_dur

            # Handle negative wait
            if wait_dur < 0:
                if self.__warn_on_behind:
                    warn("Ticker loop behind by {:,}ms, took {:,}ms".format(-wait_dur, loop_dur))
                continue

            # Sleep DMX delay time
            sleep(wait_dur / 1000.0)

    def add_callback(self, callback: Callable, interval_millis: float = 1000.0):
        self.__callbacks.append(Callback(callback, interval_millis, None, getframeinfo(stack()[1][0])))

    def remove_callback(self, callback: Callable):
        idx = [i for i, cb in enumerate(self.__callbacks) if cb.callback == callback]
        if len(idx):
            del self.__callbacks[idx[0]]

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
            thread = Thread(target=self.__ticker__loop, daemon=True)
            thread.start()
