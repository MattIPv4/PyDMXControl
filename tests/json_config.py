from PyDMXControl.controllers import uDMXController as Controller

# Create our controller
dmx = Controller()


def doLoad(file):
    from json import load, JSONDecodeError
    import re
    from importlib import import_module
    from warnings import warn
    from PyDMXControl.utils.exceptions import PyDMXControlException

    class JSONConfigException(PyDMXControlException):

        def __init__(self, filename: str, extra_info: str = ""):
            super().__init__("Failed to load JSON file '{}'{}.".format(
                filename, ", {}".format(extra_info) if extra_info else ""))

    try:
        with open(file) as f:
            data = load(f)
    except (FileNotFoundError, OSError):
        raise JSONConfigException(file)
    except JSONDecodeError:
        raise JSONConfigException(file, "unable to parse contents")

    if not isinstance(data, list):
        raise JSONConfigException(file, "expected list of dicts, got {}".format(type(data)))

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            warn("Failed to load item {} from JSON, expected dict, got {}".format(index, type(item)))
            continue

        if 'type' not in item:
            warn("Failed to load item {} from JSON, expected a type property".format(index))
            continue

        pattern = re.compile(r"^(([\w\d.]+)\.)*([\w\d]+)$", re.IGNORECASE)
        match = pattern.match(item['type'])
        if not match:
            warn("Failed to load item {} from JSON, failed to parse type '{}'".format(index, item['type']))
            continue

        try:
            module = import_module(".{}".format(match.group(2)), 'PyDMXControl.profiles')
        except ModuleNotFoundError:
            warn("Failed to load item {} from JSON, profile module '{}' not found".format(index, match.group(2)))
            continue

        try:
            module = getattr(module, match.group(3))
        except AttributeError:
            warn("Failed to load item {} from JSON, profile type '{}' not found in '{}'".format(index, match.group(3),
                                                                                                match.group(2)))
            continue

        del item['type']
        dmx.add_fixture(module, **dict(item))


doLoad('tests/fixtures.json')
dmx.all_locate()
dmx.web_control()

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
