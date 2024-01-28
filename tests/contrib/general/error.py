from asyncio import CancelledError


class UnitTestAbortError(CancelledError):
    pass


class ExampleTestError1(RuntimeError):
    pass


class ExampleTestError2(RuntimeError):
    pass
