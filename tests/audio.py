from PyDMXControl import Colors
from PyDMXControl.audio import player
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.effects.Color import Chase
from PyDMXControl.profiles.Eyourlife import Small_Flat_Par
from PyDMXControl.profiles.Stairville import LED_Par_36, LED_Par_10mm
from PyDMXControl.utils.timing import TimedEvents

# Create controller and events
dmx = Controller()
events = TimedEvents(True)

# Load some fixtures from JSON
dmx.load_json_config('tests/json/home.json')

# Pause/play testing
"""
from time import sleep

player.set_volume(0)
player.set_volume(1, 5000)
player.play("tests/you-will-be-found.mp3")
print("playing")
sleep(10)
player.pause()
print("paused")
sleep(3)
player.unpause()
print("unpaused")
sleep(5)
player.stop()
print("stopped")
sleep(5)
"""


# Define some events

def a12600():
    dmx.all_on(2000)
    dmx.get_fixtures_by_name("S1 Art Left")[0].color([50, 100, 255], 2000)
    dmx.get_fixtures_by_name("S3 Art Right")[0].color([50, 100, 255], 2000)


def a45000():
    for fixture in dmx.get_fixtures_by_profile(LED_Par_36):
        fixture.color([0, 128, 255])
        fixture.color([0, 25, 255], 5000)


def a68000():
    for fixture in dmx.get_fixtures_by_profile(LED_Par_10mm):
        fixture.color(Colors.White, 5000)

    for fixture in dmx.get_fixtures_by_profile(Small_Flat_Par):
        fixture.color([0, 128, 255], 5000)


def a93000():
    for fixture in dmx.get_fixtures_by_profile(LED_Par_10mm):
        fixture.color([0, 75, 255], 5000)

    for fixture in dmx.get_fixtures_by_profile(LED_Par_36):
        fixture.color(Colors.White, 5000)

    for fixture in dmx.get_fixtures_by_profile(Small_Flat_Par):
        fixture.color(Colors.White, 5000)


def a125000():
    for fixture in dmx.get_fixtures_by_profile(LED_Par_10mm):
        fixture.color(Colors.Blue, 5000)

    for fixture in dmx.get_fixtures_by_profile(LED_Par_36):
        fixture.color(Colors.Black, 5000)

    for fixture in dmx.get_fixtures_by_profile(Small_Flat_Par):
        fixture.color(Colors.Black, 5000)


def a143900():
    for fixture in dmx.get_fixtures_by_profile(LED_Par_36):
        fixture.dim(0)
        fixture.dim(255, 5000)

    Chase.group_apply(dmx.get_fixtures_by_profile(LED_Par_36), 2000, colors=[
        [50, 128, 255], Colors.Black, Colors.Black, Colors.Black])


def a152000():
    dmx.clear_all_effects()
    dmx.all_color(Colors.Blue)
    dmx.all_color([50, 100, 255], 2000)


def a215000():
    dmx.all_color(Colors.Blue)

    for fixture in dmx.get_fixtures_by_profile(LED_Par_36):
        fixture.color([50, 128, 255], 2000)


# Store events
dmx.all_off()
dmx.all_color(Colors.Blue)
events.add_event(0, dmx.all_dim, 15, 12000)
events.add_event(12600, a12600)
events.add_event(45000, a45000)
events.add_event(68000, a68000)
events.add_event(93000, a93000)
events.add_event(125000, a125000)
events.add_event(143900, a143900)
events.add_event(152000, a152000)
events.add_event(215000, a215000)

# Events testing
player.play("tests/you-will-be-found.mp3")
events.run()
player.sleep_till_done()

# Close
dmx.close()
