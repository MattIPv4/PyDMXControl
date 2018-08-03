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
import re

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

with open("README.md", "r") as f:
    readme = f.read()

with open("PyDMXControl/__init__.py", "r") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

setup(
    name="PyDMXControl",
    author="MattIPv4",
    url="https://github.com/MattIPv4/PyDMXControl/",
    version=version,
    packages=['PyDMXControl'],
    python_requires=">= 3.5",
    include_package_data=True,
    install_requires=requirements,
    description='A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="lighting light lights control dmx theatre fixtures udmx",
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
    project_urls={
        'Funding': 'http://patreon.mattcowley.co.uk/',
        'Support': 'http://discord.mattcowley.co.uk/',
        'Source': 'https://github.com/MattIPv4/PyDMXControl/',
    },
)

# How2Ship:tm:
# 1. Update version in PyDMXControl/__init__.py
# 2. Run python3 setup.py sdist bdist_wheel bdist_egg
# 3. Run python3 -m twine upload dist/*
