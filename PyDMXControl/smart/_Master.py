from colorsys import hsv_to_rgb

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB


class MasterLight(Accessory):
    category = CATEGORY_LIGHTBULB

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service(
            'Lightbulb', chars=['On', 'Hue', 'Saturation', 'Brightness'])

        # Set our instance variables
        self.controller = controller
        self.hue = self.get_hue()  # Hue Value 0 - 360 Homekit API
        self.saturation = self.get_saturation()  # Saturation Values 0 - 100 Homekit API
        self.brightness = self.get_brightness()  # Brightness value 0 - 100 Homekit API

        # Configure our callbacks
        self.char_state = serv_light.configure_char(
            'On', getter_callback=self.get_state)
        self.char_hue = serv_light.configure_char(
            'Hue', setter_callback=self.set_hue, getter_callback=self.get_hue)
        self.char_saturation = serv_light.configure_char(
            'Saturation', setter_callback=self.set_saturation, getter_callback=self.get_saturation)
        self.char_brightness = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness, getter_callback=self.get_brightness)

    @staticmethod
    def get_state():
        return 1

    def set_color(self):
        h = self.hue / 360
        s = self.saturation / 100
        r, g, b = hsv_to_rgb(h, s, 1)
        self.controller.all_color([r * 255, g * 255, b * 255])

    def set_brightness(self, value):
        self.brightness = value
        self.controller.all_dim(self.brightness * 255 / 100)

    @staticmethod
    def get_brightness():
        return 50

    def set_hue(self, value):
        self.hue = value
        self.set_color()

    @staticmethod
    def get_hue():
        return 0

    def set_saturation(self, value):
        self.saturation = value
        self.set_color()

    @staticmethod
    def get_saturation():
        return 100
