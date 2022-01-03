from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.effects.Intensity import Dim
from PyDMXControl.profiles.funGeneration import LED_Pot_12_RGBW
from PyDMXControl.profiles.Stairville import LED_Par_10mm, LED_Par_36

dmx = Controller(dynamic_frame=True)

# Fixtures
dmx.add_fixture(LED_Par_10mm)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Par_36)
dmx.add_fixture(LED_Pot_12_RGBW)
dmx.add_fixture(LED_Pot_12_RGBW)


def strobe():
    dmx.all_off()
    Dim.group_apply(dmx.get_all_fixtures(), 50)


def clear():
    dmx.all_locate()
    dmx.clear_all_effects()


# Web Debug
dmx.web_control(
    callbacks={
        "strobe": strobe,
        "clear": clear
    },
    host="0.0.0.0",
    port=80
)

# Web console is now accessible at http://0.0.0.0/ and will have two custom global callbacks for testing.

# Dim all up
dmx.all_locate()

# Done
dmx.sleep_till_enter()
dmx.close()
