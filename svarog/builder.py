from functools import singledispatch
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from .checks import has_annotated_init
from .checks import is_union_type
from .functional_dispatch import FunctionalDispatch
from .types import Build
from .types import NoneType

T = TypeVar("T")


class CannotDispatch(Exception):
    pass


def sentry(type_: Type[T], data: Any, build: Build) -> T:
    raise CannotDispatch()


def none_builder(type_: NoneType, data: Any, build: Build) -> None:
    return None


def annotated_init_build(type_: Type[T], data: Any, build: Build) -> T:
    return type_(**data)  # type: ignore


def union_build(union: Union, data: Any, build: Build) -> Optional[T]:
    params = union.__args__  # type: ignore
    if NoneType in params:
        if data is None:
            return None

        if len(params) == 2:
            first, second = params
            other = first if second is NoneType else second
            return build(other, data)

    raise NotImplementedError("Unions other as optionals are not supported yet")


class Builder:
    def __init__(self):
        self.single_dispatch = singledispatch(sentry)
        self.single_dispatch.register(NoneType)(none_builder)  # type: ignore

        self.functional_dispatch: FunctionalDispatch = FunctionalDispatch(sentry)
        self.functional_dispatch.register(has_annotated_init)(annotated_init_build)
        self.functional_dispatch.register(is_union_type)(union_build)

    def build(self, type_: Type[T], data: Any) -> T:
        try:
            return self.single_dispatch(type_, data, self.build)
        except CannotDispatch:
            try:
                return self.functional_dispatch(type_, data, self.build)
            except CannotDispatch:
                return type_(data)  # type: ignore
