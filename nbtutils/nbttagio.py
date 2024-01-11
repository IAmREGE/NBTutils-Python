__all__ = ["writesnbttostream"]

from io import BufferedIOBase
from typing import Final, Iterator, List, Tuple, cast

from .nbttag import NBTCompound, NBTList, NBTTag, NBTTagType

EOF_REACH_MSG: Final[str] = "Stream reached EOF before the payload's end"

def _format_name(name: str) -> bytes :
    RES: Final[List[bytes]] = []
    if str and not str.strip("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                             "abcdefghijklmnopqrstuvwxyz_-.+") :
        name = name.replace("\\", r"\\").replace('"', r'\"')
    for i in name :
        RES.append(bytes((0xed, ord(i)>>6&63|128, ord(i)&63|128)) \
                   if "\ud7ff" < i < "\ue000" else i.encode())
    return b"".join(RES)

def writesnbttostream(tag: NBTTag, stream: BufferedIOBase) -> int :
    if tag.type == NBTTagType.TAG_End :
        return 0
    if tag.type in (NBTTagType.TAG_Byte, NBTTagType.TAG_Short,
                    NBTTagType.TAG_Int, NBTTagType.TAG_Long,
                    NBTTagType.TAG_Float, NBTTagType.TAG_Double,
                    NBTTagType.TAG_Byte_Array, NBTTagType.TAG_Int_Array,
                    NBTTagType.TAG_Long_Array) :
        return stream.write(str(tag.value).encode())
    if tag.type == NBTTagType.TAG_String :
        res: int = 0
        for i in str(tag.value) :
            res += stream.write(bytes((0xed, ord(i)>>6&63|128, ord(i)&63|128))\
                                if "\ud7ff" < i < "\ue000" else i.encode())
        return res
    if tag.type == NBTTagType.TAG_List :
        if not tag.value :
            return stream.write(b"[]")
        res: int = stream.write(b"[")
        ITER: Iterator[NBTTag] = iter(cast(NBTList, tag.value))
        nexttag: NBTTag
        res += writesnbttostream(next(ITER), stream)
        try :
            while 1 :
                nexttag = next(ITER)
                res += stream.write(b",") + writesnbttostream(nexttag, stream)
        except StopIteration :
            pass
        return res + stream.write(b"]")
    if tag.type == NBTTagType.TAG_Compound :
        if not tag.value :
            return stream.write(b"{}")
        res: int = stream.write(b"{")
        ITER2:Iterator[Tuple[str, NBTTag]] = iter(cast(NBTCompound, tag.value))
        nextnametag: Tuple[str, NBTTag] = next(ITER2)
        res += stream.write(_format_name(nextnametag[0])) + stream.write(b":")\
               + writesnbttostream(nextnametag[1], stream)
        try :
            while 1 :
                nextnametag = next(ITER2)
                res += stream.write(b",") + \
                       stream.write(_format_name(nextnametag[0])) + \
                       stream.write(b":") + \
                       writesnbttostream(nextnametag[1], stream)
        except StopIteration :
            pass
        return res + stream.write(b"}")
    raise ValueError("unexpected value error")