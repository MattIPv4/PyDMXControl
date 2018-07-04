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

        if self.__auto:
            self.run()

        self.__transTicker = Ticker()
        self.__transTicker.set_interval(0)

    def _send_data(self, data: List[int]):
        pass

    def close(self):
        # Stop the threaded loop
        self.__transTicker.stop()
        print("CLOSE: sending = False")

        # Parent
        super().close()

        return

    def run(self):
        # Create the thread and transmit data
        self.__transTicker.clear_callbacks()
        self.__transTicker.add_callback(self._send_data)
        self.__transTicker.start()
