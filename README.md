<!-- Source: https://github.com/MattIPv4/template/blob/master/README.md -->

<!-- Title -->
<h1 align="center" id="PyDMXControl">
    <img src="https://raw.githubusercontent.com/MattIPv4/PyDMXControl/master/brand/PyDMXControl-500x60.png" alt="PyDMXControl" width="500"/>
</h1>

<!-- Tag line -->
<h3 align="center">A Python 3 module to control DMX using uDMX - Featuring fixture profiles, built-in effects and a web control panel.</h3>

<!-- Badges -->
<p align="center">
    <a href="https://pypi.org/project/PyDMXControl/">
        <img src="https://img.shields.io/pypi/v/PyDMXControl.svg?style=flat-square&colorB=4a89dc" alt="PyPi Version">
    </a>
    <a href="https://github.com/MattIPv4/PyDMXControl/tree/master/LICENSE">
        <img src="https://img.shields.io/pypi/l/PyDMXControl.svg?style=flat-square&colorB=4a89dc" alt="License">
    </a>
    <a href="https://pypi.org/project/PyDMXControl/">
        <img src="https://img.shields.io/pypi/pyversions/PyDMXControl.svg?style=flat-square&colorB=4a89dc" alt="Python Versions">
    </a>
    <a href="https://github.com/MattIPv4/PyDMXControl/tree/master/PyDMXControl">
        <img src="https://img.shields.io/github/languages/code-size/MattIPv4/PyDMXControl.svg?style=flat-square&colorB=4a89dc" alt="Code Size">
    </a>
    <a href="http://patreon.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/patreon-IPv4-blue.svg?style=flat-square&colorB=4a89dc" alt="Patreon"/>
    </a>
    <a href="http://slack.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/slack-MattIPv4-blue.svg?style=flat-square&colorB=4a89dc" alt="Slack"/>
    </a>
</p>

<p align="center">
    <a href="https://scrutinizer-ci.com/g/MattIPv4/PyDMXControl/">
        <img src="https://img.shields.io/scrutinizer/g/MattIPv4/PyDMXControl.svg?style=flat-square&label=scrutinizer%20quality" alt="Scrutinizer Code Quality">
    </a>
    <a href="https://scrutinizer-ci.com/g/MattIPv4/PyDMXControl/">
        <img src="https://img.shields.io/scrutinizer/build/g/MattIPv4/PyDMXControl.svg?style=flat-square" alt="Build Status">
    </a>
    <a href="https://www.codacy.com/app/MattIPv4/PyDMXControl">
        <img src="https://img.shields.io/codacy/grade/18b92886857641e685584aaab9b492e2.svg?style=flat-square&label=codacy%20quality" alt="Codacy Code Quality">
    </a>
</p>

<!-- Custom Extra Logo -->
<img src="https://raw.githubusercontent.com/MattIPv4/PyDMXControl/master/brand/PyDMXControl_icon-500x500.png" alt="PyDMXControl Icon" align="right" width="150"/>

----

<!-- Content -->
## Installation

Install via pip **(recommended)**

    pip install -U PyDMXControl
    
Install via pip **with audio support**

    pip install -U PyDMXControl[audio]
    
Install via GitHub **(development version, with audio)**

    pip install -U git+https://github.com/MattIPv4/PyDMXControl#egg=PyDMXControl[audio]

## Features

  * FIXTURE profiles per manufacturer ([see all included profiles](https://github.com/MattIPv4/PyDMXControl/tree/master/PyDMXControl/profiles))
    * Generic dimmer fixture included, single channel
    * RGB (3-channel) fixture with virtual dimmer built-in


  * EFFECT module/library support ([see all packaged effects](https://github.com/MattIPv4/PyDMXControl/tree/master/PyDMXControl/effects))
    * Intensity dim chase provided, configurable speed and offset provided
    * Included is a fixture color chase effect, unlimited number of colors supported
    * Effects can be applied to individual fixtures or multiple as a group
    * [Demo: tests/effects.py](https://github.com/MattIPv4/PyDMXControl/blob/master/tests/effects.py)
  
  
  * uDMX works out of the box
    * Package developed on and tested extensively with a uDMX system
  
  
  * CUSTOM callbacks supported with an internal ticker
    * Have actions take place on their own at certain times using the callback ticker
  
  
  * THREADED to allow continuous runtime
    * Run your own blocking scripts whilst PyDMXControl continues to output data
  
  
  * WEBSITE control panel built in
    * Global and individual fixture intensity control via sliders
    * Quick access to callback functions globally and for each fixture
    * Color picker for individual fixtures as well as specific channel control
    * [Demo: tests/web.py](https://github.com/MattIPv4/PyDMXControl/blob/master/tests/web.py)
  
 
  * JSON fixture configurations
    * Load fixture configurations from JSON files into the controller
    * Save your current set of fixtures out to JSON files for later use
    * [Demo: tests/json_config.py](https://github.com/MattIPv4/PyDMXControl/blob/master/tests/json_config.py)
  

  * Optional AUDIO playback supported
    * Play audio tracks whilst PyDMXControl continues to run lighting control
    * Uses pygame for best cross-platform and audio format support
    * [Demo: tests/audio.py](https://github.com/MattIPv4/PyDMXControl/blob/master/tests/audio.py)

## Example Usage

An example of how to get a single dimmer working with PyDMXControl, 
providing the web control panel and the console debug system once started.

```python
# Import the uDMX controller from PyDMXControl,
#  this will be how the data is outputted.
from PyDMXControl.controllers import uDMXController

# Import the fixture profile we will use,
#  the simple Dimmer in this example.
from PyDMXControl.profiles.Generic import Dimmer

# Create an instance of the uDMX controller, 
#  this holds all the fixture information and outputs it.
# This will start outputting data immediately.
dmx = uDMXController()

# Add a new Dimmer fixture to our controller
#  and save it to a variable so we can access it.
# We give it a name so it's easier to identify in the debug control options.
fixture = dmx.add_fixture(Dimmer, name="My_First_Dimmer")

# Next, dim the intensity of the fixture from it's initial value of zero
#  to full, which is represented as 255 in DMX.
# This is done over 5000 milliseconds, or 5 seconds.
fixture.dim(255, 5000)

# We can now start the web control panel built into PyDMXControl.
# This will output the web address in console, but should be http://0.0.0.0:8080
# This runs in the background and so we can continue to do other things still.
dmx.web_control()

# The console debug mode can also be started if required,
#  this provides basic control options in the console of the program.
# This is blocking however and so the script will not continue past here until
#  the debug control is exited. This won't stop DMX output.
dmx.debug_control()

# Once the console debug mode is exited the script will continue, to stop it
#  exiting and stopping DMX output when can use a built-in sleep function.
# This sleep function will wait until enter is pressed in the console before continuing.
dmx.sleep_till_enter()

# With everything done, you can terminate the DMX output and the program by calling
#  the close method of the controller.
# This will cleanly close any threads in use and stop DMX output.
dmx.close()

```

> For a "real life" example, please take a look at [tests/home.py](https://github.com/MattIPv4/PyDMXControl/tree/master/tests/home.py) which is the setup I use in my office.

Browse the tests from the [tests folder](https://github.com/MattIPv4/PyDMXControl/tree/master/tests/) to see examples of other features within the library being tested out.

## What is the point of this?

Just messing around with using Python to control/send DMX.\
Supports fixture profiling; Has defaults for a standard fixture and fixtures that need virtual dimmers.\
Prebuilt profiles for generic fixtures (Single dimmer, RGB LED, Custom (set your own number of channels)).

Has a debug shell that allows control of fixture channel values and access to general callbacks. Additionally, provides 
an advanced web control panel with access to global callbacks, fixture helpers, fixture colors and control over 
individual fixture channels.

Currently only supports actual output via uDMX.\
There is also a print controller included that prints the DMX frames to console at the same rate it should output them
 to a data cable (this can cause issues though with other things printing as well).

If someone wants to buy me an Enttec USB DMX Pro then I'll try make it work with that too.

Thank you to Dave Hocker, author of [pyudmx](https://github.com/dhocker/udmx-pyusb/), for his work on pyudmx and his
 advice via email in solving some of the issues making this library behave with uDMX.

<!-- Contributing -->
## Contributing

Contributions are always welcome to this project!\
Take a look at any existing issues on this repository for starting places to help contribute towards, or simply create your own new contribution to the project.

Please make sure to follow the existing standards within the project such as code styles, naming conventions and commenting/documentation.

When you are ready, simply create a pull request for your contribution and I will review it whenever I can!

### Donating

You can also help me and the project out by contributing through a donation on PayPal or by supporting me monthly on my Patreon page.
<p>
    <a href="http://patreon.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/patreon-IPv4-blue.svg?logo=patreon&logoWidth=30&logoColor=F96854&style=popout-square" alt="Patreon"/>
    </a>
    <a href="http://paypal.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/paypal-Matt%20(IPv4)%20Cowley-blue.svg?logo=paypal&logoWidth=30&logoColor=00457C&style=popout-square" alt="PayPal"/>
    </a>
</p>

<!-- Discussion & Support -->
## Discussion, Support and Issues

Need support with this project, have found an issue or want to chat with others about contributing to the project?
> Please check the project's issues page first for support & bugs!

Not found what you need here?
* If you have an issue, please create a GitHub issue here to report the situation, include as much detail as you can!
* _or,_ You can join our Slack workspace to discuss any issue, to get support for the project or to chat with contributors and myself:
<a href="http://slack.mattcowley.co.uk/" target="_blank">
    <img src="https://img.shields.io/badge/slack-MattIPv4-blue.svg?logo=slack&logoWidth=30&logoColor=blue&style=popout-square" alt="Slack" height="60">
</a>
