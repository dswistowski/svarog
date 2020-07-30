from typing import Any
from typing import Callable
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar

from .types import Build
from .types import Check

T = TypeVar("T")


def _true(*args, **kwargs):
    return True


class FunctionalDispatch:
    def __init__(self, always: Build):
        self.registry: Sequence[Tuple[Check, Build]] = [(_true, always)]
        self.sentry = always

    def register(self, check: Check) -> Callable[[Build], Build]:
        def wrapper(build: Build) -> Build:
            self.registry = ((check, build), *self.registry)
            return build

        return wrapper

    def __call__(self, type_: Type[T], data: Any) -> T:
        # TODO: getting correct build function for type can be cached
        for check, build in self.registry:
            if check(type_):
                return build(type_, data)
        raise RuntimeError("Cannot find dispatcher")
