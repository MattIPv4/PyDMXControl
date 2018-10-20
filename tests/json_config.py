from PyDMXControl.controllers import uDMXController as Controller

# Create our controller
dmx = Controller()


def doLoad(file):
    from json import load, JSONDecodeError
    import re
    from importlib import import_module

    try:
        with open(file) as f:
            data = load(f)
    except (FileNotFoundError, OSError) as e:
        # exception: bad file name
        print("Failed to open JSON file '{}'".format(file))
        print(e)
        return
    except JSONDecodeError as e:
        # exception: bad file contents
        print("Failed to load JSON file '{}'".format(file))
        print(e)
        return

    if not isinstance(data, list):
        # exception: list of objects
        print("Failed to load from JSON, expected list of objects, got {}".format(type(data)))
        return

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            # warn: expected dict
            print("Failed to load item {} from JSON, expected dict, got {}".format(index, type(item)))
            continue

        if 'type' not in item:
            # warn: expected type property
            print("Failed to load item {} from JSON, expected a type property".format(index))
            continue

        pattern = re.compile(r"^(([\w\d.]+)\.)*([\w\d]+)$", re.IGNORECASE)
        match = pattern.match(item['type'])
        if not match:
            # warn: couldn't understand type
            print("Failed to load item {} from JSON, failed to parse type '{}'".format(index, item['type']))
            continue

        try:
            module = import_module(".{}".format(match.group(2)), 'PyDMXControl.profiles')
        except ModuleNotFoundError as e:
            # warn: profile not found
            print("Failed to load item {} from JSON, profile module '{}' not found".format(index, match.group(2)))
            print(e)
            continue

        try:
            module = getattr(module, match.group(3))
        except AttributeError as e:
            # warn: profile not found
            print("Failed to load item {} from JSON, profile type '{}' not found in '{}'".format(index, match.group(3),
                                                                                                 match.group(2)))
            print(e)
            continue

        print(module)
        del item['type']
        dmx.add_fixture(module, **dict(item))


doLoad('tests/fixtures.json')
dmx.all_locate()
dmx.web_control()

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
