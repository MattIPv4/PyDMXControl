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


class Rect(Part):

    def __init__(self, width: Union[int, float], height: Union[int, float], x: Union[int, float], y: Union[int, float],
                 *, outline_color: Union[List[int], Tuple[int]] = (255, 0, 0),
                 fill_color: Union[List[int], Tuple[int]] = (255, 255, 255, 0), ):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__outline = outline_color
        self.__fill = fill_color
        self.set_pos(x, y)

    def design_render(self, screen: 'Screen') -> Tuple[int, int, pygame.Surface]:
        # Create the surface
        width = int(self.__width * screen.block_size)
        height = int(self.__height * screen.block_size)
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        # Draw the rect
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(surface, self.__fill, rect)
        pygame.draw.rect(surface, self.__outline, rect, int(screen.block_size / 4 * 3))

        # Render
        return int(self._x * screen.block_size), int(self._y * screen.block_size), surface
