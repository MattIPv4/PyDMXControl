"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from math import ceil, floor

from ..defaults import Effect
from ... import Colors
from ...utils.exceptions import MissingArgumentException, InvalidArgumentException


class Chase(Effect):

    def __init__(self, *args, **kwargs):
        if 'colors' not in kwargs:
            raise MissingArgumentException('colors', True)

        self.__colors = kwargs['colors'].copy()
        del kwargs['colors']
        self.__length = len(self.__colors)

        if self.__length < 2:
            raise InvalidArgumentException('callback', 'Must contain two or more colors', True)

        self.__snap = False
        if 'snap' in kwargs and isinstance(kwargs['snap'], bool):
            self.__snap = kwargs['snap']
        if 'snap' in kwargs:
            del kwargs['snap']

        super().__init__(*args, **kwargs)

        # Start of loop
        self.__start = None

    def callback(self):
        # New
        if self.__start is None:
            self.__start = self.fixture.controller.ticker.millis_now()

        offset = (self.speed / self.__length) * self.offset  # Calculate offset duration
        start = self.__start + offset  # Account for initial offset
        since_start = self.fixture.controller.ticker.millis_now() - start  # Calculate time since effect started
        since_last = since_start % self.speed  # Calculate time since this loop started

        # Get progress through this loop (excl delay)
        progress = since_last / self.speed

        # Ensure in range 0 <= p <= 1
        while progress > 1:
            progress = progress - 1
        while progress < 0:
            progress = 1 + progress

        # Convert to color index
        progress_index = self.__length * progress
        next_i = ceil(progress_index) - 1
        previous_i = floor(progress_index) - 1
        percent = 1 - (progress_index - 1 - previous_i)

        # Hit 0% & 100%
        if percent >= 0.99:
            percent = 1
        if percent <= 0.01:
            percent = 0

        # Snapping
        if self.__snap:
            if percent <= 0.5:
                percent = 0
            else:
                percent = 1

        # Generate color
        color = Colors.mix(self.__colors[previous_i], self.__colors[next_i], percent)

        # Apply color
        self.fixture.color(color, 0)

    def start(self):
        self.__start = None
        super().start()
