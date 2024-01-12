__all__ = ["Test"]

import unittest

from ..nbttag import NBTByte, NBTByteArray, NBTFloat, NBTShort, NBTInt, NBTLong

class Test(unittest.TestCase) :
    def test_new(self) :
        self.assertTrue(NBTByte(123) == NBTShort(123) == NBTInt(123) == \
                        NBTLong(123) == 123)
        self.assertEqual(NBTByte(333), 77)
        self.assertEqual(NBTByteArray((-129, True, False)), [127, 1, 0])

    def test_slice(self) :
        pass

if __name__ == "__main__" :
    unittest.main()