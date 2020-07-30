def test_can_build_primitive_str(build):
    assert build(str, "the-string") == "the-string"


def test_can_build_primitive_int(build):
    assert build(int, "3") == 3


def test_can_build_none(build):
    assert build(None, None) is None
