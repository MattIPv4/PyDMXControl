from DMX import Colors
from DMX.controllers import transmittingController as Controller  # This controller has the thread but does nothing
from DMX.profiles.Stairville import LED_Par_10mm, LED_Par_36

# Create our controller
dmx = Controller()

# Create some fixtures (auto insert at next chan)
dmx.add_fixture(LED_Par_10mm)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)

# Test callbacks
def callback1():
    print(1)
def callback2():
    print(2)
dmx.ticker.set_interval(500) # twice per second
dmx.ticker.set_callback(callback1)
dmx.sleep(1)
dmx.ticker.add_callback(callback2)
dmx.sleep(1)

# Set some values
bluegreen = Colors.add(Colors.Blue, Colors.Green, 1, 0.5)
print(bluegreen)
dmx.get_fixture(1).set_channels(bluegreen, None, None, None, 255)
for f in dmx.get_fixtures_by_profile(LED_Par_36):
    f.set_channels(None, bluegreen, None, 255)

# Test if send is threaded
dmx.sleep_till_interrupt()

# Close the controller once we're done
dmx.close()
