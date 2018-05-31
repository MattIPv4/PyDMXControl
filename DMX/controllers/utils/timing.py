from threading import Thread
from time import sleep, time
from typing import Callable

DMXMINWAIT = 0.000001 * 92


class Ticker:

    @staticmethod
    def __millis_now() -> float:
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
            sleep(DMXMINWAIT)

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
