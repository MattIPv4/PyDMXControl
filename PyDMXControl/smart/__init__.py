import signal
from threading import Thread

from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver

from ._Master import MasterDimmer,  MasterColor
from ._RGB import RGBLight
from ._Callback import Callback

driver = None


def run(controller, callbacks=None):
    if callbacks is None:
        callbacks = {}

    global driver
    if driver is not None: return

    driver = AccessoryDriver()

    bridge = Bridge(driver, 'PyDMXControl')
    bridge.set_info_service(manufacturer="PyDMXControl",
                            model="Central Controller",
                            serial_number="Chans: 1->{} (All)".format(controller.next_channel - 1))

    for fixture in controller.get_all_fixtures():
        bridge.add_accessory(RGBLight(fixture, driver))

    bridge.add_accessory(MasterDimmer(controller, driver))
    bridge.add_accessory(MasterColor(controller, driver))

    for name, callback in callbacks.items():
        bridge.add_accessory(Callback(name, callback, driver))

    signal.signal(signal.SIGTERM, driver.signal_handler)
    driver.add_accessory(bridge)

    thread = Thread(target=driver.start)
    thread.daemon = True
    thread.start()


def stop():
    global driver
    if driver is None: return
    driver.stop()
