"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2019 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
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

from typing import List

from setuptools import setup, find_packages

from PyDMXControl import __title__, __author__, __email__, __license__, __version__


def fetch_reqs(base: str = "") -> List[str]:
    if base:
        base = "PyDMXControl/{}/".format(base)
    with open(base + "requirements.txt", "r") as file:
        requirements = file.read().splitlines()
    return requirements


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=__title__,
    author=__author__,
    author_email=__email__,
    url="https://github.com/MattIPv4/PyDMXControl/",
    version=__version__,
    license=__license__,
    packages=find_packages(exclude=("tests",)),
    python_requires=">= 3.6",
    include_package_data=True,
    install_requires=fetch_reqs(),
    extras_require={
        "audio": fetch_reqs("audio")
    },
    description="A Python 3 module to control DMX using uDMX."
                " Featuring fixture profiles, built-in effects and a web control panel.",
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
        "Issues": "https://github.com/MattIPv4/PyDMXControl/issues",
        "Slack": "http://slack.mattcowley.co.uk/",
    },
)

# How2Ship:tm:
# 1. Update version in PyDMXControl/__init__.py
# 2. Run python3 setup.py sdist bdist_wheel bdist_egg
# 3. Run python3 -m twine upload dist/*
