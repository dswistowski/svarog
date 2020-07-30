from functools import singledispatch
from typing import Any
from typing import Type
from typing import TypeVar

T = TypeVar("T")


class CannotDispatch(Exception):
    pass


def sentry(type_: Type, data: Any) -> None:
    raise CannotDispatch()


def none_converter(type_: Type, data: Any) -> None:
    return None


NoneType = type(None)


class Builder:
    def __init__(self):
        self.single_dispatch = singledispatch(sentry)

        self.single_dispatch.register(NoneType)(none_converter)

    def build(self, type: Type[T], data: Any) -> T:
        try:
            return self.single_dispatch(type, data)  # type: ignore
        except CannotDispatch:
            return type(data)  # type: ignore
