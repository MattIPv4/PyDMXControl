"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from math import ceil  # Rounding
from threading import Thread  # Threading

import pygame  # PyGame


class Screen:

    def __init__(self):
        self.__thread = None
        self.__running = False
        self.__grid = True
        self.__parts = []
        self.block_size = 6

        # Init pygame
        pygame.init()

        # Create pygame screen
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((display_info.current_w - 50, display_info.current_h - 100))

    def add_part(self, part: 'Part'):
        self.__parts.append(part)

    def __events(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_g:
                    self.__grid = not self.__grid

    def __draw_parts(self):
        for part in self.__parts:
            try:
                part.design_render(self)
            except Exception as e:
                print(e)

    def __start(self):
        self.clock = pygame.time.Clock()

        while self.__running:
            # Handle events
            self.__events()

            # Clear screen
            self.screen.fill((255, 255, 255))

            # Draw grid
            if self.__grid:
                w, h = pygame.display.get_surface().get_size()
                w = ceil(w / self.block_size)
                h = ceil(h / self.block_size)
                for y in range(h):
                    for x in range(w):
                        invert = ((x + (y % 2)) % 2 == 0)
                        color = [180] * 3 if invert else [240] * 3
                        rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                        pygame.draw.rect(self.screen, color, rect)

            # Draw parts
            self.__draw_parts()

            # Update display
            self.clock.tick(60)
            pygame.display.flip()

    def run(self):
        self.__running = True
        self.__start()
        quit()
