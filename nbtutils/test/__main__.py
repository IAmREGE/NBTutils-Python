from types import ModuleType
from typing import Final, Tuple
import unittest
from . import test_nbtpath, test_nbttag

MODS: Final[Tuple[ModuleType, ...]] = (test_nbtpath, test_nbttag)
[unittest.main(module=i, exit=False) for i in MODS]