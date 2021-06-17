"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2021 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from threading import Thread
from time import sleep, time
from typing import Callable

from ... import DMXMINWAIT


class Ticker:

    @staticmethod
    def millis_now() -> float:
        return time() * 1000.0

    def __init__(self):
        self.__callbacks = []
        self.__paused = False
        self.__ticking = False
        self.thread = None

    def __ticker(self):
        # Loop over each callback
        for callback in self.__callbacks:
            # New
            if callback["last"] is None:
                callback["last"] = self.millis_now()

            # If diff in milliseconds is interval
            if self.millis_now() - callback["last"] >= callback["interval"]:
                # Check is valid callback
                if callback["callback"] and callable(callback["callback"]):
                    callback["callback"]()

                    # Finished, update last tick time
                    callback["last"] = self.millis_now()

    def __ticker__loop(self):
        # Reset
        for callback in self.__callbacks:
            callback["last"] = None
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

    def add_callback(self, callback: Callable, interval_millis: float = 1000.0):
        self.__callbacks.append({
            "callback": callback,
            "interval": interval_millis,
            "last": None
        })

    def remove_callback(self, callback: Callable):
        idx = [i for i, cb in enumerate(self.__callbacks) if cb["callback"] == callback]
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
            self.thread = Thread(target=self.__ticker__loop)
            self.thread.daemon = True
            self.thread.start()
