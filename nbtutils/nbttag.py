__all__ = ["NBTTagType", "NBTByte", "NBTShort", "NBTInt", "NBTLong",
           "NBTFloat", "NBTDouble", "NBTByteArray", "NBTString",
           "NBTCompound", "NBTIntArray", "NBTLongArray",
           "NBT_TAG_TYPE_CONSTRUCTOR", "NBTTag"]

import builtins
from enum import Enum
import struct
from typing import Any, Final, Iterable, List, Mapping, Optional, \
                   SupportsIndex, Tuple, Union, cast

class NBTTagType(Enum) :
    TAG_End = 0
    TAG_Byte = 1
    TAG_Short = 2
    TAG_Int = 3
    TAG_Long = 4
    TAG_Float = 5
    TAG_Double = 6
    TAG_Byte_Array = 7
    TAG_String = 8
    TAG_List = 9
    TAG_Compound = 10
    TAG_Int_Array = 11
    TAG_Long_Array = 12

class NBTByte(int) :
    def __new__(cls, val: int=0) :
        val %= 256
        return super().__new__(cls, val if val < 128 else val - 256)

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"{super().__repr__()}b"

class NBTShort(int) :
    def __new__(cls, val: int=0) :
        val %= 65536
        return super().__new__(cls, val if val < 32768 else val - 65536)

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"{super().__repr__()}s"

class NBTInt(int) :
    def __new__(cls, val: int=0) :
        val %= 0x100000000
        return super().__new__(cls, val if val < 0x80000000 \
                                    else val - 0x100000000)

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return super().__repr__()

class NBTLong(int) :
    def __new__(cls, val: int=0) :
        val %= 0x10000000000000000
        return super().__new__(cls, val if val < 0x8000000000000000 \
                                    else val - 0x10000000000000000)

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"{super().__repr__()}L"

class NBTFloat(float) :
    def __new__(cls, val: float=0.) :
        return super().__new__(cls,
                               struct.unpack(">f", struct.pack(">f", val))[0])

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"{super().__repr__()}f"

class NBTDouble(float) :
    def __new__(cls, val: float=0.) :
        return super().__new__(cls,
                               struct.unpack(">d", struct.pack(">d", val))[0])

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"{super().__repr__()}d"

class NBTByteArray([NBTByte()].__class__) :
    def __init__(self, iterable: Iterable[NBTByte]=()) -> None :
        super().__init__(iterable)
        for i in iterable :
            if not builtins.isinstance(i, NBTByte) :
                raise ValueError

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"[B;{','.join(str(x) for x in self)}]"

    def __setitem__(self, key: Any,
                    value: Union[NBTByte, Iterable[NBTByte]]) -> None :
        if not isinstance(value, NBTByte) :
            for i in value :
                if not builtins.isinstance(i, NBTByte) :
                    raise ValueError
        return super().__setitem__(key, value)

    def append(self, object_: NBTByte) -> None :
        if not builtins.isinstance(object_, NBTByte) :
            raise ValueError
        return super().append(object_)

    def insert(self, index: SupportsIndex, object_: NBTByte) -> None :
        if not builtins.isinstance(object_, NBTByte) :
            raise ValueError
        return super().insert(index, object_)

    def extend(self, iterable: Iterable[NBTByte]) -> None:
        for i in iterable :
            if not builtins.isinstance(i, NBTByte) :
                raise ValueError
        return super().extend(iterable)

class NBTString(str) :
    def __new__(cls, object_: object="") :
        S: Final[str] = str(object_)
        if len(S) > 65535 :
            raise ValueError("string is with a length greater than 65535")

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return '"' + self.replace("\\", r"\\").replace('"', r'\"') + '"'

class NBTList(type([])) :
    def __init__(self, iterable: Iterable["NBTTag"]=()) -> None :
        super().__init__(iterable)
        tagtype: Optional[NBTTagType] = None
        for i in iterable :
            if not builtins.isinstance(i, NBTTag) :
                raise ValueError
            if tagtype is None :
                tagtype = i.type
            elif tagtype != i.type :
                raise ValueError

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"[{','.join(str(x) for x in self)}]"

    def __setitem__(self, key: Any,
                    value: Union["NBTTag", Iterable["NBTTag"]]) -> None :
        if not isinstance(value, NBTTag) :
            for i in value :
                if not builtins.isinstance(i, NBTTag) :
                    raise ValueError
                if self and self[0].type != i.type :
                    raise ValueError
        elif self and self[0].type != value.type :
            raise ValueError
        return super().__setitem__(key, value)

    def append(self, object_: "NBTTag") -> None :
        if not builtins.isinstance(object_, NBTTag) :
            raise ValueError
        if self and self[0].type != object_.type :
            raise ValueError
        return super().append(object_)

    def insert(self, index: SupportsIndex, object_: "NBTTag") -> None :
        if not builtins.isinstance(object_, NBTTag) :
            raise ValueError
        if self and self[0].type != object_.type :
            raise ValueError
        return super().insert(index, object_)

    def extend(self, iterable: Iterable["NBTTag"]) -> None:
        for i in iterable :
            if not builtins.isinstance(i, NBTTag) :
                raise ValueError
            if self and self[0].type != i.type :
                raise ValueError
        return super().extend(iterable)

class NBTCompound(type({})) :
    def __init__(self,
                 obj: Union[Mapping[str, "NBTTag"],
                            Iterable[Iterable[Union[str,
                                                    "NBTTag"]]]]=()) -> None :
        getattr(super(), "__init__")(obj)
        for k, v in self.items() :
            if not isinstance(k, str) :
                raise ValueError
            elif len(k) > 65535 :
                raise ValueError("string is with a length greater than 65535")
            if not isinstance(v, NBTTag) :
                raise ValueError

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        if not self :
            return "{}"
        R: Final[List[str]] = ["{"]
        for k, v in self.items() :
            if cast(str, k) and not \
               cast(str, k).\
               strip("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     "abcdefghijklmnopqrstuvwxyz_-.+") :
                R.append(cast(str, k))
            else :
                R.append('"')
                R.append(cast(str, k).replace("\\", r"\\").replace('"', r'\"'))
                R.append('"')
            R.append(f":{v}")
            R.append(",")
        R[-1] = "}"
        return "".join(R)

    def __setitem__(self, key: str, value: "NBTTag") -> None:
        if not isinstance(key, str) :
            raise ValueError
        elif len(key) > 65535 :
            raise ValueError("string is with a length greater than 65535")
        if not isinstance(value, NBTTag) :
            raise ValueError
        return super().__setitem__(key, value)

    def setdefault(self, key: str,
                   default: Optional["NBTTag"]=None) -> Optional["NBTTag"] :
        if not isinstance(key, str) :
            raise ValueError
        elif len(key) > 65535 :
            raise ValueError("string is with a length greater than 65535")
        if default is not None :
            if not isinstance(default, NBTTag) :
                raise ValueError
            return super().setdefault(key, default)

class NBTIntArray([NBTInt()].__class__) :
    def __init__(self, iterable: Iterable[NBTInt]=()) -> None :
        super().__init__(iterable)
        for i in iterable :
            if not builtins.isinstance(i, NBTInt) :
                raise ValueError

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"[I;{','.join(str(x) for x in self)}]"

    def __setitem__(self, key: Any,
                    value: Union[NBTInt, Iterable[NBTInt]]) -> None :
        if not isinstance(value, NBTInt) :
            for i in value :
                if not builtins.isinstance(i, NBTInt) :
                    raise ValueError
        return super().__setitem__(key, value)

    def append(self, object_: NBTInt) -> None :
        if not builtins.isinstance(object_, NBTInt) :
            raise ValueError
        return super().append(object_)

    def insert(self, index: SupportsIndex, object_: NBTInt) -> None :
        if not builtins.isinstance(object_, NBTInt) :
            raise ValueError
        return super().insert(index, object_)

    def extend(self, iterable: Iterable[NBTInt]) -> None:
        for i in iterable :
            if not builtins.isinstance(i, NBTInt) :
                raise ValueError
        return super().extend(iterable)

class NBTLongArray([NBTLong()].__class__) :
    def __init__(self, iterable: Iterable[NBTLong]=()) -> None :
        super().__init__(iterable)
        for i in iterable :
            if not builtins.isinstance(i, NBTLong) :
                raise ValueError

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        return f"[L;{','.join(str(x) for x in self)}]"

    def __setitem__(self, key: Any,
                    value: Union[NBTLong, Iterable[NBTLong]]) -> None :
        if not isinstance(value, NBTLong) :
            for i in value :
                if not builtins.isinstance(i, NBTLong) :
                    raise ValueError
        return super().__setitem__(key, value)

    def append(self, object_: NBTLong) -> None :
        if not builtins.isinstance(object_, NBTLong) :
            raise ValueError
        return super().append(object_)

    def insert(self, index: SupportsIndex, object_: NBTLong) -> None :
        if not builtins.isinstance(object_, NBTLong) :
            raise ValueError
        return super().insert(index, object_)

    def extend(self, iterable: Iterable[NBTLong]) -> None:
        for i in iterable :
            if not builtins.isinstance(i, NBTLong) :
                raise ValueError
        return super().extend(iterable)

NBT_TAG_TYPE_CONSTRUCTOR: Final[Tuple[type, ...]] = \
(type(None), NBTByte, NBTShort, NBTInt, NBTLong, NBTFloat, NBTDouble,
 NBTByteArray, NBTString, NBTList, NBTCompound, NBTIntArray,
 NBTLongArray)

class NBTTag(object) :
    __slots__ = ("type", "value")

    type: Final[NBTTagType]
    value: Final[Union[None, NBTByte, NBTShort, NBTInt, NBTLong, NBTFloat,
                       NBTDouble, NBTByteArray, NBTString, NBTList,NBTCompound,
                       NBTIntArray, NBTLongArray]]

    def __init__(self, arg: Union[NBTTagType, None, NBTByte, NBTShort, NBTInt,
                                  NBTLong, NBTFloat, NBTDouble, NBTByteArray,
                                  NBTString, NBTList, NBTCompound, NBTIntArray,
                                  NBTLongArray]) :
        if isinstance(arg, NBTTagType) :
            self.type = arg
            self.value = NBT_TAG_TYPE_CONSTRUCTOR[cast(int, arg.value)]()
        else :
            for i in range(len(NBT_TAG_TYPE_CONSTRUCTOR)) :
                if isinstance(arg, NBT_TAG_TYPE_CONSTRUCTOR[i]) :
                    self.type = NBTTagType(i)
                    self.value = arg
                    break
            else :
                raise ValueError

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({self.value!r})"

    def __str__(self) -> str :
        return f"{self.value!s}"

    def __eq__(self, value: object) -> bool :
        if isinstance(value, NBTTag) :
            return self.type == value.type and self.value == value.value
        return False

    def __ne__(self, value: object) -> bool :
        if isinstance(value, NBTTag) :
            return self.type != value.type or self.value != value.value
        return True