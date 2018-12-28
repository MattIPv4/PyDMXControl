"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

import contextlib
from threading import Thread
from time import sleep, time

with contextlib.redirect_stdout(None):  # PyGame please shut up
    import pygame

from ..utils.exceptions import AudioException
from .. import DMXMINWAIT


class Player:

    def __init__(self):
        # set up states
        self.__paused = False
        self.__done = True

        # set up mixer
        # https://www.daniweb.com/programming/software-development/threads/491663/how-to-open-and-play-mp3-file-in-python
        self.__freq = 44100  # audio CD quality
        self.__bitsize = -16  # unsigned 16 bit
        self.__channels = 2  # 1 is mono, 2 is stereo
        self.__buffer = 2048  # number of samples
        pygame.mixer.init(self.__freq, self.__bitsize, self.__channels, self.__buffer)

        # set up user preferences
        self.__volume = 0
        self.set_volume(0.8)

    def __set_volume(self, vol):
        vol = max(min(vol, 1), 0)  # clamp
        self.__volume = vol
        pygame.mixer.music.set_volume(vol)

    def __fade_volume(self, current, target, millis):
        start = time() * 1000.0
        gap = target - current

        if millis > 0:
            while (time() * 1000.0) - start <= millis:
                diff = gap * (((time() * 1000.0) - start) / millis)
                self.__set_volume(current + diff)
                sleep(0.000001)
        self.__set_volume(target)

    def set_volume(self, volume: float, milliseconds: int = 0):
        volume = max(min(volume, 1), 0)  # clamp

        # Create the thread and run loop
        thread = Thread(target=self.__fade_volume, args=(self.__volume, volume, milliseconds))
        thread.daemon = True
        thread.start()

    def __play(self, file, start_millis):
        # Stop anything previous
        self.stop()

        # Set states
        self.__paused = False
        self.__done = False

        # Get the file
        try:
            pygame.mixer.music.load(file)
        except pygame.error:
            self.__done = True
            raise AudioException("Error occurred loading '{}': {}".format(file, pygame.get_error()))

        # Play the file and tick until play completed
        pygame.mixer.music.play(start=start_millis / 1000)
        while pygame.mixer.music.get_busy():
            sleep(DMXMINWAIT)

        # Let everyone know play is done
        self.__done = True

    def play(self, file: str, start_millis: int = 0):
        # Play in the background so this isn't blocking
        thread = Thread(target=self.__play, args=[file, start_millis])
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

    def sleep_till_interrupt(self):
        # This is very useful for playing song, stopping at a specific point and getting the timestamp
        # Probably not very useful in production but useful in development

        # Hold
        try:
            while True:
                sleep(DMXMINWAIT)
        except KeyboardInterrupt:
            print(pygame.mixer.music.get_pos())
            self.stop()


# Player can only have one instance due to how pygame works
the_player = Player()
