"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""


class PyDMXControlException(Exception):
    pass


class LTPCollisionException(PyDMXControlException):

    def __init__(self, channel_id: int):
        super().__init__("Channel {} has two different values assigned at the same timestamp.".format(channel_id))


class FixtureCreationException(PyDMXControlException):

    def __init__(self, fixture_class, message: str):
        super().__init__("Unable to create fixture '{}': {}.".format(fixture_class, message))


class MissingArgumentException(PyDMXControlException, ValueError):

    def __init__(self, argument: str, kwarg: bool = False):
        super().__init__("Argument '{}' ({}) missing from call.".format(
            argument, "Positional" if not kwarg else "Keyword"))


class JSONConfigException(PyDMXControlException):

    def __init__(self, message: str):
        super().__init__(message)


class JSONConfigLoadException(JSONConfigException):

    def __init__(self, filename: str, extra_info: str = ""):
        super().__init__("Failed to load JSON file '{}'{}.".format(
            filename, ", {}".format(extra_info) if extra_info else ""))


class JSONConfigSaveException(JSONConfigException):

    def __init__(self, message: str):
        super().__init__(message)


class AudioException(PyDMXControlException):

    def __init__(self, message: str):
        super().__init__(message)


class EventAlreadyExistsException(PyDMXControlException):

    def __init__(self, timestamp: int):
        super().__init__("An event already exists at {}".format(timestamp))
