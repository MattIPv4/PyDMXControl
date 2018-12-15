from PyDMXControl.controllers import uDMXController as Controller

# Create our controller
dmx = Controller()

# Load fixture in from json
dmx.json.load_config('tests/json/load.json')

# Check fixture was loaded
dmx.all_locate()

# Save fixture back to json
print(dmx.json.save_config('tests/json/save.json'))

# Start console debug for testing
dmx.debug_control()

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
