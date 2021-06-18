"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2021 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from typing import List


class Effect:

    def __init__(self, fixture: 'Fixture', speed: float, *, delay: float = 0, offset: float = 0):
        # The fixture effect is applied to
        self.fixture = fixture

        # Speed for effect to complete
        self.speed = speed

        # Delay & offset to allow effect stacking across fixtures
        self.delay = delay / 100
        self.offset = offset / 100

        # Animating flag for ticket
        self._animating = False

    def callback(self):
        pass

    def pause(self) -> bool:
        self._animating = not self._animating
        return self.__animating

    def stop(self):
        self._animating = False
        self.fixture.controller.ticker.remove_callback(self.callback)

    def start(self):
        self._animating = True
        self.fixture.controller.ticker.add_callback(self.callback, 0)

    @classmethod
    def group_apply(cls, fixtures: List['Fixture'], speed: float, *args, **kwargs):
        # Position
        index = 0
        total = len(fixtures) - 1

        # Iterate over each
        for fixture in fixtures:
            fixture.add_effect(cls, speed, delay=total * 100, offset=index * 100, *args, **kwargs)
            index += 1
