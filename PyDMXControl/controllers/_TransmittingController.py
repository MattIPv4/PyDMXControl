"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from queue import Queue, Empty
from typing import List

from ._Controller import Controller
from ..utils import ExceptionThread


class TransmittingController(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the frame queue
        self.__queue = Queue()

        # Track the thread
        self.__thread = None

        # Check if auto-start is enabled
        self.__auto = True
        if 'autostart' in kwargs:
            if isinstance(kwargs['autostart'], bool):
                self.__auto = kwargs['autostart']

        # Run if auto-start
        if self.__auto:
            self.run()

    def _connect(self):
        pass

    def _close(self):
        pass

    def _transmit(self, frame: List[int], first: int):
        pass

    def __runner(self):
        while True:
            # Get next item in queue, or wait for item
            item = self.__queue.get()

            # None is passed to end the runner
            if item is None:
                self.__queue.task_done()
                break

            # Transmit current frame
            self._transmit(*item)
            self.__queue.task_done()

            # Drain any excess frames if transmission is slower than frame rate
            self.__drain()

    def __send(self):
        self.__queue.put_nowait((
            self.get_frame(),  # Get the DMX channel frame
            self.first_channel if self.dynamic_frame else 1,  # Get the first channel if frame is dynamic
        ))

    def __drain(self):
        while not self.__queue.empty():
            try:
                self.__queue.get(False)
            except Empty:
                continue
            self.__queue.task_done()

    def close(self):
        # Drain and stop the thread
        if self.__thread:
            self.__drain()
            self.__queue.put(None)
            self.__queue.join()
            self.__thread = None

        # Close the device
        self._close()

        # Parent close
        super().close()

    def run(self):
        # Connect the device
        self._connect()

        # Start the thread
        self.__thread = ExceptionThread(target=self.__runner, daemon=True)
        self.__thread.start()

        # Add the transmission of data to the ticker
        self.ticker.add_callback(self.__send, 0)
