from PyDMXControl import smart
from PyDMXControl.controllers import uDMXController as Controller

# Create our controller
dmx = Controller()

# Load fixture in from json
dmx.json.load_config('json/home.json')

# Check fixture was loaded
dmx.all_locate()

# Smart
smart.run(dmx)

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
