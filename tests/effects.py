from time import sleep

from PyDMXControl import Colors
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.effects.Color import Chase
from PyDMXControl.effects.Intensity import Dim
from PyDMXControl.profiles.funGeneration import LED_Pot_12_RGBW
from PyDMXControl.profiles.Stairville import LED_Par_10mm, LED_Par_36

dmx = Controller()

# Fixtures
dmx.add_fixture(LED_Par_10mm)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Pot_12_RGBW)
dmx.add_fixture(LED_Pot_12_RGBW)

# Dim all up
dmx.all_locate()

# Test color chase
Chase.group_apply(dmx.get_all_fixtures(), 1000, colors=[Colors.Red, Colors.Yellow, Colors.Green, Colors.Blue])

# Wait then clear
sleep(15)
dmx.clear_all_effects()
dmx.all_locate()
sleep(5)

# Test color chase
Chase.group_apply(dmx.get_all_fixtures(), 5000, colors=[Colors.Blue, Colors.Cyan, Colors.White])

# Wait then clear
sleep(15)
dmx.clear_all_effects()
dmx.all_locate()
sleep(5)

# Test dim chase
dmx.all_off()
Dim.group_apply(dmx.get_fixtures_by_profile(LED_Par_36), 1000)

# Wait then clear
sleep(15)
dmx.clear_all_effects()
dmx.all_locate()
sleep(5)

# Test color chase
Chase.group_apply(dmx.get_all_fixtures(), 500, colors=[Colors.Red, Colors.Yellow, Colors.Green, Colors.Cyan, Colors.Blue, Colors.Magenta])

# Debug
dmx.debug_control()

# Done
dmx.sleep_till_enter()
dmx.close()
