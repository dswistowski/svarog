"""Top-level package for Svarog."""

__author__ = """Damian Świstowski"""
__email__ = "damian@swistowski.org"
__version__ = "0.1.2"

from .svarog import Svarog

default_builder = Svarog()

forge = default_builder.forge
register_forge = default_builder.register_forge

__all__ = ["forge"]
