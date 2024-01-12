__all__ = ["Test"]

from io import BytesIO
from typing import Final
import unittest

from ..nbttag import NBTByte, NBTCompound, NBTList, NBTString, NBTTag
from ..nbttagio import writesnbttostream

class Test(unittest.TestCase) :
    def test(self) :
        STREAM: Final[BytesIO] = BytesIO()
        writesnbttostream(NBTTag(NBTCompound({
            "foo": NBTTag(NBTByte(True)),
            "bar!!!": NBTTag(NBTString("baz")),
            "": NBTTag(NBTList([NBTTag(NBTString(i)) for i in "EMPTY"]))
        })), STREAM)
        STREAM.seek(0)
        self.assertEqual(STREAM.read(),
                         b'{foo:1b,"bar!!!":"baz","":["E","M","P","T","Y"]}')

if __name__ == "__main__" :
    unittest.main()