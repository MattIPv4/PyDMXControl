from timed_events import get_timed_events

from PyDMXControl.audio import player
from PyDMXControl.controllers import uDMXController as Controller

# Create controller and events
dmx = Controller(suppress_dmx_value_warnings=True)

# Load some fixtures from JSON
dmx.json.load_config('json/home.json')

# Pause/play testing
"""
from time import sleep

player.set_volume(0)
player.set_volume(1, 5000)
player.play("you-will-be-found.mp3")
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

# Get the timed events (contains the audio)
events = get_timed_events(dmx)

# Play a light show using events to dear evan hansen - you will be found
events.run()

dmx.sleep_till_enter()

# Close
dmx.close()
