"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""
from queue import Queue, Empty
from threading import Thread
from typing import List

from pyudmx import pyudmx

from ._transmittingController import transmittingController


class uDMXController(transmittingController):

    def __init__(self, *args, **kwargs):
        # Device information
        self.__udmx_vendor_id = kwargs.pop("udmx_vendor_id", 0x16c0)
        self.__udmx_product_id = kwargs.pop("udmx_product_id", 0x5dc)
        self.__udmx_bus = kwargs.pop("udmx_bus", None)
        self.__udmx_address = kwargs.pop("udmx_address", None)

        # Store the device
        self.__udmx = None
        self.__connect()

        # Create the queue
        self.__queue = Queue()
        thread = Thread(target=self.__runner, daemon=True)
        thread.start()

        # Create the parent controller
        super().__init__(*args, **kwargs)

    def close(self):
        # uDMX
        self.__drain()
        self.__queue.put(None)
        self.__queue.join()
        self.__udmx.close()
        print("CLOSE: uDMX closed")

        # Parent
        super().close()

    def _send_data(self):
        self.__queue.put_nowait((self.get_frame(), self.first_channel if self.dynamic_frame else 1))

    def __runner(self):
        while True:
            # Get next item in queue, or wait for item
            item = self.__queue.get()

            # None is passed to end the runner
            if item is None:
                self.__queue.task_done()
                break

            # Transmit current frame
            self.__transmit(*item)
            self.__queue.task_done()

            # Drain excess frames as they are generated more frequently than uDMX can transmit
            self.__drain()

    def __transmit(self, frame: List[int], first: int):
        # Attempt to send data max 5 times, then 2 more with reconnect to device
        # Thanks to Dave Hocker (pyudmx author) for giving me this solution to the random usb errors
        success = False
        retry_count = 0
        while not success:
            try:
                if retry_count > 5:
                    self.__connect()
                self.__udmx.send_multi_value(first, frame)
                success = True
            except Exception as e:
                retry_count += 1
                if retry_count > 7:
                    raise e

    def __connect(self):
        # Try to close if exists
        if self.__udmx is not None:
            try:
                self.__udmx.close()
            except Exception:
                pass

        # Get new device
        self.__udmx = pyudmx.uDMXDevice()
        self.__udmx.open(self.__udmx_vendor_id, self.__udmx_product_id, self.__udmx_bus, self.__udmx_address)

    def __drain(self):
        while not self.__queue.empty():
            try:
                self.__queue.get(False)
            except Empty:
                continue
            self.__queue.task_done()
