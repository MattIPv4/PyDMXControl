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


class Text(Part):

    def __init__(self, x: Union[int, float], y: Union[int, float], text: str, *,
                 scale: Union[int, float] = 1, color: Union[List[int], Tuple[int]] = (0, 0, 0),
                 background_color: Union[List[int], Tuple[int], None] = (255, 255, 255, int(255 * 0.95)),
                 align_left: bool = False):
        super().__init__()
        self.__text = text
        self.__scale = scale
        self.__color = color
        self.__bg_color = background_color
        self.__left = align_left
        self.__font = pygame.font.SysFont("monospace", int(24 * self.__scale), bold=True)
        self.set_pos(x, y)

    def design_render(self, screen: 'Screen') -> Tuple[int, int, pygame.Surface]:
        # Generate text
        text = self.__font.render(self.__text, True, self.__color)

        # Resize text
        tx, ty = text.get_size()
        text = pygame.transform.scale(text, (
            int(tx * screen.block_size * 0.15),
            int(ty * screen.block_size * 0.15)
        ))

        # Generate background
        if self.__bg_color is not None:
            padding = screen.block_size * 0.25
            tx, ty = text.get_size()
            surface = pygame.Surface((int(tx + padding * 2), int(ty + padding * 2)), pygame.SRCALPHA, 32)
            surface = surface.convert_alpha()
            surface.fill(self.__bg_color)
            surface.blit(text, (padding, padding))
        else:
            surface = text

        # Render
        x, y = surface.get_size()
        x = int((self._x * screen.block_size) - floor(x / 2))
        y = int((self._y * screen.block_size) - floor(y / 2))
        if self.__left:
            x = int(self._x * screen.block_size)
        return x, y, surface
