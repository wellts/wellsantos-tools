from contextlib import asynccontextmanager
from typing import Type, TypeVar

from ..general.tracing import ParentRequestId, RequestId
from .factory import Factory

T = TypeVar('T')


class LocalFactory(Factory):
    instances = {}

    @classmethod
    @asynccontextmanager
    async def open(cls):
        class InnerFactory(LocalFactory):
            instances = cls.instances.copy()

        InnerFactory.set_child(ParentRequestId, RequestId)
        yield InnerFactory
        await InnerFactory.close()

    @classmethod
    def set_child(cls, parent_type, child_type: Type[T]) -> T:
        if parent := cls.instances.get(child_type):
            cls.instances[parent_type] = parent
        result = child_type()
        cls.instances[child_type] = result
        return result

    @classmethod
    def set(cls, instance: T, *types: Type) -> T:
        for typ in types or [type(instance)]:
            cls.instances[typ] = instance
        return instance
