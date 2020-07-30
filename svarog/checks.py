from typing import _GenericAlias  # type: ignore
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
