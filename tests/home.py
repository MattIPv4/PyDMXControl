from datetime import datetime

from timed_events_data import get_timed_events

from PyDMXControl import Colors
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.effects.Color import Color_Chase
from PyDMXControl.profiles.Stairville import LED_Par_10mm, LED_Par_36
from PyDMXControl.profiles.funGeneration import LED_Pot_12_RGBW

# This is my home setup, which also acts as a great demo of some of what this library is capable of doing.
# See the tests directory for other recent/new features that I've possibly been working on.

# Create our controller
dmx = Controller()

# Load some fixtures from JSON
dmx.json.load_config('json/home.json')

"""
dmx.add_fixture(LED_Par_10mm, name="Flood")

dmx.add_fixture(LED_Par_36, name="S1 Art Left")
dmx.add_fixture(LED_Par_36, name="S2 Board")
dmx.add_fixture(LED_Par_36, name="S3 Art Right")
dmx.add_fixture(LED_Par_36, name="S4 Books")

dmx.add_fixture(LED_Pot_12_RGBW, name="F1 Desk Right")
dmx.add_fixture(LED_Pot_12_RGBW, name="F2 Desk Left")
"""

# Define all the methods the callback will use
custom_blue = [0, 16, 255, 0]
custom_cyan = [0, 128, 255, 0]
custom_white = [140, 120, 120, 255]
fade_time = 5000


def normal():
    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(Colors.Warm, fade_time)

    Color_Chase.group_apply(dmx.get_fixtures_by_profile(LED_Par_36), 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])
    # for f in dmx.get_fixtures_by_profile(LED_Par_36):
    # f.color(custom_blue, fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Pot_12_RGBW):
        f.color(custom_white, fade_time)


def dimmer():
    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(Colors.Black, fade_time)

    dmx.clear_all_effects()
    for f in dmx.get_fixtures_by_profile(LED_Par_36):
        f.color([int(f * 0.5) for f in custom_blue], fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Pot_12_RGBW):
        f.color([int(f * 0.75) for f in Colors.Warm], fade_time)


# Timed lights
last_state = None
last_state_type = None
times = [
    [(800, 2200)],  # Monday
    [(800, 2200)],  # Tuesday
    [(800, 2200)],  # Wednesday
    [(800, 2200)],  # Thursday
    [(800, 2200)],  # Friday
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
        if time_range[0] <= time < time_range[1]:
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
    if time >= 2100 or time <= 830:
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
dmx.web_control(callbacks=callbacks, timed_events={
    "you-will-be-found": get_timed_events(dmx)
})
# dmx.debug_control(callbacks)

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
