from controller import Controller
from profiles.Generic import Generic
from profiles.LED_RGB import LED_RGB

# Create our controller
dmx = Controller()

# Create some fixtures
dimmer = dmx.add_fixture(Generic(dmx.next_channel))
led = dmx.add_fixture(LED_RGB(dmx.next_channel))

# Set dimmer
dimmer.set_channel('dimmer', 255)

# Set our RGB fixture
led.set_channels(255, 128, 0)

# View the DMX out
print(dmx.channels)