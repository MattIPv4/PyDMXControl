from DMX.profiles.defaults import Fixture
from DMX.utils.timing import Ticker


class Effect:

    def __init__(self, fixture: Fixture, speed_milliseconds: int, offset_percent: float = 0):
        # The fixture effect is applied to
        self.fixture = fixture

        # Speed for effect to complete
        self.speed = speed_milliseconds

        # Offset to allow effect stacking across fixtures
        self.offset = offset_percent / 100

        # Ticker for callback
        self.ticker = Ticker()
        self.ticker.set_interval(0)

    def callback(self):
        pass

    def pause(self) -> bool:
        return self.ticker.pause()

    def stop(self):
        self.ticker.stop()

    def start(self):
        self.ticker.clear_callbacks()
        self.ticker.add_callback(self.callback)
        self.ticker.start()
