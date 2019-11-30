from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH


class Callback(Accessory):
    category = CATEGORY_SWITCH

    def __init__(self, name, callback, driver):
        super().__init__(driver, "Callback " + name)

        serv_switch = self.add_preload_service('Switch', chars=['On'])

        self.callback = callback
        self.state = 0
        serv_switch.configure_char('On', setter_callback=self.set_state, getter_callback=self.get_state,
                                   value=self.state)

    def get_state(self):
        return self.state

    def set_state(self, value):
        if value == 1:
            self.callback()
