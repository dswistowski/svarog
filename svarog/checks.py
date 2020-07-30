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

T = TypeVar("T")


def has_annotated_init(type_: Type[T]) -> bool:
    return hasattr(type_, "__init__") and hasattr(type_.__init__, "__annotations__")


def is_union_type(type_: Union) -> bool:
    return (
        type_ is Union or isinstance(type_, _GenericAlias) and type_.__origin__ is Union
    )


def is_list(type_: Any) -> bool:
    return type_ is List or (
        type_.__class__ is _GenericAlias
        and type_.__origin__ is not Union
        and issubclass(type_.__origin__, Sequence)
    )


def is_bare(type_: Any) -> bool:
    args = type_.__args__
    return (
        args == List.__args__  # type: ignore
        or args == Sequence.__args__  # type: ignore
        or args == Mapping.__args__  # type: ignore
        or args == Dict.__args__  # type: ignore
        or args == MutableSequence.__args__  # type: ignore
    )
