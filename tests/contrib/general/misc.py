import inspect
from typing import Callable, Coroutine, Iterable, Optional, Sequence, TypeVar

from tests.contrib.assertion.partial_dict import PartialDict

T = TypeVar('T')
V = TypeVar('V')


def intercept(
    function: T,
    *,
    before: Optional[Callable[..., Coroutine]] = None,
    after: Optional[Callable[..., Coroutine]] = None,
    error: Optional[Callable[..., Coroutine]] = None,
    success: Optional[Callable[..., Coroutine]] = None,
) -> T:
    async def handler(*args, **kwargs):
        if before:
            await before()
        try:
            result = await function(*args, **kwargs)
            if success:
                await invoke(success, result=result, args=args, kwargs=kwargs)
            return result
        except BaseException as ex:
            if error:
                await invoke(error, error=ex)
            raise ex
        finally:
            if after:
                await after()

    return handler  # type: ignore


def invoke(function, *args, **kwargs):
    try:
        spec = inspect.getfullargspec(function)
    except TypeError:
        return function(*args, **kwargs)
    arg_count = None if spec.varargs else min(len(args), len(spec.args))
    kw = {k: w for k, w in kwargs.items() if spec.varkw or (k in spec.kwonlyargs) or (k in spec.args)}
    return function(*args[0:arg_count], **kw)


def to_async(function: Callable[..., T]):
    async def handler(*args, **kwargs) -> T:
        return invoke(function, *args, **kwargs)

    return handler


def to_async_iter(*items):
    async def handler():
        for item in items:
            yield item

    return handler


def null_cast(ctor: Callable[[T], V], value: Optional[T]) -> Optional[V]:
    return ctor(value) if value is not None else None


async def scan_properties(entity, names: Iterable[Sequence[str]], wildcard='*', skip: Sequence = (None,)):
    for row in names:
        done = False
        value = entity
        for index, name in enumerate(row):
            if name == wildcard:
                for item in value or ():
                    remaining = row[index + 1 :]  # noqa
                    async for result in scan_properties(item, [remaining], wildcard):
                        yield result
                done = True
                break
            else:
                value = PartialDict.read_property_of(value, name)
        if not done and value not in skip:
            yield value
