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


# Test callbacks
def callback1():
    pass


def callback2():
    pass


dmx.ticker.set_interval(500)  # twice per second
dmx.ticker.set_callback(callback1)
dmx.ticker.add_callback(callback2)

# Set some values
bluegreen = Colors.add(Colors.Blue, Colors.Green, 1, 0.5)
dmx.get_fixture(1).set_channels(Colors.Warm, 0, 0, 0, 255)
dmx.get_fixtures_by_name("CL")[0].set_channels(0, Colors.Warm, 0, 255)
dmx.get_fixtures_by_name("FR")[0].set_channels(0, Colors.Warm, 0, 255)
dmx.get_fixtures_by_name("CR")[0].set_channels(0, bluegreen, 0, 255)
dmx.get_fixtures_by_name("FL")[0].set_channels(0, bluegreen, 0, 255)

# Debug
dmx.debug_control()

# Test if send is threaded
dmx.sleep_till_enter()

# Close the controller once we're done
dmx.close()
