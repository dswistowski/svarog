from typing import Any
from typing import Callable
from typing import Type
from typing import TypeVar

T = TypeVar("T")

Forge = Callable[[Type[T], Any], T]
Handler = Callable[[Any, Any, Forge], T]
NoneType = type(None)
Check = Callable[[Any], bool]


class CannotDispatch(Exception):
    pass
