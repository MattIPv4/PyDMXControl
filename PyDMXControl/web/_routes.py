"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from re import compile  # Regex
from typing import List, Union, Tuple  # Typing

from flask import Blueprint, render_template, current_app, redirect, url_for, request  # Flask

from .. import Colors  # Colors
from ..profiles.defaults import Fixture, Vdim  # Fixtures

routes = Blueprint('', __name__, url_prefix='/')


def fixture_channels(fixture: Fixture) -> List[Tuple[str, int]]:
    chans = [(f['name'], fixture_channel_value(fixture, f['name'])) for f in fixture.channels.values()]
    if issubclass(type(fixture), Vdim):
        chans.append(("dimmer", fixture_channel_value(fixture, "dimmer")))
    return chans


def fixture_channel_value(fixture: Fixture, channel: Union[str, int]) -> int:
    if issubclass(type(fixture), Vdim):
        return fixture.get_channel_value(channel, False)[0]
    return fixture.get_channel_value(channel)[0]


# Home
@routes.route('', methods=['GET'])
def home():
    return render_template("index.jinja2")


# Fixture Home
@routes.route('fixture/<int:fid>', methods=['GET'])
def fixture(fid: int):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return redirect(url_for('.home'))
    return render_template("fixture.jinja2", fixture=fixture, fixture_channels=fixture_channels, colors=Colors)


# Fixture Channel
@routes.route('fixture/<int:fid>/channel/<int:cid>', methods=['GET', 'POST'])
def channel(fid: int, cid: int):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return redirect(url_for('.home'))
    cid = fixture.get_channel_id(cid)
    if cid == -1:
        return redirect(url_for('.fixture', fid=fixture.id))

    if request.method == 'POST':
        data = request.form
        if 'value' in data:
            data = data['value']
            try:
                data = int(data)
            except:
                pass
            else:
                if 255 >= data >= 0:
                    fixture.set_channel(cid, data)

    channel = fixture_channels(fixture)[cid]
    return render_template("channel.jinja2", fixture=fixture, channel=channel, cid=cid)


# Fixture Color
@routes.route('fixture/<int:fid>/color/<string:val>', methods=['GET'])
def color(fid: int, val: str):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return redirect(url_for('.home'))
    pattern = compile("^\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*(?:[, ]\s*(\d{1,3})\s*)*$")
    match = pattern.match(val)
    if match:
        color = [int(f) for f in match.groups() if f]
        fixture.color(color)
    return redirect(url_for('.fixture', fid=fixture.id))


# Callbacks
@routes.route('callback/<string:cb>', methods=['GET'])
def callback(cb: str):
    if cb in current_app.parent.callbacks.keys():
        current_app.parent.callbacks[cb]()
    return redirect(url_for('.home'))
