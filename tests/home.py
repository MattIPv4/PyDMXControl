from datetime import datetime

from PyDMXControl import Colors
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.profiles.Eyourlife import Small_Flat_Par
from PyDMXControl.profiles.Stairville import LED_Par_10mm, LED_Par_36

# This is my home setup, which also acts as a great demo of some of what this library is capable of doing.
# See the tests directory for other recent/new features that I've possibly been working on.

# Create our controller
dmx = Controller()

# Load some fixtures from JSON
dmx.json.load_config('tests/json/home.json')

"""
dmx.add_fixture(LED_Par_10mm, name="Flood")

dmx.add_fixture(LED_Par_36, name="S1 Art Left")
dmx.add_fixture(LED_Par_36, name="S2 Board")
dmx.add_fixture(LED_Par_36, name="S3 Art Right")
dmx.add_fixture(LED_Par_36, name="S4 Books")

dmx.add_fixture(Small_Flat_Par, name="F1 Desk Right")
dmx.add_fixture(Small_Flat_Par, name="F2 Desk Left")
"""

# Define all the methods the callback will use
custom_blue = [0, 16, 255]
custom_white = [255, 140, 70]


def normal():
    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(Colors.Warm, 10000)

    # Chase.group_apply(dmx.get_fixtures_by_profile(LED_Par_36), 15 * 1000, colors=[Colors.Blue, Colors.Cyan])
    for f in dmx.get_fixtures_by_profile(LED_Par_36):
        f.color(custom_blue, 10000)

    for f in dmx.get_fixtures_by_profile(Small_Flat_Par):
        f.color(custom_white, 10000)


def dimmer():
    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(Colors.Black, 10000)

    # dmx.clear_all_effects()
    for f in dmx.get_fixtures_by_profile(LED_Par_36):
        f.color(custom_blue, 10000)

    for f in dmx.get_fixtures_by_profile(Small_Flat_Par):
        f.color(Colors.Warm, 10000)


# Timed lights
last_state = None
last_state_type = None
times = [
    [(700, 740), (1600, 2200)],  # Monday
    [(700, 740), (1600, 2200)],  # Tuesday
    [(700, 740), (1330, 2200)],  # Wednesday
    [(700, 740), (1600, 2200)],  # Thursday
    [(700, 740), (1330, 2200)],  # Friday
    [(800, 2200)],  # Saturday
    [(800, 2200)],  # Sunday
]


# Create the callback to turn lights on/off and change colors at certain times
def callback():
    global last_state, last_state_type, times

    # Get limits for today an current time
    time_limit = times[datetime.today().weekday()]
    time = int(datetime.today().strftime('%H%M'))

    # Check if current time is within limits
    in_range = False
    for time_range in time_limit:
        if time_range[0] <= time <= time_range[1]:
            in_range = True

    # On if within limits else off
    if in_range:
        if last_state != 1:
            dmx.all_on(10000)
            last_state = 1
    else:
        if last_state != 0:
            dmx.all_off(10000)
            last_state = 0

    # Dim the lights before/after certain times
    if time >= 2100 or time <= 715:
        if last_state_type != 1:
            dimmer()
            last_state_type = 1
    else:
        if last_state_type != 0:
            normal()
            last_state_type = 0


# Enable the callback
dmx.ticker.set_interval(500)
dmx.ticker.set_callback(callback)

# Debug
callbacks = {
    "normal": normal,
    "dimmer": dimmer
}
dmx.web_control(callbacks=callbacks)
# dmx.debug_control(callbacks)

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
