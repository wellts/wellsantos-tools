import inspect

import pytest

from app.contrib.general.misc import func_wrap


def mass():
    class A:
        async def __call__(self, a, b=4, *args, c, d=1, **kwargs):
            return ""

        async def fa(self, a, b=4, *args, c, d=1, **kwargs):
            return ""

    async def fa(a, b=4, *args, c, d=1, **kwargs):
        return ""

    class B:
        def __call__(self, *args, **kwargs):
            return [self, 2, args, kwargs]

        def fb(self, *args, **kwargs):
            return [self, 1, args, kwargs]

    def fb(*args, **kwargs):
        return [0, args, kwargs]

    this = B()

    return [
        (fa, fb, [], [0]),
        (A.fa, B.fb, [this], [this, 1]),
        (A.__call__, B.__call__, [this], [this, 2]),
        (A().__call__, this.__call__, [], [this, 2]),
        (A(), this, [], [this, 2]),
    ]


ids = [
    'static',
    'class',
    'class_call',
    'bounded_call',
    'instance_call',
]


@pytest.mark.parametrize('index', [x for x in range(len(ids))], ids=ids)
def test_func_wrap(index):
    a, b, p, r = mass()[index]
    c = func_wrap(a, b)
    found = c(*p, 10, z=20)
    assert found == r + [(10,), {'z': 20}]
    if index < 3:
        a_spec = inspect.getfullargspec(a)
        c_spec = inspect.getfullargspec(c)
        assert c_spec == a_spec
