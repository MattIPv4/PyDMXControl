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


# Define all the methods the callback will use
def standard_lights():
    dmx.get_fixtures_by_name("Flood")[0].set_channels(Colors.Black, 0, 0, 0, 0)
    dmx.get_fixtures_by_name("CL")[0].set_channels(0, Colors.Black, 0, 0)
    dmx.get_fixtures_by_name("FR")[0].set_channels(0, Colors.Black, 0, 0)
    dmx.get_fixtures_by_name("CR")[0].set_channels(0, Colors.Black, 0, 0)
    dmx.get_fixtures_by_name("FL")[0].set_channels(0, Colors.Black, 0, 0)


def normal():
    dmx.get_fixtures_by_name("Flood")[0].anim(2000, *Colors.to_tuples(Colors.White))
    dmx.get_fixtures_by_name("CL")[0].anim(2000, *Colors.to_tuples(Colors.Warm))
    dmx.get_fixtures_by_name("FR")[0].anim(2000, *Colors.to_tuples(Colors.Warm))
    dmx.get_fixtures_by_name("CR")[0].anim(2000, *Colors.to_tuples(Colors.Blue))
    dmx.get_fixtures_by_name("FL")[0].anim(2000, *Colors.to_tuples(Colors.Blue))


def dimmer():
    dmx.get_fixtures_by_name("Flood")[0].anim(2000, *Colors.to_tuples(Colors.Warm))
    dmx.get_fixtures_by_name("CL")[0].anim(2000, *Colors.to_tuples(Colors.Warm))
    dmx.get_fixtures_by_name("FR")[0].anim(2000, *Colors.to_tuples(Colors.Warm))
    dmx.get_fixtures_by_name("CR")[0].anim(2000, *Colors.to_tuples(Colors.Warm))
    dmx.get_fixtures_by_name("FL")[0].anim(2000, *Colors.to_tuples(Colors.Warm))


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


def callback():
    global last_state, last_state_type, times

    time_limit = times[datetime.today().weekday()]
    time = int(datetime.today().strftime('%H%M'))

    in_range = False
    for range in time_limit:
        if range[0] <= time <= range[1]:
            in_range = True

    if in_range:
        if last_state != 1:
            dmx.all_on()
            last_state = 1
    else:
        if last_state != 0:
            dmx.all_off()
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
