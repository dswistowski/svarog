import pytest

from svarog.tools import camel_to_snake


@pytest.mark.parametrize(
    "data,expected",
    [
        ("foo", "foo"),
        ("Bar", "bar"),
        ("loremIpsum", "lorem_ipsum"),
        ("LoremIpsum", "lorem_ipsum"),
    ],
)
def test_camel_to_snake(data, expected):
    assert camel_to_snake(data) == expected
