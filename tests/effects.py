from DMX import Colors
from DMX.controllers import uDMXController as Controller
from DMX.effects.Intensity import Dim
from DMX.effects.Color import Chase
from DMX.profiles.Stairville import Quad_Par_Profile

dmx = Controller()

# Fixtures
dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)
dmx.add_fixture(Quad_Par_Profile, mode=8)

# Effect
dmx.all_locate()

#Chase.group_apply(dmx.get_all_fixtures(), 1000, colors=[Colors.Red, Colors.Yellow, Colors.Green, Colors.Blue])
Dim.group_apply(dmx.get_all_fixtures(), 1000)

dmx.debug_control()

dmx.sleep_till_enter()
dmx.close()
