from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Any
from typing import ClassVar
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Union
from uuid import UUID

import pytest

from svarog.types import NoneType


def test_can_build_primitive_str(forge):
    assert forge(str, "the-string") == "the-string"


def test_can_build_primitive_int(forge):
    assert forge(int, "3") == 3


def test_can_build_none(forge):
    assert forge(NoneType, None) is None


def test_can_build_dataclass(forge):
    @dataclass
    class A:
        foo: str

    assert forge(A, {"foo": "bar"}) == A(foo="bar")


def test_can_build_complicated_dataclass(forge):
    @dataclass
    class A:
        foo: int
        bar: str
        lorem: Sequence[int]

    @dataclass
    class B:
        a: A
        b: Optional[A]
        c: Sequence[A]

    assert forge(
        B,
        {
            "a": {"foo": "3", "bar": "x", "lorem": [1, 3, 4]},
            "b": None,
            "c": [
                {"foo": 1, "bar": 3, "lorem": ["2", "3"]},
                {"foo": 2, "bar": 3, "lorem": []},
            ],
        },
    ) == B(
        a=A(foo=3, bar="x", lorem=[1, 3, 4]),
        b=None,
        c=[A(1, "3", [2, 3]), A(2, "3", [])],
    )


@dataclass
class A:
    b: "B"
    c: "C"


@dataclass
class B:
    number: int


@dataclass
class C:
    letter: str


def test_can_build_dataclass_from_readme(forge):
    assert forge(A, {"b": {"number": 42}, "c": {"letter": "x"}}) == A(B(42), C("x"))


def test_can_build_dataclass_with_optional_values(forge):
    @dataclass
    class A:
        a: int
        b: Sequence[str] = field(default_factory=lambda: ["x"])

    assert forge(A, {"a": 3}) == A(a=3, b=["x"])


def test_can_build_optional(forge):
    assert forge(Optional[str], None) is None
    assert forge(Optional[str], "str") == "str"


def test_can_build_list(forge):
    assert forge(list, [1, 2, "fooo"]) == [1, 2, "fooo"]


def test_can_build_bare_list(forge):
    assert forge(Sequence, (1, 3, "2")) == [1, 3, "2"]


def test_can_build_list_of_any(forge):
    assert forge(Sequence[Any], (1, 3, "2")) == [1, 3, "2"]


def test_can_build_typed_list(forge):
    assert forge(Sequence[int], (1, 3, "2")) == [1, 3, 2]


def test_can_build_dict(forge):
    assert forge(dict, {"foo": "bar"}) == {"foo": "bar"}


def test_can_build_mapping(forge):
    assert forge(Mapping, {"foo": "bar"}) == {"foo": "bar"}


def test_can_build_typed_mapping(forge):
    assert forge(Mapping[str, int], {"foo": 42, 42: "3"}) == {"foo": 42, "42": 3}


def test_can_build_typed_keys_mapping(forge):
    assert forge(Mapping[str, Any], {"foo": 42, 42: "3"}) == {"foo": 42, "42": "3"}


def test_can_build_typed_value_mapping(forge):
    assert forge(Mapping[Any, int], {"foo": 42, 42: "3"}) == {"foo": 42, 42: 3}


class WithRef:
    def __init__(self, child: Optional["WithRef"]):
        self._child = child

    def __eq__(self, other: "WithRef") -> bool:
        return type(self) == type(other) and self._child == other._child


def test_will_work_with_forward_ref(forge):
    assert forge(WithRef, {"child": {"child": None}}) == WithRef(WithRef(None))


def test_non_optional_unions_are_not_supported_yet(forge):
    with pytest.raises(NotImplementedError):
        assert forge(Union[str, int], "3")


def test_can_apply_simple_types(forge, register_forge):
    @dataclass
    class A:
        uuid: UUID

    assert forge(A, {"uuid": "00000000-0000-0000-0000-000000000000"}) == A(UUID(int=0))


def test_can_register_forge(forge, register_forge):
    class FooType(Enum):
        LOREM = "lorem"
        IPSUM = "ipsum"

    class FooParams:
        types: ClassVar[Mapping[FooType, "FooParams"]] = {}

        def __init_subclass__(cls, type: FooType):
            cls.types[type] = cls

        @classmethod
        def for_type(cls, type):
            return cls.types[type]

    @dataclass
    class LoremFooParams(FooParams, type=FooType.LOREM):
        lorem: str

    @dataclass
    class IpsumFooParams(FooParams, type=FooType.IPSUM):
        ipsum: int

    @dataclass
    class Foo:
        type: FooType
        params: FooParams

        @classmethod
        def forge(cls, _, data, forge):
            foo_type = forge(FooType, data["type"])
            return Foo(
                type=forge(FooType, foo_type),
                params=forge(FooParams.for_type(foo_type), data["params"]),
            )

    register_forge(Foo, Foo.forge)

    assert forge(Foo, {"type": "lorem", "params": {"lorem": "foo-bar"}}) == Foo(
        type=FooType.LOREM, params=LoremFooParams("foo-bar")
    )
    assert forge(Foo, {"type": "ipsum", "params": {"ipsum": 42}}) == Foo(
        type=FooType.IPSUM, params=IpsumFooParams(42)
    )


def test_can_build_class_without_annotations(forge):
    class A:
        def __init__(self, a, b):
            self._a = a
            self._b = b

        def __eq__(self, other):
            return (
                type(self) == type(other)
                and self._a == other._a
                and self._b == other._b
            )

    assert forge(A, {"a": 42, "b": "foo-bar"}) == A(42, "foo-bar")
