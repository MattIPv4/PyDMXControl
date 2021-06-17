"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2021 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ._Controller import Controller


class transmittingController(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__auto = True
        if 'autostart' in kwargs:
            if isinstance(kwargs['autostart'], bool):
                self.__auto = kwargs['autostart']

        if self.__auto:
            self.run()

    def _send_data(self):
        pass

    def run(self):
        # Add the transmission of data to the ticker
        self.ticker.add_callback(self._send_data, 0)
