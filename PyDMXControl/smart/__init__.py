import signal
from colorsys import hsv_to_rgb

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_LIGHTBULB


class HomeKitLight(Accessory):
    category = CATEGORY_LIGHTBULB

    def __init__(self, fixture, *args, **kwargs):

        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service(
            'Lightbulb', chars=['On', 'Hue', 'Saturation', 'Brightness'])

        self.fixture = fixture

        # Configure our callbacks
        self.char_hue = serv_light.configure_char(
            'Hue', setter_callback=self.set_hue)
        self.char_saturation = serv_light.configure_char(
            'Saturation', setter_callback=self.set_saturation)
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_state)
        self.char_on = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness)

        # Set our instance variables
        self.accessory_state = 0  # State of On/Off
        self.hue = 0  # Hue Value 0 - 360 Homekit API
        self.saturation = 100  # Saturation Values 0 - 100 Homekit API
        self.brightness = 100  # Brightness value 0 - 100 Homekit API

    def set_state(self, value):
        print("state", value)
        self.accessory_state = value
        if value == 1:  # On
            self.set_color()
            self.fixture.dim(self.brightness)
        else:  # Off
            self.fixture.dim(0)

    def set_color(self):
        h = self.hue / 360
        s = self.saturation / 100
        v = 1
        print("hsv", h, s, v)
        r, g, b = hsv_to_rgb(h, s, v)
        print("rgb", r, g, b)
        self.fixture.color([r * 255, g * 255, b * 255])

    def set_brightness(self, value):
        self.brightness = value
        print("bright", value)
        self.fixture.dim(self.brightness * 255 / 100)

    def set_hue(self, value):
        self.hue = value
        print("hue", value)
        self.set_color()

    def set_saturation(self, value):
        self.saturation = value
        print("sat", value)
        self.set_color()


def run(controller):
    start_port = 51826
    driver = AccessoryDriver(port=start_port)
    bridge = Bridge(driver, 'PyDMXControl')

    for i, fixture in enumerate(controller.get_all_fixtures()):
        print(fixture.name)
        bridge.add_accessory(HomeKitLight(fixture, driver, fixture.name))

    signal.signal(signal.SIGTERM, driver.signal_handler)
    driver.add_accessory(accessory=bridge)

    driver.start()
    # thread = Thread(target=driver.start)
    # thread.daemon = True
