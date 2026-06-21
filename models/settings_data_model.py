from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel
from models.settings.window_settings import WindowSettings


@dataclass
class SettingsDataModel(BaseDataModel):

    # Default values

    # Field name declarations
    FIELD_WINDOW: ClassVar[str] = 'window'

    # Fields
    window: WindowSettings | None

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> SettingsDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        window = d.get(cls.FIELD_WINDOW, {})

        return cls(
            window=WindowSettings.from_dict(window)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_WINDOW: self.window.to_dict()
        }

    #endregion Serialization
