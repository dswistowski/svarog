from typing import Any
from typing import List
from typing import Mapping
from typing import Union

import pytest

from svarog.forges import forge_annotated_init
from svarog.forges import forge_list
from svarog.forges import forge_mapping
from svarog.forges import forge_none
from svarog.forges import forge_union
from svarog.types import CannotDispatch
from svarog.types import NoneType


def test_forge_none_should_return_always_none(forge):
    assert forge_none(NoneType, Any, forge) is None


def test_forge_union_should_work_with_optional(forge):
    assert forge_union(Union[str, None], 42, forge) == "42"


def test_forge_union_should_work_with_optional_if_none(forge):
    assert forge_union(Union[str, None], None, forge) is None


def test_forge_list_should_work_with_bare_lists(forge):
    assert forge_list(List, ("foo", 42), forge) == ["foo", 42]


def test_forge_list_should_work_with_non_bare_list(forge):
    assert forge_list(List[int], ("42", "3", "14"), forge) == [42, 3, 14]


@pytest.mark.parametrize(
    "type,data,result",
    [
        (Mapping, {"foo": "bar"}, {"foo": "bar"}),
        (Mapping[str, str], {42: 24}, {"42": "24"}),
        (Mapping[str, Any], {42: 24}, {"42": 24}),
        (Mapping[Any, str], {42: 24}, {42: "24"}),
    ],
)
def test_forge_mapping(forge, type, data, result):
    assert forge_mapping(type, data, forge) == result


def test_forge_annotated_init_should_reject_forging_non_mappings(forge):
    def foo(a):
        assert False

    with pytest.raises(CannotDispatch):
        forge_annotated_init(foo, "non-dict", forge)


def test_forge_annotated_init_should_apply_without_change_if_no_types(forge):
    class A:
        def __init__(self, a):
            self.a = a

    assert forge_annotated_init(A, {"a": 42}, forge).a == 42


def test_forge_annotated_init_should_apply_type_if_not_any(forge):
    class A:
        def __init__(self, a: str):
            self.a = a

    assert forge_annotated_init(A, {"a": 42}, forge).a == "42"
