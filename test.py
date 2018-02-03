from controller import Controller
from profiles.Stairville.LED_Par_10mm import Stairville_LED_Par_10mm
from profiles.Stairville.LED_Par_36 import Stairville_LED_Par_36

# Create our controller
dmx = Controller()

# Create some fixtures
dmx.add_fixture(Stairville_LED_Par_10mm(dmx.next_channel))
dmx.add_fixture(Stairville_LED_Par_36(dmx.next_channel))
dmx.add_fixture(Stairville_LED_Par_36(dmx.next_channel))
dmx.add_fixture(Stairville_LED_Par_36(dmx.next_channel))
dmx.add_fixture(Stairville_LED_Par_36(dmx.next_channel))

dmx.get_fixture(1).set_channels(0, 50, 255, None, None, None, 255)
for f in dmx.get_fixtures_by_profile(Stairville_LED_Par_36):
    f.set_channels(None, 0, 50, 255, None, 255)

# View the DMX out
print(dmx.channels)