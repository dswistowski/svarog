from functools import singledispatch
from typing import Any
from typing import Type
from typing import TypeVar

from .checks import has_annotated_init
from .functional_dispatch import FunctionalDispatch
from .types import NoneType

T = TypeVar("T")


class CannotDispatch(Exception):
    pass


def sentry(type_: Type[T], data: Any) -> T:
    raise CannotDispatch()


def none_builder(type_: NoneType, data: Any) -> None:
    return None


def annotated_init_parser(type_: Type[T], data: Any) -> T:
    return type_(**data)  # type: ignore


class Builder:
    def __init__(self):
        self.single_dispatch = singledispatch(sentry)
        self.functional_dispatch: FunctionalDispatch = FunctionalDispatch(sentry)
        self.functional_dispatch.register(has_annotated_init)(annotated_init_parser)

        self.single_dispatch.register(NoneType)(none_builder)  # type: ignore

    def build(self, type_: Type[T], data: Any) -> T:
        try:
            return self.single_dispatch(type_, data)
        except CannotDispatch:
            try:
                return self.functional_dispatch(type_, data)
            except CannotDispatch:
                return type_(data)  # type: ignore
