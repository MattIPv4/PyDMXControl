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

# Define some custom colors and a global fade time
custom_blue = [0, 16, 255, 0]
custom_cyan = [0, 128, 255, 0]
custom_white = [255, 255, int(255 * 0.8), 255]
flood_white = [255, int(255 * 0.9), int(255 * 0.7)]
fade_time = 5000


# Create all the custom state methods
def night():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Par_36):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Pot_12_RGBW):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)


def day():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(flood_white, fade_time)
        f.dim(int(255 * 0.5), fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Par_36):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Pot_12_RGBW):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)


def evening():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(Colors.Warm, fade_time)
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Par_36):
        f.dim(255, fade_time)

    Color_Chase.group_apply(dmx.get_fixtures_by_profile(LED_Par_36), 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])

    for f in dmx.get_fixtures_by_profile(LED_Pot_12_RGBW):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)


def late():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_profile(LED_Par_10mm):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Par_36):
        f.color(Colors.Warm, fade_time)
        f.dim(int(255 * 0.5), fade_time)

    for f in dmx.get_fixtures_by_profile(LED_Pot_12_RGBW):
        f.color(Colors.Warm, fade_time)
        f.dim(int(255 * 0.75), fade_time)


# Create a time map of states for each day
last_state = None
times = [
    {0: night, 830: day, 1800: evening, 2100: late, 2200: night},  # Monday
    {0: night, 830: day, 1800: evening, 2100: late, 2200: night},  # Tuesday
    {0: night, 830: day, 1800: evening, 2100: late, 2200: night},  # Wednesday
    {0: night, 830: day, 1800: evening, 2100: late, 2200: night},  # Thursday
    {0: night, 830: day, 1800: evening, 2100: late, 2200: night},  # Friday
    {0: night, 830: day, 1800: evening, 2100: late, 2200: night},  # Saturday
    {0: night, 830: day, 1800: evening, 2100: late, 2200: night},  # Sunday
]


# Create the callback to turn lights on/off and change colors at certain times
def callback():
    global last_state, times

    # Get map for today and current time
    time_map = times[datetime.today().weekday()]
    time = int(datetime.today().strftime('%H%M'))

    # Find most recent passed time in the map
    keys = sorted(time_map.keys())
    index = -1
    while index + 1 < len(keys) and keys[index + 1] <= time:
        index += 1
    state = keys[index]

    # Run the mapped state if not previously run
    run = time_map[state]
    if last_state != run:
        run()
        last_state = run


# Enable the callback
dmx.ticker.set_interval(500)
dmx.ticker.set_callback(callback)

# Debug
callbacks = {
    "night": night,
    "day": day,
    "evening": evening,
    "late": late,
}
dmx.web_control(callbacks=callbacks, timed_events={
    "you-will-be-found": get_timed_events(dmx)
})
# dmx.debug_control(callbacks)

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
