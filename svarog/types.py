from typing import Any
from typing import Callable
from typing import Type
from typing import TypeVar

T = TypeVar("T")

Build = Callable[[Type[T], Any], T]
Handler = Callable[[Any, Any, Build], T]
NoneType = type(None)
Check = Callable[[Any], bool]
