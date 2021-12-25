from typing import Any
from typing import Callable
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar

from svarog.types import Check
from svarog.types import Filter
from svarog.types import Forge
from svarog.types import Handler

T = TypeVar("T")


def _true(*args, **kwargs):
    return True


class PredicatedFilters:
    __slots__ = ("_registry",)

    def __init__(self):
        self._registry: Sequence[Tuple[Check, Filter]] = ()

    def add(self, check: Check) -> Callable[[Filter], Filter]:
        def wrapper(filter: Filter) -> Filter:
            self._registry = (*self._registry, (check, filter))
            return filter

        return wrapper

    def __call__(self, type_: Type, data: Any) -> Any:
        for check, filter in self._registry:
            if check(type_):
                data = filter(type_, data)
        return data


class FunctionalDispatch:
    __slots__ = ("_registry", "_default")

    def __init__(self, default: Handler):
        self._registry: Sequence[Tuple[Check, Handler]] = [(_true, default)]
        self._default = default

    def register(self, check: Check) -> Callable[[Handler], Handler]:
        def wrapper(handler: Handler) -> Handler:
            self._registry = ((check, handler), *self._registry)
            return handler

        return wrapper

    def __call__(self, type_: Type[T], data: Any, forge: Forge) -> T:
        for check, local_forge in self._registry:
            if check(type_):
                return local_forge(type_, data, forge)
        raise RuntimeError("Cannot find dispatcher")
