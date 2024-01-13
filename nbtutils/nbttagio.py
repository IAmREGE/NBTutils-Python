__all__ = ["writetostream", "writesnbttostream"]

import struct

from io import BufferedIOBase
from typing import Final, Iterator, List, Tuple, cast

from .nbttag import NBTByteArray, NBTCompound, NBTIntArray, NBTList, NBTLongArray, NBTString, NBTTag, NBTTagType

EOF_REACH_MSG: Final[str] = "Stream reached EOF before the payload's end"

def _format_name(name: str) -> bytes :
    if not name :
        return b'""'
    RES: Final[List[bytes]] = []
    if name.strip("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "abcdefghijklmnopqrstuvwxyz_-.+") :
        name = '"' + name.replace("\\", r"\\").replace('"', r'\"') + '"'
    for i in name :
        RES.append(bytes((0xed, ord(i)>>6&63|128, ord(i)&63|128)) \
                   if "\ud7ff" < i < "\ue000" else i.encode())
    return b"".join(RES)

def writetostream(tag: NBTTag, stream: BufferedIOBase) -> int :
    if tag.type == NBTTagType.TAG_End :
        return 0
    if tag.type == NBTTagType.TAG_Byte :
        return stream.write(struct.pack(">b", tag.value))
    if tag.type == NBTTagType.TAG_Short :
        return stream.write(struct.pack(">h", tag.value))
    if tag.type == NBTTagType.TAG_Int :
        return stream.write(struct.pack(">i", tag.value))
    if tag.type == NBTTagType.TAG_Long :
        return stream.write(struct.pack(">l", tag.value))
    if tag.type == NBTTagType.TAG_Float :
        return stream.write(struct.pack(">f", tag.value))
    if tag.type == NBTTagType.TAG_Double :
        return stream.write(struct.pack(">d", tag.value))
    if tag.type == NBTTagType.TAG_Byte_Array :
        return stream.\
               write(struct.pack(f">i{len(cast(NBTByteArray, tag.value))}s",
                                 len(cast(NBTByteArray, tag.value)),
                                 bytes(cast(NBTByteArray, tag.value))))
    if tag.type == NBTTagType.TAG_String :
        BYTES: Final[bytes] = \
        b"".join(bytes((0xed, ord(i)>>6&63|128, ord(i)&63|128)) \
                 if "\ud7ff" < i < "\ue000" else i.encode() \
                 for i in cast(NBTString, tag.value))
        return stream.write(struct.pack(f">H{len(BYTES)}s", len(BYTES), BYTES))
    if tag.type == NBTTagType.TAG_List :
        if tag.value :
            return stream.write(bytes((cast(NBTTagType,
                                            cast(NBTList,
                                                 tag.value)[0].type).value,)))\
                 + stream.write(struct.pack(">i", len(cast(NBTList,
                                                           tag.value)))) + \
                   sum(writetostream(i, stream) for i in cast(NBTList,
                                                              tag.value))
        return stream.write(bytes((NBTTagType.TAG_End.value, 0, 0, 0, 0)))
    if tag.type == NBTTagType.TAG_Compound :
        return sum(stream.write(bytes((cast(NBTCompound,
                                            tag.value)[i].type.value,)))+\
                   writetostream(NBTTag(NBTString(i)), stream)+\
                   writetostream(cast(NBTCompound, tag.value)[i], stream)\
                   for i in cast(NBTCompound, tag.value)) + \
               stream.write(bytes((NBTTagType.TAG_End.value,)))
    if tag.type == NBTTagType.TAG_Int_Array :
        return stream.\
               write(struct.pack(f">i{len(cast(NBTIntArray, tag.value))*4}s",
                                 len(cast(NBTIntArray, tag.value)),
                                 b"".join(i.to_bytes(4, "big",signed=True) for\
                                          i in cast(NBTIntArray, tag.value))))
    if tag.type == NBTTagType.TAG_Long_Array :
        return stream.\
               write(struct.pack(f">i{len(cast(NBTLongArray, tag.value))*8}s",
                                 len(cast(NBTLongArray, tag.value)),
                                 b"".join(i.to_bytes(8, "big",signed=True) for\
                                          i in cast(NBTLongArray, tag.value))))
    raise ValueError

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
        ITER2: Iterator[Tuple[str, NBTTag]] = \
        iter(cast(NBTCompound, tag.value).items())
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