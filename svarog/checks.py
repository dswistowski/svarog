from typing import Type
from typing import TypeVar

T = TypeVar("T")


def has_annotated_init(type_: Type[T]) -> bool:
    return hasattr(type_, "__init__") and hasattr(type_.__init__, "__annotations__")
