"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
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


class InvalidArgumentException(PyDMXControlException, ValueError):

    def __init__(self, argument: str, message: str, kwarg: bool = False):
        super().__init__("Argument '{}' ({}) is not valid - {}.".format(
            argument, message, "Positional" if not kwarg else "Keyword"))


class JSONConfigException(PyDMXControlException):

    def __init__(self, message: str):
        super().__init__(message)


class JSONConfigLoadException(JSONConfigException):

    def __init__(self, filename: str, extra_info: str = ""):
        super().__init__("Failed to load JSON file '{}'{}.".format(
            filename, ", {}".format(extra_info) if extra_info else ""))


class JSONConfigSaveException(JSONConfigException):

    def __init__(self, fixture_id: int):
        super().__init__("Failed to generate JSON data for fixture #{}".format(fixture_id))


class AudioException(PyDMXControlException):

    def __init__(self, message: str):
        super().__init__(message)


class EventAlreadyExistsException(PyDMXControlException):

    def __init__(self, timestamp: int):
        super().__init__("An event already exists at {}".format(timestamp))


class ChannelNotFoundException(PyDMXControlException):

    def __init__(self, channel: str, fixture_id: int):
        super().__init__("Channel {} not found for fixture #{}".format(channel, fixture_id))