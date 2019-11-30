from PyDMXControl import smart, Colors
from PyDMXControl.controllers import uDMXController as Controller

# Create our controller
dmx = Controller()

# Load fixture in from json
dmx.json.load_config('json/home.json')

# Check fixture was loaded
dmx.all_color(Colors.Blue)
dmx.all_on()


def normal():
    dmx.all_color([255, 0, 0])


def dimmer():
    dmx.all_color([255, 128, 0])


callbacks = {
    "normal": normal,
    "dimmer": dimmer
}

# Smart
smart.run(dmx, callbacks=callbacks)

# Debug
dmx.web_control(callbacks=callbacks)

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
smart.stop()
