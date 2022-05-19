import sys
from functools import lru_cache
from typing import _eval_type  # type: ignore
from typing import Any
from typing import Dict
from typing import Hashable
from typing import Type
from typing import TypeVar

from .checks import has_annotated_init
from .checks import is_list
from .checks import is_literal
from .checks import is_mapping
from .checks import is_union
from .compat import ForwardRef
from .dispatchers.functional import PredicatedFilters
from .dispatchers.multi import MultiDispatcher
from .forges import _clean_annotations
from .forges import filter_cammel_case
from .forges import forge_annotated_init
from .forges import forge_list
from .forges import forge_literal
from .forges import forge_mapping
from .forges import forge_none
from .forges import forge_union
from .types import CannotDispatch
from .types import Check
from .types import Filter
from .types import Handler
from .types import NoneType

T = TypeVar("T", bound=Hashable)


class Svarog:
    _refs_owners: Dict[ForwardRef, Type]

    def __init__(self, snake_case: bool = False):
        self._refs_owners = {}
        self._dispatcher = MultiDispatcher()

        self.register_forge(NoneType, forge_none)  # type: ignore
        self.register_mold(has_annotated_init, forge_annotated_init)

        self.register_mold(is_list, forge_list)
        self.register_mold(is_mapping, forge_mapping)
        self.register_mold(is_union, forge_union)
        self.register_mold(is_literal, forge_literal)

        self._filter = PredicatedFilters()

        if snake_case:
            self.enable_snake_case()

    def enable_snake_case(self):
        self.add_filter(has_annotated_init, filter_cammel_case)

    def add_filter(self, predicate: Check, filter: Filter) -> None:
        self._filter.add(predicate)(filter)

    def register_forge(self, type_: Type, forge: Handler) -> None:
        self._dispatcher.register_cls(type_, forge)

    def register_mold(self, check: Check, forge: Handler) -> None:
        self._dispatcher.register_func(check, forge)

    @lru_cache(None)
    def _update_forward_ref_owners_registry(self, type_: Type) -> None:
        def update_subtype(sub_type: Type) -> None:
            if isinstance(sub_type, ForwardRef):
                self._refs_owners[sub_type] = type_
            if (
                not isinstance(sub_type, NoneType)  # type: ignore
                and sub_type is not Any
                and hasattr(sub_type, "__args__")
            ):
                for arg in sub_type.__args__:
                    update_subtype(arg)

        for _, annotation in _clean_annotations(type_.__init__):
            update_subtype(annotation)

    def forge(self, type_: Type[T], data: Any) -> T:
        if isinstance(type_, ForwardRef):
            type_ = self._resolve_forward_ref(type_)

        if has_annotated_init(type_):
            self._update_forward_ref_owners_registry(type_)

        if type_ is Any:
            return data

        data = self._filter(type_, data)

        handler = self._dispatcher.dispatch(type_)
        try:
            return handler(type_, data, self.forge)
        except (CannotDispatch, TypeError):
            return type_(data)  # type: ignore

    def _resolve_forward_ref(self, type_: ForwardRef) -> Type:
        try:
            owner: Type = self._refs_owners[type_]
        except KeyError:
            raise RuntimeError(f"Unknown forward ref: {type_}")
        return _eval_type(
            type_, vars(sys.modules[owner.__module__]), getattr(owner, "__dict__", {})
        )
