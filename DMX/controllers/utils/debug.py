from inspect import signature, Parameter
from typing import List, Tuple, Union

from DMX.profiles.defaults import Fixture, Vdim


class Debugger:

    def __init__(self, controller: 'Controller', callbacks: dict = None):
        self.cont = controller
        self.cbs = {} if callbacks is None else callbacks

    def __default_callbacks(self):
        # Some default callbacks
        if not 'all_on' in self.cbs: self.cbs['all_on'] = self.cont.all_on
        if not 'on' in self.cbs: self.cbs['on'] = self.cont.all_on

        if not 'all_off' in self.cbs: self.cbs['all_of'] = self.cont.all_off
        if not 'off' in self.cbs: self.cbs['off'] = self.cont.all_off

        if not 'all_locate' in self.cbs: self.cbs['all_locate'] = self.cont.all_locate
        if not 'locate' in self.cbs: self.cbs['locate'] = self.cont.all_locate

    def __check_callbacks(self):
        for key in self.cbs.keys():
            if not self.cbs[key] or not callable(self.cbs[key]):
                del self.cbs[key]

    def __callbacks_parameters(self, parameters: List[Parameter]) -> Tuple[list, dict]:
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
                if this is None: return False

                # Default?
                if this.strip() == "":
                    if has_default:
                        return param.default
                    else:
                        return False

                # Normal
                try:
                    return param.annotation(this)
                except:
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
        print("[Callbacks Debug] Available callbacks:",
              ", ".join(["'" + f + "'" for f in self.cbs.keys()]))
        while True:
            # Selection
            callback = input("[Callbacks Debug] Callback Name (or 'exit'): ").strip()

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

        return

    def __fixture_channels(self, fixture: Fixture) -> List[str]:
        names = ["'" + f['name'] + "'" for f in fixture.channels.values()]
        print(issubclass(type(fixture), Vdim))
        if issubclass(type(fixture), Vdim):
            names.append("'dimmer'")
        return names

    def __fixture_channel_value(self, fixture: Fixture, channel: Union[str, int]) -> int:
        if issubclass(type(fixture), Vdim):
            return fixture.get_channel_value(channel, False)[0]
        return fixture.get_channel_value(channel)[0]

    def run_fixture(self, fixture: str):
        # Find the fixture
        if not fixture.isdigit():
            fixture = self.cont.get_fixtures_by_name(fixture)
            if fixture: fixture = fixture[0]
        else:
            fixture = self.cont.get_fixture(int(fixture))
        if not fixture:
            return

        # Fixture debug control
        print("[Fixture Debug] Fixture selected:", fixture)
        # Give Channels
        print("[Fixture Debug] Available channels:",
              ", ".join(self.__fixture_channels(fixture)))
        while True:

            # Channel selection / exit fixture debug
            channel = input("[Fixture Debug] Channel Number/Name (or 'exit'): ").strip()
            if channel == 'exit':
                break
            channel = fixture.get_channel_id(channel)
            if channel == -1:
                continue
            value = str(self.__fixture_channel_value(fixture, channel))
            value = input("[Fixture Debug] Channel Value (Currently " + value + ", leave blank to abort): ").strip()
            if value == "":
                continue
            if not value.isdigit():
                continue
            value = int(value)
            fixture.set_channel(channel, value)

        return

    def run(self):
        # DMX debug control
        print("[DMX Debug] Currently operating in channels: 1->{}.".format(self.cont.next_channel - 1))
        while True:
            # Selection
            fixture = input("[DMX Debug] Fixture ID/Name or 'callbacks' (or 'exit'): ").strip()

            # Allow exit
            if fixture == 'exit':
                break

            # Callback control
            if fixture == 'callbacks':
                self.run_callbacks()
                continue

            # Fixture control
            self.run_fixture(fixture)

        return
