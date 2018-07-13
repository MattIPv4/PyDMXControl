from datetime import datetime

from PyDMXControl import Colors
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.profiles.Stairville import LED_Par_10mm, LED_Par_36

# This is my home setup, which also acts as a great demo of some of what this library is capabple of doing.
# See the tests directory for other recent/new features that I've possibly been working on.

# Create our controller
dmx = Controller()

# Create some fixtures (auto insert at next chan)
dmx.add_fixture(LED_Par_10mm, name="Flood")
dmx.add_fixture(LED_Par_36, name="CL")
dmx.add_fixture(LED_Par_36, name="FL")
dmx.add_fixture(LED_Par_36, name="FR")
dmx.add_fixture(LED_Par_36, name="CR")


# Define all the methods the callback will use
def standard_lights():
    dmx.get_fixtures_by_name("Flood")[0].set_channels(Colors.Black, 0, 0, 0, 0)
    dmx.get_fixtures_by_name("CL")[0].set_channels(0, Colors.Black, 0, 0)
    dmx.get_fixtures_by_name("FR")[0].set_channels(0, Colors.Black, 0, 0)
    dmx.get_fixtures_by_name("CR")[0].set_channels(0, Colors.Black, 0, 0)
    dmx.get_fixtures_by_name("FL")[0].set_channels(0, Colors.Black, 0, 0)


def normal():
    dmx.get_fixtures_by_name("Flood")[0].color(Colors.White, 10000)
    dmx.get_fixtures_by_name("CL")[0].color(Colors.Warm, 10000)
    dmx.get_fixtures_by_name("FR")[0].color(Colors.Warm, 10000)
    dmx.get_fixtures_by_name("CR")[0].color(Colors.Blue, 10000)
    dmx.get_fixtures_by_name("FL")[0].color(Colors.Blue, 10000)


def dimmer():
    dmx.get_fixtures_by_name("Flood")[0].color(Colors.Warm, 10000)
    dmx.get_fixtures_by_name("CL")[0].color(Colors.Warm, 10000)
    dmx.get_fixtures_by_name("FR")[0].color(Colors.Warm, 10000)
    dmx.get_fixtures_by_name("CR")[0].color(Colors.Warm, 10000)
    dmx.get_fixtures_by_name("FL")[0].color(Colors.Warm, 10000)


# Set some values
standard_lights()

# Timed lights
last_state = None
last_state_type = None
times = [
    [(700, 750), (1500, 2130)],  # Monday
    [(700, 750), (1600, 2130)],  # Tuesday
    [(700, 750), (1600, 2130)],  # Wednesday
    [(700, 750), (1600, 2130)],  # Thursday
    [(700, 750), (1330, 2200)],  # Friday
    [(900, 2200)],  # Saturday
    [(900, 2130)],  # Sunday
]


# Create the callback to turn lights on/off and change colors at certain times
def callback():
    global last_state, last_state_type, times

    time_limit = times[datetime.today().weekday()]
    time = int(datetime.today().strftime('%H%M'))

    in_range = False
    for time_range in time_limit:
        if time_range[0] <= time <= time_range[1]:
            in_range = True

    if in_range:
        if last_state != 1:
            dmx.all_on(10000)
            last_state = 1
    else:
        if last_state != 0:
            dmx.all_off(10000)
            last_state = 0

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
dmx.debug_control({
    "normal": normal,
    "dimmer": dimmer
})

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
