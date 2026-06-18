import os
import platform
from pathlib import Path


class PathUtils:
    """Utilities for resolving platform-specific application paths."""

    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this static utility class."""
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    @staticmethod
    def get_settings_dir(app_name: str, remove_spaces: bool = True) -> str:
        """Returns the platform-specific settings directory for an application."""
        system = platform.system()
        directory_name = app_name.replace(' ', '') if remove_spaces else app_name

        if system == 'Windows':
            base_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        elif system == 'Darwin':
            base_dir = Path.home() / 'Library' / 'Application Support'
        else:
            base_dir = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))

        return str(base_dir / directory_name)
