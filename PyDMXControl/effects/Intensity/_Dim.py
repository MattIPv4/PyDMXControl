"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ..defaults import Effect


class Dim(Effect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Start of loop
        self.__start = None

    def callback(self):
        # New
        if self.__start is None:
            self.__start = self.ticker.millis_now()

        offset = self.speed * self.offset  # Calculate offset duration
        delay = self.speed * self.delay  # Calculate delay period after effect
        total = self.speed + delay  # Calculate total loop time (speed + delay)

        start = self.__start + offset  # Account for initial offset
        since_start = self.ticker.millis_now() - start  # Calculate time since effect started
        since_last = since_start % total  # Calculate time since this loop started

        # If in delay period
        if since_last > self.speed:
            self.fixture.set_channel('dimmer', 0)
            return

        # Get progress through this loop (excl delay)
        progress = since_last / self.speed

        # Ensure in range 0 <= p <= 1
        while progress > 1:
            progress = progress - 1
        while progress < 0:
            progress = 1 + progress

        # Flip half way through
        progress *= 2
        if progress > 1:
            progress = 1 - (progress - 1)

        # Ensure we reach 100%
        if progress >= 0.95:
            progress = 1

        # Apply dimmer
        self.fixture.set_channel('dimmer', int(255 * progress))

    def start(self):
        self.__start = None
        super().start()
