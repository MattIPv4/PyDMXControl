from DMX.controllers.transmittingController import transmittingController
from pyudmx import pyudmx


class uDMXController(transmittingController):

    def __init__(self, *args, **kwargs):
        self.udmx = pyudmx.uDMXDevice()
        self.udmx.open()

        super().__init__(*args, **kwargs)

    def _send__data(self, data):
        self.udmx.send_multi_value(1, data)
