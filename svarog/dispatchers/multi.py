from functools import lru_cache
from functools import singledispatch
from typing import Any
from typing import Type
from typing import TypeVar

from ..types import CannotDispatch
from ..types import Forge
from .functional import FunctionalDispatch


T = TypeVar("T")


def sentry(type_: Type[T], data: Any, build: Forge) -> T:
    raise CannotDispatch()


class MultiDispatcher:
    def __init__(self):
        self._single_dispatch = singledispatch(CannotDispatch)
        self._functional_dispatch: FunctionalDispatch = FunctionalDispatch(sentry)
        self.dispatch = lru_cache()(self._dispatch)

    def register_cls(self, type_, handler):
        self._single_dispatch.register(type_, handler)
        self.dispatch.cache_clear()

    def register_func(self, func, handler):
        self._functional_dispatch.register(func)(handler)
        self.dispatch.cache_clear()

    def _dispatch(self, type_):
        try:
            dispatch = self._single_dispatch.dispatch(type_)
        except AttributeError:
            dispatch = CannotDispatch

        if dispatch == CannotDispatch:
            return self._functional_dispatch
        return dispatch
