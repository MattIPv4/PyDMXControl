from DMX.Controller import Controller
#from pyudmx import pyudmx
from time import sleep
from threading import Thread


class Controller(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.udmx = pyudmx.uDMXDevice()
        #self.udmx.open()

        self.sending = True
        self.run()

    def __send_data(self):
        while self.sending:
            #self.udmx.send_multi_value(1, self.frame)
            sleep(0.000001*92) # Minimum transmission break for DMX512

    def run(self):
        Thread(target=self.__send_data).start()