from __future__ import annotations
from abc import ABC, abstractmethod
import copy
import json
from json import JSONDecodeError
from pathlib import Path
import tempfile
import threading
from typing import Any, Dict


class BaseJsonStorage(ABC):
    """Base storage for thread-safe JSON file access."""

    _ENCODING = 'utf-8'
    _INDENT = 4

    def __init__(self, directory: str, file_name: str, cache_enabled: bool = True) -> None:
        self._directory = Path(directory)
        self._file_name = file_name
        self._cache_enabled = cache_enabled
        self._lock = threading.RLock()
        self._cache_data: Dict[str, Any] | None = None
        self._cache_mtime: float | None = None

    #region Properties

    @property
    def directory(self) -> Path:
        """Returns the directory where the JSON file is stored."""
        return self._directory

    @property
    def file_name(self) -> str:
        """Returns the JSON file name."""
        return self._file_name

    @property
    def file_path(self) -> Path:
        """Returns the full JSON file path."""
        return self._directory / self._file_name

    #endregion Properties

    @abstractmethod
    def _initialize_default_data(self) -> Dict[str, Any]:
        """Return the initial data structure for the JSON storage."""
        raise NotImplementedError(f'The {self._initialize_default_data.__name__}() method must be overridden in the derived class.')

    #region Cache

    def invalidate_cache(self) -> None:
        """Clear the in-memory cache and force future reads to reload from disk."""
        with self._lock:
            self._cache_data = None
            self._cache_mtime = None

    def get_snapshot(self) -> Dict[str, Any]:
        """Return a deep-copied snapshot of the current JSON data."""
        return self._read()

    #endregion Cache

    #region File operations

    def exists(self) -> bool:
        """Checks whether the JSON file exists."""
        return self.file_path.exists()

    def _ensure_parent_dir_exists(self) -> None:
        """Creates the JSON parent directory when it does not exist."""
        self._directory.mkdir(parents=True, exist_ok=True)

    def _get_file_mtime(self) -> float | None:
        """Returns the JSON file modification time when the file exists."""
        try:
            return self.file_path.stat().st_mtime
        except FileNotFoundError:
            return None

    def _read(self) -> Dict[str, Any]:
        """Read JSON data from disk or cache with thread-safe access."""
        with self._lock:
            if self._cache_enabled and self._cache_data is not None:
                try:
                    current_mtime = self.file_path.stat().st_mtime
                except FileNotFoundError:
                    data = self._initialize_default_data()
                    self._cache_data = copy.deepcopy(data)
                    self._cache_mtime = None
                    return copy.deepcopy(data)

                if self._cache_mtime is not None and current_mtime == self._cache_mtime:
                    return copy.deepcopy(self._cache_data)

            data = self._read_json_or_default()

            if self._cache_enabled:
                self._cache_data = copy.deepcopy(data)
                self._cache_mtime = self._get_file_mtime()

            return copy.deepcopy(data)

    def _read_json_or_default(self) -> Dict[str, Any]:
        """Reads JSON data or returns initial data when the file is missing or invalid."""
        try:
            with self.file_path.open('r', encoding=self._ENCODING) as file:
                data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            return self._initialize_default_data()

        if not isinstance(data, dict):
            return self._initialize_default_data()

        return data

    def _write(self, data: Dict[str, Any]) -> None:
        """Write JSON data atomically using a temporary file and replace operation."""
        with self._lock:
            self._ensure_parent_dir_exists()
            temp_path = None

            try:
                with tempfile.NamedTemporaryFile(
                    'w',
                    delete=False,
                    dir=self._directory,
                    encoding=self._ENCODING,
                ) as file:
                    temp_path = Path(file.name)
                    json.dump(data, file, ensure_ascii=False, indent=self._INDENT)
                    file.write('\n')

                temp_path.replace(self.file_path)

                if self._cache_enabled:
                    self._cache_data = copy.deepcopy(data)
                    self._cache_mtime = self._get_file_mtime()
            finally:
                if temp_path is not None and temp_path.exists():
                    temp_path.unlink()

    #endregion File operations
