from DMX import Colors
from DMX.controllers import uDMXController as Controller
from DMX.effects.Intensity import Intensity_Dim
from DMX.profiles.Stairville import LED_Par_36, LED_Par_10mm

dmx = Controller()

dmx.add_fixture(LED_Par_10mm, name="Flood")
dmx.add_fixture(LED_Par_36, name="CL")
dmx.add_fixture(LED_Par_36, name="FL")
dmx.add_fixture(LED_Par_36, name="FR")
dmx.add_fixture(LED_Par_36, name="CR")

color = Colors.Blue
dmx.get_fixtures_by_name("Flood")[0].color(color, 0)
dmx.get_fixtures_by_name("CL")[0].color(color, 0)
dmx.get_fixtures_by_name("FR")[0].color(color, 0)
dmx.get_fixtures_by_name("CR")[0].color(color, 0)
dmx.get_fixtures_by_name("FL")[0].color(color, 0)

speed = 1000
Intensity_Dim(dmx.get_fixtures_by_name("Flood")[0], speed, 400, 0).start()
Intensity_Dim(dmx.get_fixtures_by_name("FR")[0], speed, 400, 100).start()
Intensity_Dim(dmx.get_fixtures_by_name("CR")[0], speed, 400, 200).start()
Intensity_Dim(dmx.get_fixtures_by_name("CL")[0], speed, 400, 300).start()
Intensity_Dim(dmx.get_fixtures_by_name("FL")[0], speed, 400, 400).start()

# dmx.debug_control()

dmx.sleep_till_enter()
dmx.close()
