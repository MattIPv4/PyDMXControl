from colorsys import hsv_to_rgb

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB


class MasterDimmer(Accessory):
    category = CATEGORY_LIGHTBULB

    def __init__(self, controller, driver):
        super().__init__(driver, "Global Dimmer")

        serv_light = self.add_preload_service(
            'Lightbulb', chars=['On', 'Brightness'])

        # Set our instance variables
        self.controller = controller
        self.brightness = 50  # Brightness value 0 - 100 Homekit API

        # Configure our callbacks
        self.char_state = serv_light.configure_char(
            'On', setter_callback=self.set_state, value=1)
        self.char_brightness = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness, value=self.brightness)

        # Set model info
        self.set_info_service(manufacturer="PyDMXControl",
                              model="Global Dimmer",
                              serial_number="Chans: 1->{} (All)".format(controller.next_channel - 1))

    def set_state(self, value):
        if value == 1:  # On
            self.set_brightness(100)
        else:  # Off
            self.set_brightness(0)

    def set_brightness(self, value):
        self.brightness = value
        self.controller.all_dim(self.brightness * 255 / 100)


class MasterColor(Accessory):
    category = CATEGORY_LIGHTBULB

    def __init__(self, controller, driver):
        super().__init__(driver, "Global Color")

        serv_light = self.add_preload_service(
            'Lightbulb', chars=['On', 'Hue', 'Saturation'])

        # Set our instance variables
        self.controller = controller
        self.state = 1
        self.hue = 0  # Hue Value 0 - 360 Homekit API
        self.saturation = 0  # Saturation Values 0 - 100 Homekit API

        # Configure our callbacks
        self.char_state = serv_light.configure_char(
            'On', getter_callback=self.get_state, value=self.state)
        self.char_hue = serv_light.configure_char(
            'Hue', setter_callback=self.set_hue, getter_callback=self.get_hue)
        self.char_saturation = serv_light.configure_char(
            'Saturation', setter_callback=self.set_saturation, getter_callback=self.get_saturation)

        # Set model info
        self.set_info_service(manufacturer="PyDMXControl",
                              model="Global Color",
                              serial_number="Chans: 1->{} (All)".format(controller.next_channel - 1))

    def get_state(self):
        return self.state

    def set_color(self):
        h = self.hue / 360
        s = self.saturation / 100
        r, g, b = hsv_to_rgb(h, s, 1)
        self.controller.all_color([r * 255, g * 255, b * 255])

    def get_hue(self):
        return self.hue

    def set_hue(self, value):
        self.hue = value
        self.set_color()

    def get_saturation(self):
        return self.saturation

    def set_saturation(self, value):
        self.saturation = value
        self.set_color()
