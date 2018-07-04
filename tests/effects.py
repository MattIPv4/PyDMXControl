from DMX import Colors
from DMX.controllers import printController as Controller
from DMX.profiles.Stairville import LED_Par_10mm
from DMX.effects.Intensity import Intensity_Dim

dmx = Controller()

dmx.add_fixture(LED_Par_10mm, name="Flood")

dmx.get_fixtures_by_name("Flood")[0].set_channels(255, 255, 255, 0, 0, 0, 0)

effect = Intensity_Dim(dmx.get_fixtures_by_name("Flood")[0], 10000)
effect.start()

# dmx.debug_control()

dmx.sleep_till_enter()
dmx.close()
