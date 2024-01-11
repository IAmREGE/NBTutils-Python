__all__ = ["Test"]

from typing import Final
import unittest

from ..nbtpath import NBTPath

class Test(unittest.TestCase) :
    def test_new(self) :
        PATH: Final[NBTPath] = NBTPath(("Foo", 1, "bar", -2, "Baz "))
        self.assertEqual(PATH, ("Foo", 1, "bar", -2, "Baz "))
        self.assertEqual(str(PATH), 'Foo[1].bar[-2]."Baz "')
        self.assertRaises(ValueError, NBTPath, (3.14,))

    def test_slice(self) :
        PATH: Final[NBTPath] = NBTPath(("Foo", 1, "bar", -2, "Baz "))
        self.assertEqual(PATH[-3], "bar")
        self.assertEqual(PATH[1:4], NBTPath((1, "bar", -2)))
        self.assertEqual(PATH[::-1], NBTPath(("Baz ", -2, "bar", 1, "Foo")))

if __name__ == "__main__" :
    unittest.main()