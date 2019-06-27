import signal
from threading import Thread

from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver

from ._Master import MasterLight
from ._RGB import RGBLight

driver = None


def run(controller):
    global driver
    if driver is not None: return

    driver = AccessoryDriver()
    bridge = Bridge(driver, 'PyDMXControl')

    for fixture in controller.get_all_fixtures():
        bridge.add_accessory(RGBLight(fixture, driver, fixture.name))

    bridge.add_accessory(MasterLight(controller, driver, "Master"))

    signal.signal(signal.SIGTERM, driver.signal_handler)
    driver.add_accessory(accessory=bridge)

    thread = Thread(target=driver.start)
    thread.daemon = True
    thread.start()


def stop():
    global driver
    if driver is None: return
    driver.stop()
