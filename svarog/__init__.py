"""Top-level package for Svarog."""

__author__ = """Damian Świstowski"""
__email__ = "damian@swistowski.org"
__version__ = "0.1.0"

from .builder import Builder

default_builder = Builder()

build = default_builder.build


__all__ = "build"
