from colorsys import hsv_to_rgb, rgb_to_hsv

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB


class RGBLight(Accessory):
    category = CATEGORY_LIGHTBULB

    def __init__(self, fixture, *args, **kwargs):

        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service(
            'Lightbulb', chars=['On', 'Hue', 'Saturation', 'Brightness'])

        # Set our instance variables
        self.fixture = fixture
        self.accessory_state = self.get_state()  # State of On/Off
        self.hue = self.get_hue()  # Hue Value 0 - 360 Homekit API
        self.saturation = self.get_saturation()  # Saturation Values 0 - 100 Homekit API
        self.brightness = self.get_brightness()  # Brightness value 0 - 100 Homekit API

        # Configure our callbacks
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_state, getter_callback=self.get_state)
        self.char_hue = serv_light.configure_char(
            'Hue', setter_callback=self.set_hue, getter_callback=self.get_hue)
        self.char_saturation = serv_light.configure_char(
            'Saturation', setter_callback=self.set_saturation, getter_callback=self.get_saturation)
        self.char_brightness = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness, getter_callback=self.get_brightness)

    def set_state(self, value):
        self.accessory_state = value
        if value == 1:  # On
            self.set_brightness(100)
        else:  # Off
            self.set_brightness(0)

    def get_state(self):
        self.accessory_state = 1 if self.get_brightness() > 0 else 0
        return self.accessory_state

    def set_color(self):
        h = self.hue / 360
        s = self.saturation / 100
        r, g, b = hsv_to_rgb(h, s, 1)
        self.fixture.color([r * 255, g * 255, b * 255])

    def get_color(self):
        return self.fixture.get_color()[:3]

    def set_brightness(self, value):
        self.accessory_state = 1 if value > 0 else 0
        self.brightness = value
        self.fixture.dim(self.brightness * 255 / 100)

    def get_brightness(self):
        return self.fixture.get_channel_value(self.fixture.get_channel_id("dimmer"))[0] * 100 / 255

    def set_hue(self, value):
        self.hue = value
        self.set_color()

    def get_hue(self):
        h, s, v = rgb_to_hsv(*self.get_color())
        return h * 360

    def set_saturation(self, value):
        self.saturation = value
        self.set_color()

    def get_saturation(self):
        h, s, v = rgb_to_hsv(*self.get_color())
        return s * 100
