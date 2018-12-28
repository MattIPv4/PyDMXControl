"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from typing import List

from ...utils.timing import Ticker


class Effect:

    def __init__(self, fixture: 'Fixture', speed: float, *, delay: float = 0, offset: float = 0):
        # The fixture effect is applied to
        self.fixture = fixture

        # Speed for effect to complete
        self.speed = speed

        # Delay & offset to allow effect stacking across fixtures
        self.delay = delay / 100
        self.offset = offset / 100

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

    @classmethod
    def group_apply(cls, fixtures: List['Fixture'], speed: float, *args, **kwargs):
        # Position
        index = 0
        total = len(fixtures) - 1

        # Iterate over each
        for fixture in fixtures:
            fixture.add_effect(cls, speed, delay=total * 100, offset=index * 100, *args, **kwargs)
            index += 1
