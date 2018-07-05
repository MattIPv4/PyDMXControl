from usb.core import USBError

from pyudmx import pyudmx
from .transmittingController import transmittingController


class uDMXController(transmittingController):

    def __init__(self, *args, **kwargs):
        self.__opening = False
        self.__init()

        super().__init__(*args, **kwargs)

    def __init(self):
        self.__opening = True

        try:
            self.udmx.close()
        except:
            pass

        self.udmx = pyudmx.uDMXDevice()
        self.udmx.open()

        self.__opening = False

    def close(self):
        # uDMX
        self.udmx.close()
        print("CLOSE: uDMX closed")

        # Parent
        super().close()

        return

    def _send_data(self):
        data = self.get_frame()
        if not self.__opening:
            try:
                self.udmx.send_multi_value(1, data)
            except Exception as e:
                print(e)
                self.__init()
