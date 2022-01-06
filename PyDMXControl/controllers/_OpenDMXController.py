"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from typing import List

from pyftdi.ftdi import Ftdi

from ._TransmittingController import TransmittingController


class OpenDMXController(TransmittingController):

    def __init__(self, *args, **kwargs):
        # Device information
        self.__ftdi_vendor_id = kwargs.pop("ftdi_vendor_id", 0x0403)
        self.__ftdi_product_id = kwargs.pop("ftdi_product_id", 0x6001)
        self.__ftdi_serial = kwargs.pop("ftdi_serial", None)

        # Store the device
        self.__ftdi = None

        # Create the parent controller
        super().__init__(*args, **kwargs)

    def _connect(self):
        # Try to close if exists
        if self.__ftdi is not None:
            try:
                self.__ftdi.close()
            except Exception:
                pass

        # Get new device
        self.__ftdi = Ftdi()
        self.__ftdi.open(self.__ftdi_vendor_id, self.__ftdi_product_id, serial=self.__ftdi_serial)
        self.__ftdi.reset()
        self.__ftdi.set_baudrate(baudrate=250000)
        self.__ftdi.set_line_property(bits=8, stopbit=2, parity='N', break_=False)

    def _close(self):
        self.__ftdi.close()
        print("CLOSE: OpenDMX closed")

    def _transmit(self, frame: List[int], first: int):
        # Convert to a bytearray and pad the start of the frame
        # We're transmitting direct DMX data here, so a frame must start at channel 1, but can end early
        data = bytearray(([0] * (first - 1)) + frame)

        # The first byte in the type, and is `0` for normal DMX data
        data.insert(0, 0)

        # Write
        self.__ftdi.set_break(True)
        self.__ftdi.set_break(False)
        self.__ftdi.write_data(data)
