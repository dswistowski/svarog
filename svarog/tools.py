import re

CAMEL_RE_PRE = re.compile("(.)([A-Z][a-z]+)")
CAMEL_RE_POST = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake(name: str) -> str:
    name = CAMEL_RE_PRE.sub(r"\1_\2", name)
    return CAMEL_RE_POST.sub(r"\1_\2", name).lower()
