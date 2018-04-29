# PyDMXControl
A Python 3.6 module to control DMX via Python. Featuring fixture profiles and working with uDMX. 

Just messing around with using Python to control/send DMX.
Supports fixture profiling. Has defaults for a standard fixture and fixtures that need virtual dimmers.
Prebuilt profiles for generic fixtures (Single dimmer, RGB LED, Custom [set your own number of channels]).

Currently only supports actual output via uDMX (I still need to test this). There is also a print controller included that prints the DMX frames to console at the same rate it should output them to a data cable (this can cause issues though with other things printing as well).

If someone wants to buy me an Enttec USB DMX Pro then I'll try make it work with that too.
