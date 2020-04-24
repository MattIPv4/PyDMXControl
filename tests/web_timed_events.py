from timed_events_data import you_will_be_found, into_the_unknown

from PyDMXControl.controllers import uDMXController as Controller

# Create controller and events
dmx = Controller(dynamic_frame=True, suppress_dmx_value_warnings=True)

# Load some fixtures from JSON
dmx.json.load_config('json/home.json')

# Get the timed events (contains the audio)
you_will_be_found_events = you_will_be_found(dmx)
into_the_unknown_events = into_the_unknown(dmx)

# Web Debug
dmx.web_control(
    timed_events={
        "you-will-be-found": you_will_be_found_events,
        "into-the-unknown": into_the_unknown_events
    }
)

# Done
dmx.sleep_till_enter()
dmx.close()
