from pyudmx import pyudmx
from .transmittingController import transmittingController


class uDMXController(transmittingController):

    def __init__(self, *args, **kwargs):
        self.udmx = pyudmx.uDMXDevice()
        self.udmx.open()

        super().__init__(*args, **kwargs)

    def close(self):
        # uDMX
        self.udmx.close()
        print("CLOSE: uDMX closed")

        # Parent
        super().close()

        return

    def _send_data(self, data):
        self.udmx.send_multi_value(1, data)
