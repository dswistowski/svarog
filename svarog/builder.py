from typing import Any
from typing import Callable
from typing import TypeVar

T = TypeVar("T")


class Builder:
    def build(self, type: Callable, data: Any) -> T:
        return type(data)
