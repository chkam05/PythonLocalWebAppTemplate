from time import time, sleep
from threading import Lock
from typing import ClassVar
import socket
import webview

from config import *
from core.models.settings_data_model import SettingsDataModel
from core.service import Service
from core.storage.settings_storage import SettingsStorage
from utils.webview_runtime import WebviewRuntime


class App:
    _CONNECTION_TIMEOUT: ClassVar[float] = 0.3
    _CONNECTION_EXCEPTION_TIMEOUT: ClassVar[float] = 0.1

    def __init__(self):
        WebviewRuntime.validate_webview_runtime()

        self._configure_app_metadata()

        self._app_url = f'http://{HOST}:{PORT}'
        self._backend = WebviewRuntime.choose_webview_backend()
        self._app_icon = APP_ICON_WINDOWS if WebviewRuntime.is_windows() else APP_ICON
        self._settings_storage = SettingsStorage()
        self._window_count = 0
        self._window_lock = Lock()
        self._service = Service(
            HOST,
            PORT,
            settings_storage = self._settings_storage,
            template_folder = TEMPLATE_FOLDER,
            static_folder = STATIC_FOLDER,
            static_url_path = STATIC_URL_PATH
        )

    def _create_window(self):
        settings = self._settings_storage.load()

        with self._window_lock:
            self._window_count += 1

        window = webview.create_window(
            title=APP_NAME,
            url=self._app_url,
            width=settings.window_width,
            height=settings.window_height,
            x=settings.window_pos_x,
            y=settings.window_pos_y
        )
        window.events.closing += lambda: self._on_window_closing(window)
        window.events.closed += self._on_window_closed

        return window

    def _on_window_closing(self, window):
        try:
            settings = SettingsDataModel(
                window_height=window.height,
                window_pos_x=window.x,
                window_pos_y=window.y,
                window_width=window.width
            )
        except Exception:
            return

        self._settings_storage.save(settings)

    def _on_window_closed(self):
        with self._window_lock:
            self._window_count -= 1
            has_open_windows = self._window_count > 0

        if not has_open_windows:
            self._service.stop()

    @classmethod
    def _configure_app_metadata(cls):
        if not WebviewRuntime.is_macos():
            return

        try:
            from AppKit import NSBundle
        except ImportError:
            return

        info = NSBundle.mainBundle().infoDictionary()
        info.setObject_forKey_(APP_NAME, 'CFBundleName')
        info.setObject_forKey_(APP_NAME, 'CFBundleDisplayName')

    @classmethod
    def __wait_for_server__(cls, host: str, port: int, timeout: int):
        start = time()

        while time() - start < timeout:
            try:
                with socket.create_connection((host, port), timeout=cls._CONNECTION_TIMEOUT):
                    return True
            except OSError:
                sleep(cls._CONNECTION_EXCEPTION_TIMEOUT)
        
        return False
    
    def startup(self):
        self._service.run_async()
        
        if not self.__wait_for_server__(HOST, PORT, SERVICE_TIMEOUT):
            raise RuntimeError('Flask server failed to start.')
        
        self._create_window()

        try:
            if self._backend:
                webview.start(gui=self._backend, icon=self._app_icon)
            else:
                webview.start(icon=self._app_icon)
        finally:
            self._service.stop()


if __name__ == "__main__":
    App().startup()
