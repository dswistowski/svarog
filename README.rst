======
Svarog
======


.. image:: https://img.shields.io/pypi/v/svarog.svg
        :target: https://pypi.python.org/pypi/svarog

.. image:: https://github.com/dswistowski/svarog/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/dswistowski/svarog/actions/workflows/tests.yml

.. image:: https://readthedocs.org/projects/svarog/badge/?version=latest
        :target: https://svarog.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Svarog allow to create object from non typed data. All it need is annotated `__init__` method:


>>> from svarog import forge
... class A:
...     def __init__(self, a: int, b: str):
...       self._a = a
...       self._b = b
...    def __repr__(self):
...        return f'A(a={self._a}, b="{self._b}")'
>>> forge(A, {"a": 1, "b": "3"})
A(a=1, b="3")


More complicated types as `Sequence`, `Mapping`, `Optional` are possible

>>> class A:
...     def __init__(self, b: Sequence[int]):
...         self._b = b
...     def __repr__(self):
...         return f'A(b={self._b})'
>>> forge(A, {"b": "3213"})
A(b=[3, 2, 1, 3])

You can use forward refs:

>>> class WithRef:
...    def __init__(self, child: Optional['WithRef']):
...        self._child = child
...    def __repr__(self):
...        return f"WithRef({self._child!r})"
>>> forge(WithRef(WithRef(WithRef())))
WithRef(WithRef(WithRef(None)))


Objects are forged recursively:


>>> @dataclass
... class A:
...     b: 'B'
...     c: 'C'
... @dataclass
... class B:
...     number: int
... @dataclass
... class C:
...     string: str
>>> forge(A, {'b': {'number': 42}, 'c': {'string': 'the-string'}})
A(b=B(number=42), c=C(string='the-string'))


You can register own forge for your classes:

>>> class FooType(Enum):
...     LOREM = "lorem"
...     IPSUM = "ipsum"
...
... class FooParams:
...     types: ClassVar[Mapping[FooType, "FooParams"]] = {}
...     def __init_subclass__(cls, type: FooType):
...        cls.types[type] = cls
...
...    @classmethod
...    def for_type(cls, type):
...        return cls.types[type]
...
... @dataclass
... class LoremFooParams(FooParams, type=FooType.LOREM):
...     lorem: str
...
... @dataclass
... class IpsumFooParams(FooParams, type=FooType.IPSUM):
...     ipsum: int
...
... @dataclass
... class Foo:
...     type: FooType
...     params: FooParams
...
...     @classmethod
...     def forge(cls, _, data, forge):
...         foo_type = forge(FooType, data["type"])
...         return Foo(
...             type=forge(FooType, foo_type),
...             params=forge(FooParams.for_type(foo_type), data["params"])
...         )
...
>>> register_forge(Foo, Foo.forge)
>>> forge(Foo, {"type": "lorem", "params": {"lorem": "foo-bar"}})
Foo(type=<FooType.LOREM: 'lorem'>, params=LoremFooParams(lorem='foo-bar'))

>>> forge(Foo, {"type": "ipsum", "params": {"ipsum": 42}})
Foo(type=<FooType.IPSUM: 'ipsum'>, params=IpsumFooParams(ipsum=42))


* Free software: MIT license
* Documentation: https://svarog.readthedocs.io.


Features
--------

* Converts unstructured data into structured recursively

  * Works with `dataclasses`
  * Works with `Sequence`, `Mapping`, `Optional`
  * Special conventers for types can be registered with

Credits
-------

Some parts of this code, and concept borrowed from cattrs_ project

.. _Cattrs: https://github.com/Tinche/cattrs

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
