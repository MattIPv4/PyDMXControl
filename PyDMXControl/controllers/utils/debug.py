"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from collections import namedtuple
from inspect import signature, Parameter
from re import compile as re_compile
from typing import List, Tuple, Union, Dict, Callable

from ... import Colors
from ...profiles.defaults import Fixture, Vdim


class Debugger:

    def __init__(self, controller: 'Controller', callbacks: Dict[str, Callable] = None):
        self.cont = controller
        self.cbs = {} if callbacks is None else callbacks

    def __default_callbacks(self):
        # Some default callbacks
        if 'all_on' not in self.cbs:
            self.cbs['all_on'] = self.cont.all_on
        if 'on' not in self.cbs:
            self.cbs['on'] = self.cont.all_on

        if 'all_off' not in self.cbs:
            self.cbs['all_off'] = self.cont.all_off
        if 'off' not in self.cbs:
            self.cbs['off'] = self.cont.all_off

        if 'all_locate' not in self.cbs:
            self.cbs['all_locate'] = self.cont.all_locate
        if 'locate' not in self.cbs:
            self.cbs['locate'] = self.cont.all_locate

    def __check_callbacks(self):
        for key in self.cbs.keys():
            if not self.cbs[key] or not callable(self.cbs[key]):
                del self.cbs[key]

    @staticmethod
    def __callbacks_parameters(parameters: List[Parameter]) -> Tuple[list, dict]:
        # Given params
        ordered_params = []
        keyword_params = {}

        # Go through all params
        for param in parameters:
            # Basic param information
            has_default = (param.default != Parameter.empty)
            has_type = (param.annotation != Parameter.empty)
            param_type = str(param.annotation) if has_type else "Unknown"
            param_default = (", leave blank for default " + str(param.default)) if has_default else ""

            # Validate the parameter input
            given_param = False

            def valid(this):
                # Not started
                if this is None:
                    return False

                # Default?
                if this.strip() == "":
                    if has_default:
                        return param.default
                    return False

                # Normal
                try:
                    return param.annotation(this)
                except Exception:
                    return this

            # Get input
            while given_param is False:
                given_param = valid(input(
                    "[Callbacks Debug] Parameter '" + param.name + "' (expects " + param_type + param_default + "): "))

            # Add to return
            if param.kind == Parameter.POSITIONAL_ONLY:
                ordered_params.append(given_param)
            else:
                keyword_params[param.name] = given_param

        return ordered_params, keyword_params

    def run_callbacks(self):
        # Defaults
        self.__default_callbacks()
        self.__check_callbacks()

        # Give callbacks
        print("\n[Callbacks Debug] Available callbacks:",
              ", ".join(["'" + f + "'" for f in self.cbs.keys()]))
        while True:
            # Selection
            callback = input("\n[Callbacks Debug] Callback Name (or 'exit'): ").strip()

            # Allow exit
            if callback == 'exit':
                break

            # Check it exists
            if callback not in self.cbs:
                continue

            # Run the callback
            cb = self.cbs[callback]
            try:
                # Get all parameters
                params = signature(cb).parameters.values()
                ordered, keyword = self.__callbacks_parameters(params)

                # Run
                res = cb(*ordered, **keyword)
            except Exception as e:
                print(e)
                print("[Callbacks Debug] '" + callback + "' failed.")
            else:
                print("[Callbacks Debug] Callback '" + callback + "' succeed and returned:", res)

    @staticmethod
    def __fixture_channels(fixture: Fixture) -> List[str]:
        names = ["'" + f['name'] + "'" for f in fixture.channels.values()]
        if issubclass(type(fixture), Vdim):
            names.append("'dimmer'")
        return names

    @staticmethod
    def __fixture_channel_value(fixture: Fixture, channel: Union[str, int]) -> int:
        if issubclass(type(fixture), Vdim):
            return fixture.get_channel_value(channel, False)[0]
        return fixture.get_channel_value(channel)[0]

    @staticmethod
    def run_fixture_color(fixture: Fixture):
        # Select
        select = input("\n[Fixture Debug] Color Name: ").strip().lower()

        # Try finding enum
        color = [c for c in Colors if c.name.lower() == select]

        # If not enum, try regex, else fetch enum
        if not color:
            pattern = re_compile(
                r"^\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*(?:[, ]\s*(\d{1,3})\s*)*$")
            match = pattern.match(select)
            if not match:
                return
            color = {"name": "User Input", "value": [int(f) for f in match.groups() if f]}
            color = namedtuple("Color", color.keys())(*color.values())
        else:
            color = color[0]

        # Apply
        fixture.color(color.value)
        print("[Fixture Debug] Color set to " + color.name + " (" + Colors.to_print(color.value) + ")")

    def run_fixture_channel(self, fixture: Fixture):
        # Select
        channel = input("\n[Channel Debug] Channel Number/Name: ").strip()

        # Find
        channel = fixture.get_channel_id(channel)

        # Abort if not found
        if channel == -1:
            return

        # Value
        value = str(self.__fixture_channel_value(fixture, channel))
        value = input("[Channel Debug] Channel Value (Currently " + value + ", leave blank to abort): ").strip()

        # Abort if bad value
        if value == "":
            return
        if not value.isdigit():
            return

        # Apply
        value = int(value)
        fixture.set_channel(channel, value)
        print("[Channel Debug] Channel '" + str(channel) + "' set to " + str(
            self.__fixture_channel_value(fixture, channel)))

    def run_fixture(self):
        fixture = input("\n[Fixture Debug] Fixture ID/Name: ").strip()

        # Find the fixture
        if not fixture.isdigit():
            fixture = self.cont.get_fixtures_by_name(fixture)
            if fixture:
                fixture = fixture[0]
        else:
            fixture = self.cont.get_fixture(int(fixture))
        if not fixture:
            return

        # Fixture debug control
        print("\n[Fixture Debug] Fixture selected:", fixture)
        while True:

            # Selection
            select = input("\n[Fixture Debug] '1': Channel Select by Number/Name"
                           "\n            '2': Channel List"
                           "\n            '3': Color (if fixture supports)"
                           "\n            '4': Color List"
                           "\n            '5': Exit"
                           "\nSelection: ").strip()

            # Channel number/name
            if select == '1':
                self.run_fixture_channel(fixture)
                continue

            # Channel list
            if select == '2':
                print("\n[Fixture Debug] Channel List:", ", ".join(self.__fixture_channels(fixture)))
                continue

            # Color select
            if select == '3':
                self.run_fixture_color(fixture)
                continue

            # Color list
            if select == '4':
                print("\n[Fixture Debug] Color List:", ", ".join([color.name for color in Colors]))
                continue

            # Exit
            if select == '5':
                break

    def run(self):
        # DMX debug control
        print("[DMX Debug] Currently operating in channels: {}".format("1->{}.".format(self.cont.next_channel - 1) if
                                                                       self.cont.next_channel > 1 else "None"))
        while True:
            # Selection
            select = input("\n[DMX Debug] '1': Fixture Select by ID/Name"
                           "\n            '2': Fixture List"
                           "\n            '3': Callbacks"
                           "\n            '4': Exit"
                           "\nSelection: ").strip()

            # Fixture id/name
            if select == '1':
                self.run_fixture()
                continue

            # Fixture list
            if select == '2':
                # Compile list
                fixtures = []
                for f in self.cont.get_all_fixtures():
                    fixtures.extend(["\n", f])
                # Output
                print("\n[DMX Debug] Fixture List:", *fixtures)
                continue

            # Callbacks
            if select == '3':
                self.run_callbacks()
                continue

            # Exit
            if select == '4':
                break
