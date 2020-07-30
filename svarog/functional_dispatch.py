from typing import Any
from typing import Callable
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar

from .types import Build
from .types import Check
from .types import Handler

T = TypeVar("T")


def _true(*args, **kwargs):
    return True


class FunctionalDispatch:
    def __init__(self, always: Handler):
        self.registry: Sequence[Tuple[Check, Handler]] = [(_true, always)]
        self.sentry = always

    def register(self, check: Check) -> Callable[[Handler], Handler]:
        def wrapper(handler: Handler) -> Handler:
            self.registry = ((check, handler), *self.registry)
            return handler

        return wrapper

    def __call__(self, type_: Type[T], data: Any, build: Build) -> T:
        # TODO: getting correct build function for type can be cached
        for check, local_build in self.registry:
            if check(type_):
                return local_build(type_, data, build)
        raise RuntimeError("Cannot find dispatcher")
