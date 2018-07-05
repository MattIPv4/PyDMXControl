from math import ceil, floor

from DMX import Colors
from DMX.utils.exceptions import MissingArgumentException
from ..defaults import Effect


class Chase(Effect):

    def __init__(self, *args, **kwargs):
        if 'colors' not in kwargs:
            raise MissingArgumentException('colors', True)

        self.__colors = kwargs['colors']
        self.__colors.append(self.__colors[0])
        del kwargs['colors']

        super().__init__(*args, **kwargs)

        # Start of loop
        self.__start = None

    def callback(self):
        # New
        if self.__start is None:
            self.__start = self.ticker.millis_now()

        offset = (self.speed / len(self.__colors)) * self.offset  # Calculate offset duration

        # Initial offset
        if (self.ticker.millis_now() - self.__start) <= offset:
            return

        start = self.__start + offset  # Account for initial offset
        since_start = self.ticker.millis_now() - start  # Calculate time since effect started
        since_last = since_start % self.speed  # Calculate time since this loop started

        # Get progress through this loop (excl delay)
        progress = since_last / self.speed

        # Ensure in range 0 <= p <= 1
        while progress > 1:
            progress = progress - 1
        while progress < 0:
            progress = 1 + progress

        # Ensure we reach 100%
        if progress >= 0.95:
            progress = 1

        # Convert to color index
        index = (len(self.__colors) - 1) * progress
        previous_i = floor(index)
        next_i = ceil(index)
        total = next_i - previous_i
        if total == 0:
            return
        percent = 1 - ((index - previous_i) / (next_i - previous_i))

        color = Colors.mix(self.__colors[previous_i], self.__colors[next_i], percent)

        self.fixture.color(color, 0)

    def start(self):
        self.__start = None
        super().start()
