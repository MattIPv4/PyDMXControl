"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from pyudmx import pyudmx

from ._transmittingController import transmittingController


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

    def _send_data(self):
        # Get the data
        data = self.get_frame()

        # Attempt to send data max 5 times
        # Thanks to Dave Hocker (pyudmx author) for giving me this solution to the random usb errors
        success = False
        retry_count = 0
        while not success:
            try:
                self.udmx.send_multi_value(1, data)
                success = True
            except Exception as e:
                retry_count += 1
                if retry_count > 5:
                    raise e
