from DMX.Controller import Controller
from pyudmx import pyudmx
from time import sleep
from threading import Thread


class Controller(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.udmx = pyudmx.uDMXDevice()
        self.udmx.open()

        self.__sending = True
        self.__auto = True
        if 'autostart' in kwargs:
            if type(kwargs['autostart']) is bool:
                self.__auto = kwargs['autostart']

        if self.__auto:
            self.run()

    def __send_data(self):
        self.__sending = True
        while self.__sending:

            self.udmx.send_multi_value(1, self.frame)
            sleep(0.000001*92) # Minimum transmission break for DMX512

        return

    def close(self, all_zero = False):
        self.__sending = False

        if all_zero:
            self.udmx.send_multi_value(1, [0 for v in range(0, 512)])
        self.udmx.close()

        return

    def run(self):
        Thread(target=self.__send_data).start()
        return