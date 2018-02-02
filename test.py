from controller import Controller
from profiles.Generic import Generic
from profiles.LED_RGB import LED_RGB
from profiles.Custom import Custom

# Create our controller
dmx = Controller()

# Create some fixtures
dimmer = dmx.add_fixture(Generic(dmx.next_channel))
led = dmx.add_fixture(LED_RGB(dmx.next_channel))
custom = dmx.add_fixture(Custom(5, dmx.next_channel))

# Set dimmer (1 chan)
dimmer.set_channel('dimmer', 10)

# Set our RGB fixture (3 chan + vdim)
led.set_channels(255, 128, 0, 0)

# Test custom (5 chan, setting chan 1)
custom.set_channel(1, 10)

# View the DMX out
print(dmx.channels)