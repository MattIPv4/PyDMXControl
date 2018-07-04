from ..defaults import Effect


class Dim(Effect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Start of latest loop
        self.__last = None

    def callback(self):
        # New
        if self.__last is None:
            self.__last = self.ticker.millis_now()

        # Get progress through this loop
        progress = (self.ticker.millis_now() - self.__last) / self.speed

        # Reset if past 100% progress
        if progress >= 1:
            progress = 0
            self.__last = self.ticker.millis_now()

        # Apply offset
        progress += self.offset

        # Ensure in range 0 <= p <= 1
        while progress > 1:
            progress = progress - 1
        while progress < 0:
            progress = 1 + progress

        # Flip half way through
        if progress > 0.5:
            progress = 1 - progress

        print(progress)

        # Apply dimmer
        self.fixture.set_channel('dimmer', int(255 * progress))

    def start(self):
        self.__last = None
        super().start()
