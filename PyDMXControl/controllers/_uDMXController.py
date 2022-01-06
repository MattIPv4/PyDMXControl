"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from typing import List

from pyudmx import pyudmx

from ._TransmittingController import TransmittingController


class uDMXController(TransmittingController):

    def __init__(self, *args, **kwargs):
        # Device information
        self.__udmx_vendor_id = kwargs.pop("udmx_vendor_id", 0x16c0)
        self.__udmx_product_id = kwargs.pop("udmx_product_id", 0x5dc)
        self.__udmx_bus = kwargs.pop("udmx_bus", None)
        self.__udmx_address = kwargs.pop("udmx_address", None)

        # Store the device
        self.__udmx = None

        # Create the parent controller
        super().__init__(*args, **kwargs)

    def _connect(self):
        # Try to close if exists
        if self.__udmx is not None:
            try:
                self.__udmx.close()
            except Exception:
                pass

        # Get new device
        self.__udmx = pyudmx.uDMXDevice()
        self.__udmx.open(self.__udmx_vendor_id, self.__udmx_product_id, self.__udmx_bus, self.__udmx_address)

    def _close(self):
        self.__udmx.close()
        print("CLOSE: uDMX closed")

    def _transmit(self, frame: List[int], first: int):
        # Attempt to send data max 5 times, then 2 more with reconnect to device
        # Thanks to Dave Hocker (pyudmx author) for giving me this solution to the random usb errors
        success = False
        retry_count = 0
        while not success:
            try:
                if retry_count > 5:
                    self._connect()
                self.__udmx.send_multi_value(first, frame)
                success = True
            except Exception as e:
                retry_count += 1
                if retry_count > 7:
                    raise e
