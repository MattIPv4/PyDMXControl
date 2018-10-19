"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
 *
 *  This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published
 *   by the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *  This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *  You should have received a copy of the GNU General Public License
 *   along with this program. If not, please see
 *   <https://github.com/MattIPv4/PyDMXControl/blob/master/LICENSE> or <http://www.gnu.org/licenses/>.
"""

from setuptools import setup

from PyDMXControl import __version__

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="PyDMXControl",
    author="MattIPv4",
    url="https://github.com/MattIPv4/PyDMXControl/",
    version=__version__,
    packages=["PyDMXControl"],
    python_requires=">= 3.5",
    include_package_data=True,
    install_requires=requirements,
    description="A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="lighting light lights "
             "fixtures fixture-profiles "
             "controller control control-dmx "
             "dmx dmx-512 dmx-interface dmx-channels dmx-dimmer dmx-library "
             "theatre udmx",
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",

        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",

        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Flask",

        "Natural Language :: English",
        "Operating System :: OS Independent",

        "Topic :: Home Automation",
        "Topic :: Internet",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ),
    project_urls={
        "Source": "https://github.com/MattIPv4/PyDMXControl/tree/master",
        "Funding": "http://patreon.mattcowley.co.uk/",
        "Patreon": "http://patreon.mattcowley.co.uk/",
        "Support": "http://discord.mattcowley.co.uk/",
        "Discord": "http://discord.mattcowley.co.uk/",
    },
)

# How2Ship:tm:
# 1. Update version in PyDMXControl/__init__.py
# 2. Run python3 setup.py sdist bdist_wheel bdist_egg
# 3. Run python3 -m twine upload dist/*
