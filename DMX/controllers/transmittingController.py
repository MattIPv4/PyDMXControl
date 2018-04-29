from threading import Thread
from typing import List

from DMX.controllers.Controller import Controller


class transmittingController(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__sending = True
        self.__auto = True
        if 'autostart' in kwargs:
            if type(kwargs['autostart']) is bool:
                self.__auto = kwargs['autostart']

        if self.__auto:
            self.run()

    def _send__data(self, data: List[int]):
        pass

    def __send_data_loop(self):
        # Start loop
        self.__sending = True
        while self.__sending:
            # Transmit frame
            self._send__data(self.frame)

            # Sleep (Minimum transmission break for DMX512)
            self.sleep(Controller.DMX_min_wait)

        return

    def close(self, all_zero=False):
        # Stop the threaded loop
        self.__sending = False

        # Send blank frame if wanted
        if all_zero:
            self._send__data([0 for v in range(0, 512)])

    def run(self):
        # Create the thread and transmit data
        Thread(target=self.__send_data_loop).start()
        return
