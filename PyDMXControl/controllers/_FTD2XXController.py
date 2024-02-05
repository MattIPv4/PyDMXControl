"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from time import sleep
from typing import List

from ._TransmittingController import TransmittingController

try:
    import ftd2xx
except OSError as e:
    print("ftd2xx binaries not present")

class FTD2XXController(TransmittingController):

    def __init__(self, device_number, *args, **kwargs):
        """
        FTD2CXX interface requires a device number to establish connection, e.g. 0

        Parameters
        ----------
        device_number: int
        """

        # Store the device_number and device
        self.__device_number = device_number
        self.__device = None
        super().__init__(*args, **kwargs)

    def _connect(self):
        # Try to close if exists
        if self.__device is not None:
            try:
                self.__device.close()
            except Exception:
                pass

        # Get new device
        self.__device = ftd2xx.open(self.__device_number)
        self.__device.resetDevice()
        self.__device.setBaudRate(250000)
        self.__device.setDataCharacteristics(8, 2, 0) # 8 bit word, 2 stop bit, no parity

    def _close(self):
        self.__device.close()
        print("CLOSE: FTD2XX device connection closed")

    def _transmit(self, frame: List[int], first: int):
        # Convert to a bytearray and pad the start of the frame
        # We're transmitting direct DMX data here, so a frame must start at channel 1, but can end early
        data = bytearray(([0] * (first - 1)) + frame)

        # The first byte in the type, and is `0` for normal DMX data
        data.insert(0, 0)

        # Write
        self.__device.setBreakOn()
        self.__device.setBreakOff()
        self.__device.write(bytes(data))
