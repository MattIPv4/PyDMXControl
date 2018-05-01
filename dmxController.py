from datetime import datetime

from DMX import Colors
from DMX.controllers import uDMXController as Controller  # This controller has the thread but does nothing
from DMX.profiles.Stairville import LED_Par_10mm, LED_Par_36

# Create our controller
dmx = Controller()

# Create some fixtures (auto insert at next chan)
dmx.add_fixture(LED_Par_10mm, name="Flood")
dmx.add_fixture(LED_Par_36, name="CL")
dmx.add_fixture(LED_Par_36, name="FL")
dmx.add_fixture(LED_Par_36, name="FR")
dmx.add_fixture(LED_Par_36, name="CR")


def standard_lights():
    dmx.get_fixtures_by_name("Flood")[0].set_channels(Colors.White, 0, 0, 0, 0)
    dmx.get_fixtures_by_name("CL")[0].set_channels(0, Colors.Warm, 0, 0)
    dmx.get_fixtures_by_name("FR")[0].set_channels(0, Colors.Warm, 0, 0)
    dmx.get_fixtures_by_name("CR")[0].set_channels(0, Colors.Blue, 0, 0)
    dmx.get_fixtures_by_name("FL")[0].set_channels(0, Colors.Blue, 0, 0)


def on():
    for f in dmx.get_all_fixtures():
        f.dim(255, 2000)


def off():
    for f in dmx.get_all_fixtures():
        f.dim(0, 2000)


# Set some values
standard_lights()

# Timed lights
last_state = None
times = [
    [(700, 800), (1510, 2130)],  # Monday
    [(700, 800), (1550, 2130)],  # Tuesday
    [(700, 800), (1550, 2130)],  # Wednesday
    [(700, 800), (1550, 2130)],  # Thursday
    [(700, 800), (1510, 2200)],  # Friday
    [(900, 2200)],  # Saturday
    [(900, 2130)],  # Sunday
]


def callback():
    global last_state, times

    time_limit = times[datetime.today().weekday()]
    time = int(datetime.today().strftime('%H%M'))

    in_range = False
    for range in time_limit:
        if time >= range[0] and time <= range[1]:
            in_range = True

    if in_range:
        if last_state != 1:
            on()
            last_state = 1
    else:
        if last_state != 0:
            off()
            last_state = 0


dmx.ticker.set_interval(500)
dmx.ticker.set_callback(callback)

# Debug
dmx.debug_control()

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
