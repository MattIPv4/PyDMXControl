from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.profiles.Eyourlife import Small_Flat_Par
from PyDMXControl.profiles.Stairville import LED_Par_10mm, LED_Par_36

dmx = Controller()

# Fixtures
dmx.add_fixture(LED_Par_10mm)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(Small_Flat_Par)
dmx.add_fixture(Small_Flat_Par)

# Web Debug
dmx.web_control()

# Dim all up
dmx.all_locate()

# Done
dmx.sleep_till_enter()
dmx.close()
