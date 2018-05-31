from threading import Thread
from time import sleep
from typing import List

from .Controller import Controller
from .utils.timing import DMXMINWAIT


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

        self.thread = None

    def _send_data(self, data: List[int]):
        pass

    def __send_data_loop(self):
        # Start loop
        self.__sending = True
        while self.__sending:
            # Transmit frame (if fail, try again)
            try:
                self._send_data(self.get_frame())
            except:
                continue

            # Sleep (Minimum transmission break for DMX512)
            sleep(DMXMINWAIT)

        return

    def close(self):
        # Stop the threaded loop
        self.__sending = False
        print("CLOSE: sending = False")

        # Parent
        super().close()

        return

    def run(self):
        # Create the thread and transmit data
        self.thread = Thread(target=self.__send_data_loop)
        self.thread.daemon = True
        self.thread.start()
