from DMX import Colors
from DMX.controllers import uDMXController as Controller
from DMX.effects.Color.Chase import Chase
from DMX.profiles.Stairville import Quad_Par_Profile

dmx = Controller()

# Fixtures
dmx.add_fixture(Quad_Par_Profile, name="test", mode=8)

# Color
# dmx.all_color(Colors.Blue)

# Effect
"""speed = 1000
all = dmx.get_all_fixtures()
i = 0
for fix in all:
    fix.add_effect(Intensity_Dim, speed, delay=(len(all)-1)*100, offset=i*100)
    i += 1"""
# Intensity_Dim.group_apply(dmx.get_all_fixtures(), 1000)
dmx.get_all_fixtures()[0].dim(255, 0)
dmx.get_all_fixtures()[0].add_effect(Chase, 5000, colors=[Colors.Red, Colors.Yellow, Colors.Green, Colors.Blue])

# dmx.debug_control()

dmx.sleep_till_enter()
dmx.close()