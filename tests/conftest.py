import pytest

from svarog import Svarog
from svarog.types import Forge


@pytest.fixture
def svarog() -> Svarog:
    return Svarog()


@pytest.fixture
def forge(svarog) -> Forge:
    return svarog.forge


@pytest.fixture
def register_forge(svarog):
    return svarog.register_forge
