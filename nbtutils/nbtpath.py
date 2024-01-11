import builtins

from typing import Final, Iterable, List, SupportsIndex, Tuple, Union

class NBTPath(((len(""), repr(0))*2).__class__) :
    def __new__(cls, iterable: Iterable[Union[int, str]]=()) :
        for i in iterable :
            if not builtins.isinstance(i, (int, str)) :
                raise ValueError
        return super().__new__(cls, iterable)

    def __repr__(self) -> str :
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str :
        if self.isroot() :
            return "{}"
        R: Final[List[str]] = []
        for i in self :
            if isinstance(i, int) :
                R.append(f"[{i}]")
            elif isinstance(i, str) :
                if any(x in i for x in "{}[].'\" ") or not i:
                    R.append('."' if R else '"')
                    R.append(i.replace("\\", r"\\").replace('"', r'\"'))
                    R.append('"')
                else :
                    R.append(f".{i}" if R else i)
        return "".join(R)

    def isroot(self) -> bool :
        return not self

    def __getitem__(self, key: Union[SupportsIndex, slice]) :
        R: Final[Union[int, str, Tuple[Union[int, str], ...]]] = \
        super().__getitem__(key)
        return R if isinstance(R, (int, str)) else type(self)(R)