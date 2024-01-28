import functools
import inspect
from typing import Callable, Iterable, Optional, Type, TypeVar

from .error import NoneValueIsNotAllowedError

T = TypeVar('T')


class Undefined:
    def __str__(self):
        return '__undefined__'


UNDEFINED = Undefined()
"""A value used to represent that 'getattr' on an object raised an error."""


def not_none(value: Optional[T]) -> T:
    if value is None:
        raise NoneValueIsNotAllowedError()
    return value


def full_name(object_type):
    return f"{getattr(object_type, '__module__', '')}.{getattr(object_type, '__qualname__', '')}"


def get_first_error(items: Iterable) -> Optional[BaseException]:
    return next((item for item in items if isinstance(item, BaseException)), None)


def returning_type_hint(_: Callable[..., T], value=None) -> T:
    return value


def func_wrap(function: T, wrapper) -> T:
    sig = inspect.signature(function)  # type: ignore
    if not getattr(function, '__call__', None):
        try:
            setattr(wrapper, '__signature__', sig)
            return wrapper
        except AttributeError:
            pass
    handler = functools.partial(wrapper)
    setattr(handler, '__signature__', sig)
    return handler  # type: ignore


def safe_cast(typ: Type[T], value) -> T:
    if not isinstance(value, typ):
        raise TypeError(f'expected type {typ}, but got {type(value)}')
    return value
