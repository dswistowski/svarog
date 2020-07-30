from typing import Any
from typing import Protocol
from typing import Type
from typing import TypeVar

T = TypeVar("T")


class Build(Protocol):
    def __call__(self, type: Type[T], data: Any) -> T:
        ...
