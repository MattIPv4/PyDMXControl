"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

import pygame

from ._Part import Part
from .._screen import Screen


class Pipe(Part):

    def __init__(self, size: int, x: int, y: int, rotation: int = 0):
        super().__init__()
        self.__rotation = rotation
        self.__length = size
        self.set_pos(x, y)

    def design_render(self, screen: Screen):
        # Create the surface
        surface = pygame.Surface((self.__length * screen.block_size, screen.block_size))
        surface.fill([80] * 3)

        # Rotate
        surface = pygame.transform.rotate(surface, self.__rotation)

        # Render
        screen.screen.blit(surface, (self._x * screen.block_size, self._y * screen.block_size))
