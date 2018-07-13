from PyDMXControl import Colors
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.effects.Intensity import Dim
from PyDMXControl.effects.Color import Chase
from PyDMXControl.profiles.Stairville import LED_Par_10mm, LED_Par_36, Quad_Par_Profile

dmx = Controller()

# Fixtures
dmx.add_fixture(LED_Par_10mm, name="Flood")
dmx.add_fixture(LED_Par_36, name="CL")
dmx.add_fixture(LED_Par_36, name="FL")
dmx.add_fixture(LED_Par_36, name="FR")
dmx.add_fixture(LED_Par_36, name="CR")
"""dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)"""

# Effect
dmx.all_locate()

# Chase.group_apply(dmx.get_all_fixtures(), 1000, colors=[Colors.Red, Colors.Yellow, Colors.Green, Colors.Blue])
Chase.group_apply(dmx.get_all_fixtures(), 1000, colors=[Colors.Blue, Colors.Cyan, Colors.White])
# Dim.group_apply(dmx.get_all_fixtures(), 100)

dmx.debug_control()

dmx.sleep_till_enter()
dmx.close()
