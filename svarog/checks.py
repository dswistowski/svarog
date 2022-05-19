import sys
from typing import _GenericAlias  # type: ignore
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import MutableSequence
from typing import Sequence
from typing import Type
from typing import TypeVar
from typing import Union

from .compat import _SpecialGenericAlias
from .compat import get_args
from .compat import get_origin


T = TypeVar("T")


def is_alias(type_: Any) -> bool:
    try:
        return isinstance(type_, _GenericAlias)
    except TypeError:
        return False


def has_annotated_init(type_: Type[T]) -> bool:
    return (
        not is_alias(type_)
        and hasattr(type_, "__init__")
        and hasattr(type_.__init__, "__annotations__")
    )


def is_literal(type_: Any) -> bool:
    if origin := get_origin(type_):
        try:
            return origin._name == "Literal"
        except AttributeError:
            pass
    return False


def is_union(type_: Union) -> bool:
    origin = get_origin(type_)
    if origin is Union:
        return True
    if sys.version_info >= (3, 10):
        UnionType = type(str | None)
        return origin is UnionType
    return False


def is_sequence(type_: Any) -> bool:
    try:
        return issubclass(get_origin(type_), Sequence)  # type: ignore
    except TypeError:
        return False


def is_list(type_: Any) -> bool:
    return type_ is List or (
        isinstance(type_, (_GenericAlias, _SpecialGenericAlias)) and is_sequence(type_)
    )


def is_bare(type_: Any) -> bool:
    args = get_args(type_)
    return (
        args == get_args(List)
        or args == get_args(Sequence)
        or args == get_args(Mapping)
        or args == get_args(Dict)
        or args == get_args(MutableSequence)
    )


def is_mapping_alias(type_: Any) -> bool:
    try:
        return type_.__class__ is _GenericAlias and issubclass(
            type_.__origin__, Mapping
        )
    except TypeError:
        return False


def is_mapping(type_: Any) -> bool:
    return type_ is Mapping or is_mapping_alias(type_)
