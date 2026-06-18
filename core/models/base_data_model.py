from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, ClassVar, Dict, List, Type, TypeVar, get_origin


T = TypeVar('T', bound='BaseDataModel')


@dataclass
class BaseDataModel(ABC):

    def __init_subclass__(cls, **kwargs) -> None:
        """Validates field constants when a model subclass is declared."""
        super().__init_subclass__(**kwargs)
        cls._validate_field_constants()

    #region Fields

    @classmethod
    def field_names(cls) -> List[str]:
        """Returns all dataclass field names defined for the model."""
        return [field.name for field in fields(cls)]
    
    @classmethod
    def _declared_field_constants(cls) -> Dict[str, str]:
        """Returns FIELD_* constants with their declared field names."""
        return {
            name: getattr(cls, name)
            for name, type_hint in cls.__annotations__.items()
            if name.startswith('FIELD_') and cls._is_class_var(type_hint)
        }
    
    @classmethod
    def _declared_field_names(cls) -> List[str]:
        """Returns model attribute names declared in class annotations."""
        return [
            name
            for name, type_hint in cls.__annotations__.items()
            if not cls._is_class_var(type_hint)
        ]
    
    @staticmethod
    def _is_class_var(type_hint) -> bool:
        """Checks whether a type hint represents a ClassVar annotation."""
        return get_origin(type_hint) is ClassVar or str(type_hint).startswith('ClassVar')

    @classmethod
    def _validate_field_constants(cls) -> None:
        """Validates that model fields and FIELD_* constants match each other."""
        fields = set(cls._declared_field_names())
        field_constants = cls._declared_field_constants()
        constant_fields = set(field_constants.values())

        fields_without_constants = sorted(fields - constant_fields)
        constants_without_fields = sorted([
            constant_name
            for constant_name, field_name in field_constants.items()
            if field_name not in fields
        ])

        if not fields_without_constants and not constants_without_fields:
            return

        details = []

        if fields_without_constants:
            details.append(
                'There are no field name declarations for attributes: '
                + ', '.join(fields_without_constants)
            )

        if constants_without_fields:
            details.append(
                'There are no attributes for field name declarations: '
                + ', '.join(constants_without_fields)
            )

        raise ValueError(f'{cls.__name__}: ' + '; '.join(details))

    #endregion Fields

    #region Serialization

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], d: Dict[str, Any]) -> BaseDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        raise NotImplementedError(f'The {cls.from_dict.__name__} method must be overridden in the derived class.')
    
    @classmethod
    def from_dict_list(cls: Type[T], rows: List[Dict[str, Any]]) -> List[T]:
        """Deserializes data from a list of "attribute:value" format dictionaries to a list of objects."""
        return [cls.from_dict(r) for r in (rows or [])]
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        raise NotImplementedError(f'The {self.to_dict.__name__} method must be overridden in the derived class.')
    
    @staticmethod
    def to_dict_list(items: List[BaseDataModel] | None) -> List[Dict[str, Any]]:
        """Serializes a list of objects to a dictionary list in "attribute:value" format."""
        return [i.to_dict() for i in (items or [])]

    #endregion Serialization
