from abc import ABC, abstractmethod
from flask import Blueprint
from typing import ClassVar


class BaseController(Blueprint, ABC):
    CONTROLLER_NAME: ClassVar[str]

    def __init__(self):
        super().__init__(self.CONTROLLER_NAME, self.__class__.__module__)
        self.register_routes()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if 'CONTROLLER_NAME' not in cls.__dict__:
            raise TypeError(f'{cls.__name__} must define CONTROLLER_NAME')
        
        if not isinstance(cls.CONTROLLER_NAME, str) or cls.CONTROLLER_NAME == '':
            raise TypeError(f'{cls.__name__}.CONTROLLER_NAME must be not empty str')
    
    @abstractmethod
    def register_routes(self):
        raise NotImplementedError(f'{self.__class__.__name__} must implement register_routes')
