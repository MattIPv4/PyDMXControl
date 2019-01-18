"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from math import floor
from typing import Union, List, Tuple

import pygame

from ._Part import Part


class Pipe(Part):

    def __init__(self, size: Union[int, float], x: Union[int, float], y: Union[int, float],
                 rotation: Union[int, float] = 0, *, color: Union[List[int], Tuple[int]] = (80, 80, 80)):
        super().__init__()
        self.__rotation = rotation
        self.__length = size
        self.__color = color
        self.set_pos(x, y)

    def design_render(self, screen: 'Screen') -> Tuple[int, int, pygame.Surface]:
        # Create the surface
        width = int(self.__length * screen.block_size)
        height = int(screen.block_size)
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        # Draw the rect
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(surface, self.__color, rect)

        # Rotate
        surface = pygame.transform.rotate(surface, int(self.__rotation))

        # Render
        x, y = surface.get_size()
        x = int((self._x * screen.block_size) - floor(x / 2))
        y = int((self._y * screen.block_size) - floor(y / 2))
        return x, y, surface
