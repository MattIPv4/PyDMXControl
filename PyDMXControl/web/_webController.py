"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2022 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

import builtins  # Builtins for Jinja context
import logging  # Logging
from os import path  # OS Path
from typing import Dict, Callable  # Typing

from flask import Flask  # Flask
from werkzeug.serving import make_server  # Flask server

from ._routes import routes  # Web Routes
from ..utils import ExceptionThread  # Threading
from ..utils.timing import TimedEvents  # Timed Events

# Set error only logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class ServerThread(ExceptionThread):

    def __init__(self, host, port, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print("Started web controller: http://{}:{}".format(self.srv.host, self.srv.port))
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


# WebController
class WebController:

    def __init__(self, controller: 'Controller', *,
                 callbacks: Dict[str, Callable] = None,
                 timed_events: Dict[str, TimedEvents] = None,
                 host: str = "0.0.0.0", port: int = 8080):

        # Setup flask
        self.__thread = None
        self.__host = host
        self.__port = port
        self.__app = Flask("PyDMXControl Web Controller")
        self.__app.template_folder = path.dirname(__file__) + "/templates"
        self.__app.static_url_path = "/static"
        self.__app.static_folder = path.dirname(__file__) + "/static"
        self.__app.register_blueprint(routes)
        self.__app.parent = self

        # Setup controller
        self.controller = controller

        # Setup callbacks
        self.callbacks = {} if callbacks is None else callbacks
        self.__default_callbacks()
        self.__check_callbacks()

        # Setup timed events
        self.timed_events = {} if timed_events is None else timed_events

        # Setup template context
        @self.__app.context_processor
        def variables() -> dict:  # pylint: disable=unused-variable
            return dict({"controller": self.controller, "callbacks": self.callbacks, "timed_events": self.timed_events,
                         "web_resource": WebController.web_resource},
                        **dict(globals(), **builtins.__dict__))  # Dictionary stacking to concat

        # Setup thread
        self.__running = False
        self.run()

    @staticmethod
    def filemtime(file: str) -> int:
        try:
            return path.getmtime(file)
        except Exception:
            return 0

    @staticmethod
    def web_resource(file: str) -> str:
        return "{}?v={:.0f}".format(file, WebController.filemtime(path.dirname(__file__) + file))

    def __default_callbacks(self):
        # Some default callbacks
        if 'all_on' not in self.callbacks:
            self.callbacks['all_on'] = self.controller.all_on
        if 'all_off' not in self.callbacks:
            self.callbacks['all_off'] = self.controller.all_off
        if 'all_locate' not in self.callbacks:
            self.callbacks['all_locate'] = self.controller.all_locate

    def __check_callbacks(self):
        for key in self.callbacks.keys():
            if not self.callbacks[key] or not callable(self.callbacks[key]):
                del self.callbacks[key]

    def run(self):
        if not self.__running:
            self.__thread = ServerThread(self.__host, self.__port, self.__app, daemon=True)
            self.__thread.start()

    def stop(self):
        self.__thread.shutdown()
        self.__running = False
