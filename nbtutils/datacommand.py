__all__ = ["DataOperationResult", "data"]

import builtins
from numbers import Integral, Real
from typing import Dict, Final, Literal, NamedTuple, Optional, Tuple, Union, cast, overload
from .nbttag import NBTByte, NBTByteArray, NBTCompound, NBTDouble, NBTFloat, \
                    NBTInt, NBTIntArray, NBTList, NBTLong, NBTLongArray, \
                    NBTShort, NBTString, NBTTagType, NBTTag
from .nbtpath import NBTPath

class DataOperationResult(NamedTuple) :
    success: bool
    result: int
    tag: Optional[NBTTag]

    def __str__(self) -> str :
        return f"{self.result} {self.tag}" if self.success else "failure"

    @overload
    @classmethod
    def of(cls, arg1: Optional[NBTTag]=None,
           arg2: Real=cast(Real, 1)) -> "DataOperationResult" :
        pass
    @overload
    @classmethod
    def of(cls, arg1: Integral,
           arg2: Optional[NBTTag]) -> "DataOperationResult" :
        pass
    @classmethod
    def of(cls, arg1: Union[Optional[NBTTag], Integral]=None,
           arg2: Union[Real, Optional[NBTTag]]=None) -> "DataOperationResult" :
        if arg1 is None :
            return cls(success=False, result=0, tag=None)
        if isinstance(arg1, NBTTag) :
            if isinstance(arg1.value, (NBTByte, NBTShort, NBTInt, NBTLong,
                                       NBTFloat, NBTDouble)) :
                result: Real = cast(Real, arg2) * arg1.value
                return cls(success=True,
                           result=\
                            0x7fffffff if cast(Real, 0x7fffffff) < result else\
                            (-0x80000000 if result < -0x80000000 else \
                             int(result)), tag=arg1)
            elif isinstance(arg1.value, (NBTByteArray, NBTString, NBTList,
                                         NBTCompound, NBTIntArray,
                                         NBTLongArray)) :
                result: Real = cast(Real, arg2) * len(arg1.value)
                return cls(success=True,
                           result=\
                            0x7fffffff if cast(Real, 0x7fffffff) < result else\
                            (-0x80000000 if result < -0x80000000 else \
                             int(result)), tag=arg1)
            elif arg1.value is None :
                return cls(success=True, result=0, tag=arg1)
            else :
                assert 0
        elif builtins.isinstance(arg1, Integral) :
            if arg2 is None :
                return cls(success=False, result=0, tag=None)
            elif isinstance(arg2, NBTTag) :
                RESULT: Final[int] = arg1 % 0x100000000
                return cls(success=True,
                           result=RESULT if RESULT < 0x80000000 else \
                                  RESULT - 0x100000000, tag=arg2)
        raise ValueError

class data :
    def __new__(cls) :
        raise TypeError("can't instantiate an utility class")

    @classmethod
    def get(cls, tag: NBTTag, path: NBTPath,
            scale: Real=cast(Real, 1)) -> DataOperationResult:
        if path.isroot() :
            return DataOperationResult.of(tag, scale)
        if isinstance(path[0], str) :
            if tag.type != NBTTagType.TAG_Compound or \
               path[0] not in cast(NBTCompound, tag.value) :
                return DataOperationResult.of()
            return cls.get(cast(NBTCompound, tag.value)[path[0]],
                           cast(NBTPath, path[1:]), scale)
        INDEX: Final[int] = cast(int, path[0])
        if tag.type == NBTTagType.TAG_Byte_Array :
            if len(path) > 1 :
                return DataOperationResult.of()
            try :
                return DataOperationResult.\
                       of(NBTTag(cast(NBTByteArray, tag.value)[INDEX]), scale)
            except IndexError :
                return DataOperationResult.of()
        elif tag.type == NBTTagType.TAG_Int_Array :
            if len(path) > 1 :
                return DataOperationResult.of()
            try :
                return DataOperationResult.\
                       of(NBTTag(cast(NBTIntArray, tag.value)[INDEX]), scale)
            except IndexError :
                return DataOperationResult.of()
        elif tag.type == NBTTagType.TAG_Long_Array :
            if len(path) > 1 :
                return DataOperationResult.of()
            try :
                return DataOperationResult.\
                       of(NBTTag(cast(NBTLongArray, tag.value)[INDEX]), scale)
            except IndexError :
                return DataOperationResult.of()
        elif tag.type == NBTTagType.TAG_List :
            try :
                return DataOperationResult.\
                       of(cls.get(cast(NBTList, tag.value)[INDEX],
                                  cast(NBTPath, path[1:]), scale).tag, scale)
            except IndexError :
                return DataOperationResult.of()
        else :
            return DataOperationResult.of()

    @classmethod
    def merge(cls, tag: NBTTag, another: NBTTag) -> DataOperationResult :
        if tag.type != NBTTagType.TAG_Compound or \
           another.type != NBTTagType.TAG_Compound :
            return DataOperationResult.of()
        NEW: Final[NBTCompound] = NBTCompound(cast(NBTCompound, tag.value))
        NEW.update(cast(NBTCompound, another.value))
        return DataOperationResult.of(cast(Integral, 1), NBTTag(NEW))

    '''@overload
    @classmethod
    def modify(cls, tag: NBTTag,
               oper: Literal["append", "merge", "remove", "set"],
               value: NBTTag) -> DataOperationResult :
        pass
    @overload
    @classmethod
    def modify(cls, tag: NBTTag, oper: Literal["insert"], index: int,
               value: NBTTag) -> DataOperationResult :
        pass
    @classmethod
    def modify(cls, tag: NBTTag, oper: Literal["append", "insert", "merge", "remove", "set"], index: Union[int, NBTTag], value: Optional[NBTTag]) :'''