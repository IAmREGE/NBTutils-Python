#!/usr/bin/env python3

import sys
from typing import Final

from .nbttag import NBTTagType, NBTTag
from .nbttagio import writesnbttostream

def print_help() -> None :
    print(f"Usage: {sys.argv[0]} read [<filename>]")

ARGC: Final[int] = len(sys.argv)

if ARGC == 1 :
    print_help()