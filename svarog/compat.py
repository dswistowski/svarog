from typing import Any
from typing import Optional
from typing import Tuple

try:
    from typing import ForwardRef
except ImportError:
    from typing import _ForwardRef as ForwardRef  # type: ignore

try:
    from typing import _SpecialGenericAlias  # type: ignore
except ImportError:

    class _SpecialGenericAlias:  # type: ignore
        ...


try:
    from typing import get_args
except ImportError:

    def get_args(tp: Any) -> Tuple[Any, ...]:
        return tp.__args__


try:
    from typing import get_origin
except ImportError:

    def get_origin(tp: Any) -> Optional[Any]:
        return tp.__origin__


__all__ = ["ForwardRef", "_SpecialGenericAlias", "get_args", "get_origin"]
