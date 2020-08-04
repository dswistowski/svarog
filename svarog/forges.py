import inspect
from functools import lru_cache
from typing import Any
from typing import ForwardRef
from typing import List
from typing import Mapping
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from .checks import is_bare
from .compat import get_args
from .types import CannotDispatch
from .types import Forge
from .types import NoneType


T = TypeVar("T")


@lru_cache()
def _cached_defaults(thingy):
    parameters = inspect.signature(thingy).parameters
    return {
        name: parameter.default
        for name, parameter in parameters.items()
        if parameter.default != inspect._empty  # type: ignore
    }


def _clean_annotations(annotated):
    if annotated.__annotations__ == {}:
        for varname in annotated.__code__.co_varnames:
            if varname != "self":
                yield varname, Any
    else:
        for name, value in annotated.__annotations__.items():
            if isinstance(value, str):
                yield name, ForwardRef(value)
            else:
                yield name, value


def forge_none(type_: NoneType, data: Any, forge: Forge) -> None:
    return None


def forge_annotated_init(type_: Type[T], data: Any, forge: Forge) -> T:
    if not hasattr(data, "items"):
        raise CannotDispatch()

    forged = {
        name: forge(value, data[name])
        for name, value in _clean_annotations(type_.__init__)
        if name != "return" and name in data
    }

    return type_(**_cached_defaults(type_.__init__), **forged)  # type: ignore


def forge_union(union: Union, data: Any, forge: Forge) -> Optional[T]:
    params = union.__args__  # type: ignore
    if NoneType in params:
        if data is None:
            return None

        if len(params) == 2:
            first, second = params
            other = first if second is NoneType else second
            return forge(other, data)

    raise NotImplementedError("Unions other as optionals are not supported yet")


def forge_list(type_: Type[List], list_: List, forge: Forge) -> List:
    if is_bare(type_):
        return list(list_)
    element_type = get_args(type_)[0]
    if element_type is Any:
        return list(list_)
    return [forge(element_type, element) for element in list_]


def forge_mapping(type_: Type[Mapping], mapping: Mapping, forge: Forge) -> Mapping:
    if is_bare(type_):
        return dict(mapping)
    key_arg, value_arg = type_.__args__  # type: ignore
    return {forge(key_arg, k): forge(value_arg, v) for k, v in mapping.items()}
