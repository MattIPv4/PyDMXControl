from typing import List

from DMX.utils.timing import Ticker
from .Controller import Controller


class transmittingController(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__auto = True
        if 'autostart' in kwargs:
            if type(kwargs['autostart']) is bool:
                self.__auto = kwargs['autostart']

        self.internalTicker = Ticker()
        self.internalTicker.set_interval(0)

        if self.__auto:
            self.run()

    def _send_data(self):
        pass

    def close(self):
        # Stop the threaded loop
        self.internalTicker.stop()
        print("CLOSE: sending = False")

        # Parent
        super().close()

        return

    def run(self):
        # Create the thread and transmit data
        self.internalTicker.clear_callbacks()
        self.internalTicker.add_callback(self._send_data)
        self.internalTicker.start()
