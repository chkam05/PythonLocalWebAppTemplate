from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class WindowSettings(BaseDataModel):

    # Default values
    _DEFAULT_HEIGHT: ClassVar[int] = 800
    _DEFAULT_X: ClassVar[int] = 100
    _DEFAULT_Y: ClassVar[int] = 100
    _DEFAULT_WIDTH: ClassVar[int] = 1200

    # Field name declarations
    FIELD_HEIGHT: ClassVar[str] = 'height'
    FIELD_X: ClassVar[str] = 'x'
    FIELD_Y: ClassVar[str] = 'y'
    FIELD_WIDTH: ClassVar[str] = 'width'

    # Fields
    height: int
    x: int
    y: int
    width: int

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> WindowSettings:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            height=d.get(cls.FIELD_HEIGHT, cls._DEFAULT_HEIGHT),
            x=d.get(cls.FIELD_X, cls._DEFAULT_X),
            y=d.get(cls.FIELD_Y, cls._DEFAULT_Y),
            width=d.get(cls.FIELD_WIDTH, cls._DEFAULT_WIDTH)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_HEIGHT: self.height,
            self.FIELD_X: self.x,
            self.FIELD_Y: self.y,
            self.FIELD_WIDTH: self.width
        }

    #endregion Serialization
