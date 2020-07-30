from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Sequence


def test_can_build_primitive_str(build):
    assert build(str, "the-string") == "the-string"


def test_can_build_primitive_int(build):
    assert build(int, "3") == 3


def test_can_build_none(build):
    assert build(None, None) is None


def test_can_build_dataclass(build):
    @dataclass
    class A:
        foo: str

    assert build(A, {"foo": "bar"}) == A(foo="bar")


def test_can_build_optional(build):
    assert build(Optional[str], None) is None
    assert build(Optional[str], "str") == "str"


def test_can_build_list(build):
    assert build(list, [1, 2, "fooo"]) == [1, 2, "fooo"]


def test_can_build_bare_list(build):
    assert build(Sequence, (1, 3, "2")) == [1, 3, "2"]


def test_can_build_list_of_any(build):
    assert build(Sequence[Any], (1, 3, "2")) == [1, 3, "2"]


def test_can_build_typed_list(build):
    assert build(Sequence[int], (1, 3, "2")) == [1, 3, 2]
