from controller import Controller
from profiles.Generic import Generic
from profiles.LED_RGB import LED_RGB
from profiles.Custom import Custom

# Create our controller
dmx = Controller()

# Create some fixtures
dimmer1 = dmx.add_fixture(Generic(1))
dimmer2 = dmx.add_fixture(Generic(1))
led = dmx.add_fixture(LED_RGB(dmx.next_channel))
custom = dmx.add_fixture(Custom(5, dmx.next_channel))

# Set dimmer (1 chan)
dimmer1.set_channel('dimmer', 255)

# Set dimmer (1 chan) (Conflict with above dimmer, testing LTP/HTP)
dimmer2.set_channel('dimmer', 10)

# Set our RGB fixture (3 chan + vdim)
led.set_channels(255, 128, 0, 0)

# Test custom (5 chan, setting chan 1)
custom.set_channel(1, 10)

# View the DMX out
print(dmx.channels)

# Test getting by profile
print(dmx.get_fixtures_by_profile(Generic))

# Testing str info
print(led)