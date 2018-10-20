from PyDMXControl.controllers import uDMXController as Controller

# Create our controller
dmx = Controller()

# Load from json
dmx.load_json_config('tests/fixtures.json')

# TODO: update fixture so it saves original args and kwargs passed
# TODO: ability to save current fixtures to a json file, using original args and kwargs passed
# TODO: before saving, update any args/kwargs possible, name etc if changed since instantiation

dmx.all_locate()
print(dmx.get_fixture(1).json_data)
dmx.debug_control()

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
