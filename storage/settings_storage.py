from __future__ import annotations
from typing import Any, Dict

from config import SETTINGS_DIR, SETTINGS_FILE_NAME
from models.settings_data_model import SettingsDataModel
from core.data.base_json_storage import BaseJsonStorage


class SettingsStorage(BaseJsonStorage):
    """Storage for application settings."""

    def __init__(self) -> None:
        super().__init__(SETTINGS_DIR, SETTINGS_FILE_NAME)

    def load(self) -> SettingsDataModel:
        """Loads application settings from JSON."""
        return SettingsDataModel.from_dict(self._read())

    def save(self, model: SettingsDataModel) -> None:
        """Saves application settings to JSON."""
        self._write(model.to_dict())

    def _initialize_default_data(self) -> Dict[str, Any]:
        """Return the initial data structure for application settings."""
        return SettingsDataModel.from_dict({}).to_dict()
