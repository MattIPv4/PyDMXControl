"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

import os.path  # User files
from datetime import datetime  # Dates
from math import ceil, floor  # Rounding

import pygame  # PyGame


class Screen:

    def __init__(self):
        self.__thread = None
        self.__running = False
        self.__grid = False
        self.__parts = []
        self.__bg = (245, 245, 245)
        self.block_size = 19

        # Init pygame
        pygame.init()

        # Get font
        self.__font = pygame.font.SysFont("monospace", 15)

        # Create pygame screen
        display_info = pygame.display.Info()
        self.parts_render = None
        self.last_render = None
        self.screen = pygame.display.set_mode((display_info.current_w - 20, display_info.current_h - 70))
        pygame.display.set_caption("PyDMXControl Design")

    def add_part(self, part: 'Part'):
        self.__parts.append(part)

    def __events(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                # if e.key == pygame.K_g:
                #    self.__grid = not self.__grid
                if e.key == pygame.K_q:
                    self.__running = False
                if e.key == pygame.K_s:
                    if self.parts_render:
                        file = "{}/PYDMXControl_Design_{}.png".format(
                            os.path.expanduser("~/Desktop"),
                            datetime.now().strftime("%Y%m%d_%H%M%S")
                        )
                        pygame.image.save(self.parts_render, file)

    def __draw_parts(self):
        # Get render of each
        parts = []
        for part in self.__parts:
            try:
                parts.append(part.design_render(self))
            except Exception as e:
                print(e)

        # Generate size
        maxx = max([f[0] + f[2].get_width() for f in parts])
        maxy = max([f[1] + f[2].get_height() for f in parts])
        surface = pygame.Surface((maxx, maxy), pygame.SRCALPHA, 32)
        surface.convert_alpha()

        # Render
        for part in parts:
            surface.blit(part[2], (part[0], part[1]))

        # Save full res
        self.parts_render = surface

    def __draw_bg(self):
        # New surface
        sx, sy = self.parts_render.get_size()
        surface = pygame.Surface((sx, sy), pygame.SRCALPHA, 32)
        surface.convert_alpha()
        surface.fill(self.__bg)

        # Draw grid
        if self.__grid:
            w, h = pygame.display.get_surface().get_size()
            w = ceil(w / self.block_size)
            h = ceil(h / self.block_size)
            for y in range(h):
                for x in range(w):
                    invert = ((x + (y % 2)) % 2 == 0)
                    color = [200] * 3 if invert else [250] * 3
                    rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                    pygame.draw.rect(surface, color, rect)

        # Add parts
        surface.blit(self.parts_render, (0, 0))

        # Save full res
        self.last_render = surface

    def __draw_mouse(self):
        # Generate text
        mx, my = pygame.mouse.get_pos()
        text = self.__font.render("x: {:,} y: {:,}".format(
            floor(mx / self.block_size),
            floor(my / self.block_size),
        ), True, (0, 0, 0))

        # Generate background
        padding = 5
        x, y = text.get_size()
        surface = pygame.Surface((x + padding * 2, y + padding * 2), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()
        surface.fill((225, 225, 225, 128))

        # Add text
        surface.blit(text, (padding, padding))

        # Add border
        x, y = surface.get_size()
        rectv = pygame.Rect(0, y / 4 * 3, int(floor(padding / 2)), y / 4)
        pygame.draw.rect(surface, (0, 0, 0), rectv)
        recth = pygame.Rect(0, y - int(floor(padding / 2)), y / 4, int(floor(padding / 2)))
        pygame.draw.rect(surface, (0, 0, 0), recth)

        # Render
        self.screen.blit(surface, (mx, my - y))

    def __draw(self):
        # Draw parts
        self.__draw_parts()

        # Draw base
        self.__draw_bg()

        # Draw mouse
        # self.__draw_mouse()

        # Resize if bigger than screen
        mx, my = self.last_render.get_size()
        sx, sy = self.screen.get_size()
        if mx > sx:
            my = my * (sx / mx)
            mx = sx
        if my > sy:
            mx = mx * (sy / my)
            my = sy
        surface = pygame.transform.scale(self.last_render, (floor(mx), floor(my)))

        # Render
        self.screen.fill(self.__bg)
        self.screen.blit(surface, (0, 0))

    def __start(self):
        self.clock = pygame.time.Clock()

        # Draw to screen
        self.__draw()
        redraw = 0

        while self.__running:
            # Handle events
            self.__events()

            # Draw to screen (every 10 cycles)
            if redraw == 10:
                redraw = 0
                self.__draw()
            redraw += 1

            # Update display
            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

    def render(self):
        self.__running = True
        self.__start()
        quit()
