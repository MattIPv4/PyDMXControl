from timed_events_data import get_timed_events

from PyDMXControl.controllers import uDMXController as Controller

# Create controller and events
dmx = Controller(dynamic_frame=True, suppress_dmx_value_warnings=True)

# Load some fixtures from JSON
dmx.json.load_config('json/home.json')

# Get the timed events (contains the audio)
events = get_timed_events(dmx)

# Web Debug
dmx.web_control(
    timed_events={
        "you-will-be-found": events
    }
)

# Done
dmx.sleep_till_enter()
dmx.close()
