from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.models.base_data_model import BaseDataModel


@dataclass
class SettingsDataModel(BaseDataModel):

    # Default values
    _DEFAULT_WINDOW_HEIGHT: ClassVar[int] = 800
    _DEFAULT_WINDOW_POS_X: ClassVar[int] = 100
    _DEFAULT_WINDOW_POX_Y: ClassVar[int] = 100
    _DEFAULT_WINDOW_WIDTH: ClassVar[int] = 1200

    # Field name declarations
    FIELD_WINDOW_HEIGHT: ClassVar[str] = 'window_height'
    FIELD_WINDOW_POS_X: ClassVar[str] = 'window_pos_x'
    FIELD_WINDOW_POS_Y: ClassVar[str] = 'window_pos_y'
    FIELD_WINDOW_WIDTH: ClassVar[str] = 'window_width'

    # Fields
    window_height: int
    window_pos_x: int
    window_pos_y: int
    window_width: int

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> SettingsDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            window_height=d.get(cls.FIELD_WINDOW_HEIGHT, cls._DEFAULT_WINDOW_HEIGHT),
            window_pos_x=d.get(cls.FIELD_WINDOW_POS_X, cls._DEFAULT_WINDOW_POS_X),
            window_pos_y=d.get(cls.FIELD_WINDOW_POS_Y, cls._DEFAULT_WINDOW_POX_Y),
            window_width=d.get(cls.FIELD_WINDOW_WIDTH, cls._DEFAULT_WINDOW_WIDTH)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_WINDOW_HEIGHT: self.window_height,
            self.FIELD_WINDOW_POS_X: self.window_pos_x,
            self.FIELD_WINDOW_POS_Y: self.window_pos_y,
            self.FIELD_WINDOW_WIDTH: self.window_width
        }

    #endregion Serialization
