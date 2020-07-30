import pytest

from svarog import Builder
from svarog.types import Build


@pytest.fixture
def builder() -> Builder:
    return Builder()


@pytest.fixture
def build(builder: Builder) -> Build:
    return builder.build
