from __future__ import print_function, absolute_import

from . import patch
from .build import build_rust
from .build_ext import build_ext
from .check import check_rust
from .clean import clean_rust
from .extension import RustExtension
from .test import test_rust
from .tomlgen import tomlgen_rust, find_rust_extensions
from .utils import Binding, Strip

__all__ = (
    "RustExtension",
    "Binding",
    "Strip",
    "check_rust",
    "clean_rust",
    "build_ext",
    "build_rust",
    "test_rust",
)


patch.monkey_patch_dist(build_ext)
