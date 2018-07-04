from DMX import Colors
from DMX.controllers import uDMXController as Controller
from DMX.effects.Intensity import Intensity_Dim
from DMX.profiles.Stairville import LED_Par_36, LED_Par_10mm, Quad_Par_Profile

dmx = Controller()

# Fixtures
dmx.add_fixture(LED_Par_10mm, name="Flood")
dmx.add_fixture(LED_Par_36, name="CL")
dmx.add_fixture(LED_Par_36, name="FL")
dmx.add_fixture(LED_Par_36, name="FR")
dmx.add_fixture(LED_Par_36, name="CR")
dmx.add_fixture(Quad_Par_Profile, name="test")

# Color
dmx.all_color(Colors.Blue)

# Effect
"""speed = 1000
all = dmx.get_all_fixtures()
i = 0
for fix in all:
    fix.add_effect(Intensity_Dim, speed, delay=(len(all)-1)*100, offset=i*100)
    i += 1"""
Intensity_Dim.group_apply(dmx.get_all_fixtures(), 1000)

# dmx.debug_control()

dmx.sleep_till_enter()
dmx.close()
