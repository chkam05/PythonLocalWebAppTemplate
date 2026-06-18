from typing import ClassVar

import platform
import subprocess
import shutil
import importlib.util


class WebviewRuntime:
    _LINUX_PKG_CONFIG_BIN: ClassVar[str] = 'pkg-config'
    _SYSTEM_NAME_LINUX: ClassVar[str] = 'Linux'
    _SYSTEM_NAME_MACOS: ClassVar[str] = 'Darwin'
    _SYSTEM_NAME_WINDOWS: ClassVar[str] = 'Windows'
    _WEBVIEW_EDGE_CHROMIUM: ClassVar[str] = 'edgechromium'
    _WEBVIEW_GTK: ClassVar[str] = 'gtk'
    _WEBVIEW_QT: ClassVar[str] = 'qt'

    _QT_MODULES: ClassVar[list] = [
        'PyQt6',
        'PySide6',
        'PyQt5',
        'PySide2'
    ]

    _WEBKIT_GTK_PACKAGES: ClassVar[list] = [
        'webkit2gtk-4.1',
        'webkit2gtk-4.0'
    ]

    _WINDOWS_WEBVIEW_KEYS: ClassVar[list] = [
        r'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}',
        r'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}'
    ]

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')
    
    @staticmethod
    def command_exists(command: str) -> bool:
        return shutil.which(command) is not None
    
    @staticmethod
    def module_exists(module_name: str) -> bool:
        return importlib.util.find_spec(module_name) is not None
    
    @classmethod
    def choose_webview_backend(cls) -> str | None:
        if cls.is_windows():
            if cls.is_windows_webview2_installed():
                return cls._WEBVIEW_EDGE_CHROMIUM

            if cls.is_qt_backend_installed():
                return cls._WEBVIEW_QT

            return None

        if cls.is_macos():
            return None

        if cls.is_linux():
            if cls.is_webkitgtk_installed():
                return cls._WEBVIEW_GTK

            if cls.is_qt_backend_installed():
                return cls._WEBVIEW_QT

            return None

        return None

    @classmethod
    def dependency_message(cls) -> str:
        if cls.is_windows():
            return (
                'Microsoft Edge WebView2 Runtime is missing.\n'
                'Install WebView2 Evergreen Runtime.'
            )

        if cls.is_linux():
            return (
                'No WebView backend.\n\n'
                'Ubuntu/Debian:\n'
                'sudo apt install libwebkit2gtk-4.1-0 gir1.2-webkit2-4.1\n\n'
                'Alternatively:\n'
                'pip install pywebview[qt]'
            )

        return 'No WebView backend supported.'

    @staticmethod
    def get_system() -> str:
        return platform.system()
    
    @classmethod
    def is_linux(cls) -> bool:
        return cls.get_system() == cls._SYSTEM_NAME_LINUX
    
    @classmethod
    def is_macos(cls) -> bool:
        return cls.get_system() == cls._SYSTEM_NAME_MACOS
    
    @classmethod
    def is_qt_backend_installed(cls) -> bool:
        return any([cls.module_exists(module_name) for module_name in cls._QT_MODULES])

    @classmethod
    def is_webkitgtk_installed(cls) -> bool:
        if not cls.is_linux():
            return False

        if not cls.command_exists(cls._LINUX_PKG_CONFIG_BIN):
            return False

        for package in cls._WEBKIT_GTK_PACKAGES:
            result = subprocess.run(
                [cls._LINUX_PKG_CONFIG_BIN, '--exists', package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if result.returncode == 0:
                return True

        return False
    
    @classmethod
    def is_windows(cls) -> bool:
        return cls.get_system() == cls._SYSTEM_NAME_WINDOWS
    
    @classmethod
    def is_windows_webview2_installed(cls) -> bool:
        if not cls.is_windows():
            return False

        try:
            import winreg
        except ImportError:
            return False

        for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for key_path in cls._WINDOWS_WEBVIEW_KEYS:
                try:
                    with winreg.OpenKey(root, key_path) as key:
                        version, _ = winreg.QueryValueEx(key, 'pv')

                        if version and version != '0.0.0.0':
                            return True

                except OSError:
                    continue

        return False

    @classmethod
    def validate_webview_runtime(cls) -> None:
        backend = cls.choose_webview_backend()

        if cls.is_windows() and backend is None:
            raise RuntimeError(cls.dependency_message())

        if cls.is_linux() and backend is None:
            raise RuntimeError(cls.dependency_message())
