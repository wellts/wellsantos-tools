from typing import Dict, Type, TypeVar

from ..general.misc import UNDEFINED
from .factory import Factory, use

T = TypeVar('T', bound=Type)


class Subclass:
    @classmethod
    def of(cls, typ: T, **properties) -> T:
        object_type = typ
        if issubclass(typ, Subclass):
            object_type = typ._root_class()
            properties = typ._subclass_properties() | properties
        key = Factory.key_of(Subclass, object_type, sorted(properties.items()))
        return use(key, lambda: cls._declare(object_type, properties))

    @classmethod
    def _declare(cls, object_type, properties: Dict):
        class VariationClass(object_type, Subclass):
            @classmethod
            def _root_class(cls):
                return object_type

            @classmethod
            def _subclass_properties(cls):
                return properties

        identical = True
        for k, v in properties.items():
            found = getattr(object_type, k, UNDEFINED)
            identical = identical and found is not UNDEFINED and Factory.key_of(v) == Factory.key_of(found)
            setattr(VariationClass, k, v)

        return object_type if identical else VariationClass

    @classmethod
    def root(cls, typ: T) -> T:
        return typ._root_class() if issubclass(typ, Subclass) else typ

    @classmethod
    def _root_class(cls):
        return cls

    @classmethod
    def _subclass_properties(cls):
        return {}
