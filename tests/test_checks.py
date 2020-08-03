from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import pytest

from svarog.checks import has_annotated_init
from svarog.checks import is_bare
from svarog.checks import is_list
from svarog.checks import is_mapping
from svarog.checks import is_union


@pytest.mark.parametrize(
    "type,result", [(Sequence, True), (Dict, False), (Mapping, False)]
)
def test_is_list(type, result):
    assert is_list(type) is result


@pytest.mark.parametrize(
    "type,result",
    [(Optional[str], True), (Union[int, str], True), (Tuple[int, str], False)],
)
def test_is_union(type, result):
    assert is_union(type) is result


class WithAnnotated:
    def __init__(self, a: str):
        ...


@dataclass
class TheDataclass:
    b: int


class WithoutAnnotations:
    def __init__(self, a, b, c):
        ...


@pytest.mark.parametrize(
    "type, result",
    [
        (WithAnnotated, True),
        (TheDataclass, True),
        (WithoutAnnotations, True),
        (str, False),
        (list, False),
    ],
)
def test_has_annotated_init(type, result):
    assert has_annotated_init(type) is result


@pytest.mark.parametrize(
    "type, result",
    [(List, True), (List[Any], False), (Mapping, True), (Mapping[str, Any], False)],
)
def test_is_bare(type, result):
    assert is_bare(type) is result


@pytest.mark.parametrize(
    "type, result", [(List, False), (Mapping, True), (Mapping[str, Any], True)]
)
def test_is_mapping(type, result):
    assert is_mapping(type) is result
