from PyDMXControl.controllers import uDMXController as Controller

# Create our controller
dmx = Controller()

# Load from json
dmx.load_json_config('tests/fixtures.json')

dmx.all_locate()

# Save to json
print(dmx.save_json_config('tests/save.json'))

dmx.debug_control()

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
