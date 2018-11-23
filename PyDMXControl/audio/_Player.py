"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from threading import Thread
from time import sleep

import pygame

from ..utils.timing import DMXMINWAIT


class Player:

    def __init__(self):
        # set up states
        self.__paused = False
        self.__done = True

        # set up mixer
        self.__freq = 44100  # audio CD quality
        self.__bitsize = -16  # unsigned 16 bit
        self.__channels = 2  # 1 is mono, 2 is stereo
        self.__buffer = 2048  # number of samples
        pygame.mixer.init(self.__freq, self.__bitsize, self.__channels, self.__buffer)

        # set up user preferences
        self.__volume = 0
        self.set_volume(0.8)

    def set_volume(self, volume: float):
        self.__volume = max(min(volume, 1), 0)  # clamp
        pygame.mixer.music.set_volume(volume)

    def __play(self, file: str):
        clock = pygame.time.Clock()

        # Get the file
        try:
            pygame.mixer.music.load(file)
            print("Music file {} loaded!".format(file))
        except pygame.error:
            print("File {} not found! ({})".format(file, pygame.get_error()))
            return

        # Play the file
        self.__paused = False
        self.__done = False
        pygame.mixer.music.play()

        # Tick until play completed
        while pygame.mixer.music.get_busy():
            clock.tick(30)

        # Let everyone know play is done
        self.__done = True

    def play(self, file: str):
        # Play in the background so this isn't blocking
        thread = Thread(target=self.__play, args=[file])
        thread.daemon = True
        thread.start()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def sleep_till_done(self):
        # Hold until the play method sets done
        while not self.__done:
            sleep(DMXMINWAIT)


# Player can only have one instance due to how pygame works
the_player = Player()
