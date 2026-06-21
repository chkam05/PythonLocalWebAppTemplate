from __future__ import annotations
from flask import Blueprint, Flask
from threading import Lock, Thread, current_thread
from typing import Any
from werkzeug.serving import make_server

from storage.settings_storage import SettingsStorage


class Service:

    def __init__(self, host: str, port: int, settings_storage: SettingsStorage, **args: Any):
        self._host = host
        self._port = port

        self._service = Flask(__name__, **args)
        self._server: Any | None = None
        self._settings_storage = settings_storage
        self._thread: Thread | None = None
        self._lock = Lock()
        self._register_controllers()
    
    #region Properties

    @property
    def host(self) -> str:
        return self._host
    
    @property
    def port(self) -> int:
        return self._port

    #endregion

    def _register_controllers(self):
        from controllers.settings_controller import SettingsController
        from controllers.window_controller import WindowController

        self._register_controller(SettingsController(self._settings_storage))
        self._register_controller(WindowController())
    
    def _register_controller(self, controller: Blueprint, **options: Any):
        self._service.register_blueprint(controller, **options)

    def run(self):
        with self._lock:
            if self._server is None:
                self._server = make_server(
                    host=self._host,
                    port=self._port,
                    app=self._service,
                    threaded=True
                )

            server = self._server

        server.serve_forever()
    
    def run_async(self):
        with self._lock:
            if self._thread and self._thread.is_alive():
                return self._thread

            self._thread = Thread(target=self.run, daemon=True)
            self._thread.start()

            return self._thread

    def stop(self):
        with self._lock:
            server = self._server
            thread = self._thread

        if server is not None:
            server.shutdown()

        if thread and thread.is_alive() and thread is not current_thread():
            thread.join(timeout=5)

        with self._lock:
            if self._server is server:
                self._server = None

            if self._thread is thread:
                self._thread = None
