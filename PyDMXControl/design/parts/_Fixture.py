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
from ._Text import Text
from .data import load
from .._screen import Screen


class Fixture(Part):

    def __init__(self, x: Union[int, float], y: Union[int, float], name: str = "", rotation: Union[int, float] = 0, *,
                 outline_color: Union[List[int], Tuple[int]] = (0, 0, 0),
                 fill_color: Union[List[int], Tuple[int]] = (255, 255, 255),
                 label: str = "", scale: float = 1, align_left: bool = False):
        super().__init__()
        self.__rotation = rotation
        self.__name = name
        self.__data = load(name)
        self.__outline = outline_color
        self.__fill = fill_color
        self.__label = Text(0, 0, label, scale=scale) if label else None
        self.__scale = scale
        self.__size = 0.06 * self.__scale
        self.__left = align_left
        self.set_pos(x, y)

    def design_render(self, screen: Screen) -> Tuple[int, int, pygame.Surface]:
        # Get points from fixture else rectangle
        raw_points = self.__data[2] if self.__data else [[0, 0, 0], [30, 0, 1], [30, 10, 1], [0, 10, 1]]

        # Get largest x/y
        maxx = max([f[0] for f in raw_points])
        maxy = max([f[1] for f in raw_points])

        # Split the points up into their line groups
        pen = 6
        points = []
        for point in raw_points:
            if point[2] == 0:
                points.append([])
            points[-1].append([point[0] + pen, point[1] + pen])

        # Generate the surface
        surface = pygame.Surface((maxx + (pen * 2), maxy + (pen * 2)), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()

        # Draw each line group filled
        for point_set in points:
            if len(point_set) > 2:
                pygame.draw.polygon(surface, self.__fill, point_set)

        # Draw each line group outline
        for point_set in points:
            if len(point_set) > 1:
                pygame.draw.lines(surface, self.__outline, True, point_set, pen)

        # Resize
        """max_size = self.__size
        x, y = surface.get_size()
        if x > y:
            y = y * (max_size / x)
            x = max_size
        else:
            x = x * (max_size / y)
            y = max_size
        x, y = int(x), int(y)
        surface = pygame.transform.scale(surface, (x * screen.block_size, y * screen.block_size))"""
        x, y = surface.get_size()
        surface = pygame.transform.scale(surface, (
        int(x * self.__size * screen.block_size), int(y * self.__size * screen.block_size)))

        # Rotate
        surface = pygame.transform.rotate(surface, int(self.__rotation))

        # Calc pos
        x, y = surface.get_size()
        x = int((self._x * screen.block_size) - floor(x / 2))
        y = int((self._y * screen.block_size) - floor(y / 2))
        if self.__left:
            x = int(self._x * screen.block_size)

        # Text label
        if self.__label is not None:
            # Generate text
            text = self.__label.design_render(screen)[2]

            # Add to full
            tx, ty = text.get_size()
            fx, fy = surface.get_size()
            new_surface = pygame.Surface((tx + fx + 3, max(ty, fy + ty / 2)), pygame.SRCALPHA, 32)
            new_surface = new_surface.convert_alpha()
            new_surface.blit(surface, (0, new_surface.get_height() - fy))
            new_surface.blit(text, (fx + 3, 0))

            # Update pos
            y -= (new_surface.get_height() - fy)
        else:
            new_surface = surface

        # Render
        return x, y, new_surface
