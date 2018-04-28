# from DMX.uDMXController import Controller
from DMX.printController import Controller
from DMX.profiles.Stairville import Stairville_LED_Par_10mm, Stairville_LED_Par_36

# Create our controller
dmx = Controller()

# Create some fixtures (auto insert at next chan)
dmx.add_fixture(Stairville_LED_Par_10mm)
dmx.add_fixture(Stairville_LED_Par_36)
dmx.add_fixture(Stairville_LED_Par_36)
dmx.add_fixture(Stairville_LED_Par_36)
dmx.add_fixture(Stairville_LED_Par_36)

# Test if send is threaded
dmx.sleep(2)

# Set some values
dmx.get_fixture(1).set_channels(0, 50, 255, None, None, None, 255)
for f in dmx.get_fixtures_by_profile(Stairville_LED_Par_36):
    f.set_channels(None, 0, 50, 255, None, 255)

# Test if send is threaded
dmx.sleep_till_interrupt()

# Close the controller once we're done
dmx.close()
