"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from re import compile  # Regex
from typing import List, Union, Tuple, Dict, Callable  # Typing

from flask import Blueprint, render_template, current_app, redirect, url_for, jsonify  # Flask

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


helpers = ["on", "off", "locate"]


def fixture_helpers(fixture: Fixture) -> Dict[str, Callable]:
    return {f: fixture.__getattribute__(f) for f in helpers if hasattr(fixture, f)}


# Home
@routes.route('', methods=['GET'])
def home():
    return render_template("index.jinja2", helpers=helpers)


# Fixture Home
@routes.route('fixture/<int:fid>', methods=['GET'])
def fixture(fid: int):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return redirect(url_for('.home'))
    return render_template("fixture.jinja2", fixture=fixture, fixture_channels=fixture_channels,
                           colors=Colors, helpers=helpers)


# Fixture Channel
@routes.route('fixture/<int:fid>/channel/<int:cid>', methods=['GET'])
def channel(fid: int, cid: int):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return redirect(url_for('.home'))
    chan = fixture.get_channel_id(cid)
    if chan == -1:
        return redirect(url_for('.fixture', fid=fixture.id))
    channel = fixture_channels(fixture)[chan]
    return render_template("channel.jinja2", fixture=fixture, channel=channel, cid=chan)


# Fixture Channel Set
@routes.route('fixture/<int:fid>/channel/<int:cid>/<int:val>', methods=['GET'])
def channel_val(fid: int, cid: int, val: int):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404
    chan = fixture.get_channel_id(cid)
    if chan == -1:
        return jsonify({"error": "Channel {} not found".format(cid)}), 404

    if val < 0 or val > 255:
        return jsonify({"error": "Value {} is invalid".format(val)}), 400

    fixture.set_channel(chan, val)
    val = fixture_channel_value(fixture, chan)
    return jsonify({"message": "Channel updated to {}".format(val), "elements": {
        "channel-{}-value".format(chan): val,
        "value": val
    }}), 200


# Fixture Color
@routes.route('fixture/<int:fid>/color/<string:val>', methods=['GET'])
def color(fid: int, val: str):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404
    pattern = compile("^\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*(?:[, ]\s*(\d{1,3})\s*)*$")
    match = pattern.match(val)
    if not match:
        return jsonify({"error": "Invalid color {} supplied".format(val)}), 400
    color = [int(f) for f in match.groups() if f]
    fixture.color(color)
    return jsonify({"message": "Color updated to {}".format(color), "elements":
        dict({"value": Colors.to_hex(fixture.get_color())}, **{
            "channel-{}-value".format(i): f[1] for i, f in enumerate(fixture_channels(fixture))
        })}), 200


# Fixture Helpers
@routes.route('fixture/<int:fid>/helper/<string:val>', methods=['GET'])
def helper(fid: int, val: str):
    fixture = current_app.parent.controller.get_fixture(fid)
    if not fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404

    val = val.lower()
    help = fixture_helpers(fixture)
    if val not in help.keys():
        return jsonify({"error": "Helper {} not found".format(val)}), 404

    try:
        help[val]()
    except:
        return jsonify({"error": "Helper {} failed to execute".format(val)}), 500
    return jsonify({"message": "Helper {} executed".format(val), "elements":
        dict({"value": Colors.to_hex(fixture.get_color())}, **{
            "channel-{}-value".format(i): f[1] for i, f in enumerate(fixture_channels(fixture))
        })}), 200


# Callbacks
@routes.route('callback/<string:cb>', methods=['GET'])
def callback(cb: str):
    if cb not in current_app.parent.callbacks.keys():
        return jsonify({"error": "Callback {} not found".format(cb)}), 404
    try:
        current_app.parent.callbacks[cb]()
    except:
        return jsonify({"error": "Callback {} failed to execute".format(cb)}), 500
    return jsonify({"message": "Callback {} executed".format(cb)}), 200
