[![PyPI](https://img.shields.io/pypi/v/PyDMXControl.svg)](https://pypi.org/project/PyDMXControl/)

# PyDMXControl
![PyDMXControl](brand/PyDMXControl-500x60.png)\
**A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.**

## Installation

Install via pip (recommended)

    pip install PyDMXControl

## Features

* FIXTURE profiles per manufacturer
* EFFECT module/library support
* uDMX works out of the box
* CUSTOM callbacks supported with an internal ticker
* THREADED to allow continuous runtime

## Example

```Python
from PyDMXControl.controllers import uDMXController
from PyDMXControl.profiles.Generic import Dimmer

dmx = uDMXController() # create the controller

fixture = dmx.add_fixture(Dimmer, name="My_First_Dimmer") # add the Dimmer and give it a name for quick reference
fixture.dim(255, 5000) # dim to full over 5 seconds

dmx.debug_control() # enter shell debug mode

dmx.sleep_till_enter() # sleep till enter pressed in shell (once debug mode exited)
dmx.close() # cleanly close PyDMXControl
```

## Ramble
Just messing around with using Python to control/send DMX.\
Supports fixture profiling; Has defaults for a standard fixture and fixtures that need virtual dimmers.\
Prebuilt profiles for generic fixtures (Single dimmer, RGB LED, Custom (set your own number of channels)).

Currently only supports actual output via uDMX.\
There is also a print controller included that prints the DMX frames to console at the same rate it should output them
 to a data cable (this can cause issues though with other things printing as well).

If someone wants to buy me an Enttec USB DMX Pro then I'll try make it work with that too.

Thank you to Dave Hocker, author of [pyudmx](https://github.com/dhocker/udmx-pyusb/), for his work on pyudmx and his
 advice via email in solving some of the issues making this library behave with uDMX.

## Discussion, Support and Issues
For general support and discussion of this project, please join the Discord lounge server: https://discord.gg/qyXqA7y \
[![Discord Server](https://discordapp.com/api/guilds/204663881799303168/widget.png?style=banner2)](https://discord.gg/qyXqA7y)

To check known bugs and see planned changes and features for this project, please see the GitHub issues.\
Found a bug we don't already have an issue for? Please report it in a new GitHub issue with as much detail as you can!
