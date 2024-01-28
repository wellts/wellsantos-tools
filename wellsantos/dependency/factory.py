from typing import Any, Callable, Dict, Optional, Type, TypeVar

from ..general.model import JsonTypeError, json_dump
from .close import CloseInterface

T = TypeVar('T')


# TODO: refactor to not use "@classmethod", but use instance methods instead;
#   then we create a variable "Factory = _FactoryClass()" to be used globally
class Factory:
    instances: Dict = {}

    @classmethod
    def require(cls, typ: Callable[..., T], ctor: Optional[Callable[..., T]] = None) -> T:
        return cls.instances.get(typ) or cls.instances.setdefault(typ, (ctor or typ)())

    @classmethod
    def init(cls, instance: T, *types: Type) -> T:
        for typ in types or [type(instance)]:
            done = cls.instances.setdefault(typ, instance)
            if done is not instance:
                raise RuntimeError(f'{typ} was already initialized with {type(done)}')  # pragma: no cover
        return instance

    @classmethod
    async def close(cls):
        values = list(cls.instances.values())
        cls.instances.clear()
        for item in values:
            if isinstance(item, CloseInterface):
                await item.close()

    @classmethod
    def key_of(cls, *values) -> Any:
        return json_dump(values, default=cls._key_json_default)

    @classmethod
    def _key_json_default(cls, value):
        if callable(value):
            return id(value)
        raise JsonTypeError.raise_error(value)  # pragma: no cover

    @classmethod
    def find(cls, typ: Type[T]) -> Optional[T]:
        return cls.instances.get(typ)


use = Factory.require
