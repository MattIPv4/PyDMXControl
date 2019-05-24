"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2019 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from inspect import getsource
from time import time
from typing import Dict, Union


class TimedEvent:

    def __init__(self, run_time: int, callback: callable, args: tuple = (), name: str = ""):
        self.__time = run_time
        self.__cb = callback
        self.__args = args
        self.__name = name
        self.__fired = None

    @property
    def time(self) -> str:
        return "{}ms".format("{:,.4f}".format(self.__time).rstrip("0").rstrip("."))

    @property
    def name(self) -> str:
        return "{}".format(self.__name)

    @property
    def func(self) -> str:
        return "<func {}>".format(self.__cb.__name__)

    @property
    def args(self) -> str:
        return "[{}]".format(", ".join(["{}".format(f) for f in self.__args]))

    @property
    def source(self) -> str:
        return getsource(self.__cb)

    @property
    def fired(self) -> str:
        if self.__fired is None:
            return ""
        return "{:,.4f}ms ({:,.4f}ms late)".format(self.__fired, self.__fired - self.__time)

    @property
    def data(self) -> Dict[str, Union[None, str, float, int]]:
        return {
            "time": self.time,
            "time_raw": self.__time,
            "name": self.name,
            "func": self.func,
            "args": self.args,
            "source": self.source,
            "fired": self.fired,
            "fired_raw": None if self.__fired is None else self.__fired,
            "fired_late_raw": None if self.__fired is None else self.__fired - self.__time
        }

    def __str__(self) -> str:
        return "Event {} (\"{}\") {}".format(self.__time, self.name, self.func)

    def run(self, start_time) -> str:
        self.__cb(*self.__args)
        self.__fired = (time() * 1000.0) - start_time
        return "{} fired at {}".format(str(self), self.fired)

    def reset_fired(self):
        self.__fired = None
