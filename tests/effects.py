from time import sleep

from PyDMXControl import Colors
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.effects.Color import Chase
from PyDMXControl.effects.Intensity import Dim

dmx = Controller()

# Load some fixtures from JSON
dmx.json.load_config('json/home.json')

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
Dim.group_apply(dmx.get_all_fixtures(), 1000)

# Wait then clear
sleep(15)
dmx.clear_all_effects()
dmx.all_locate()
sleep(5)

# Test color chase
walls = dmx.get_fixtures_by_name_include('Board') + dmx.get_fixtures_by_name_include('Art') + dmx.get_fixtures_by_name_include('Shelf') + dmx.get_fixtures_by_name_include('Books')
dmx.all_on()
Chase.group_apply(walls, 250 * len(walls), colors=([Colors.Black] * (len(walls) - 1) + [Colors.Blue]))

# Debug
dmx.debug_control()

# Done
dmx.sleep_till_enter()
dmx.close()
