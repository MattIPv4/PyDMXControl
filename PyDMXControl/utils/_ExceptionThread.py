"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from os import kill, getpid
from signal import SIGTERM
from threading import Thread
from traceback import print_exc


class ExceptionThread(Thread):

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except BaseException:
            # Print the exception and kill the whole process
            print_exc()
            kill(getpid(), SIGTERM)
        finally:
            del self._target, self._args, self._kwargs
