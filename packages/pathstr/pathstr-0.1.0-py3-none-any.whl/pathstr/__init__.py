from itertools import chain
from typing import Tuple, Union

__version__ = '0.1.0'


class Path:
    SEPARATOR = '/'

    __slots__ = ['_segments']

    def __init__(self, *paths: Union['Path', str]):

        try:
            self._segments = tuple(chain(*[path.strip(self.SEPARATOR).split(self.SEPARATOR)
                                           if isinstance(path, str) else path.segments
                                           for path in paths]))
        except AttributeError:
            raise ValueError(f'{paths} are not valid values')

    @property
    def segments(self) -> Tuple[str]:
        return self._segments

    def rpush(self, *paths: Union['Path', str]) -> 'Path':
        return self.__class__(self, *paths)

    def lpush(self, *paths: Union['Path', str]) -> 'Path':
        return self.__class__(*paths, self)

    def rpop(self, count: int = 1) -> Tuple['Path', 'Path']:
        if not isinstance(count, int):
            raise ValueError('Count must be an integer')
        elif count <= 0:
            return self, self.__class__()

        elif count >= len(self):
            return self.__class__(), self

        return self.__class__(*self._segments[:-count]), self.__class__(*self._segments[-count:])

    def lpop(self, count: int = 1) -> Tuple['Path', 'Path']:
        if not isinstance(count, int):
            raise ValueError('Count must be an integer')
        elif count <= 0:
            return self.__class__(), self
        elif count >= len(self):
            return self, self.__class__()

        return self.__class__(*self._segments[:count]), self.__class__(*self._segments[count:])

    def _normalize_other(self, other: Union['Path', str]) -> 'Path':
        if not isinstance(other, (Path, str)):
            raise ValueError(f'{other} is not a valid dialog path')
        if isinstance(other, str):
            return self.__class__(other)

        return other

    def startswith(self, other: Union['Path', str]) -> bool:
        other = self._normalize_other(other)

        return other.segments == self.segments[:len(other)]

    def endswith(self, other: Union['Path', str]) -> bool:
        other = self._normalize_other(other)

        return other.segments == self.segments[-len(other):]

    def common_parent(self, other: Union['Path', str]):
        other = self._normalize_other(other)

        if self.startswith(other):
            return other
        elif other.startswith(self):
            return self
        elif len(self) > len(other):
            base = other
        else:
            base = self

        for idx in range(len(base)):
            if self[idx] != other[idx]:
                return self[:idx]

    def iter_parents(self):
        for idx in range(1, len(self) - 1):
            parent_path = self[:idx]
            yield parent_path

    def __iter__(self):
        return self.iter_parents()

    def __str__(self):
        return self.SEPARATOR.join(self._segments)

    def __repr__(self):
        return f'{self.__class__.__name__}({self})'

    def __len__(self):
        return len(self._segments)

    def __eq__(self, other: Union['Path', str]) -> bool:
        try:
            other = self._normalize_other(other)
        except ValueError:
            return False

        return self.segments == other.segments

    def __contains__(self, other: Union['Path', str]) -> bool:
        try:
            other = self._normalize_other(other)
        except ValueError:
            return False

        return other.startswith(self)

    def __add__(self, other: Union['Path', str]) -> 'Path':
        other = self._normalize_other(other)

        return self.rpush(other)

    def __radd__(self, other: Union['Path', str]) -> 'Path':
        other = self._normalize_other(other)

        return self.lpush(other)

    def __sub__(self, other: Union['Path', str]) -> 'Path':
        other = self._normalize_other(other)

        if not self.endswith(other):
            raise ValueError(f'{self} does not end with {other}')

        result, _ = self.rpop(len(other))
        return result

    def __rsub__(self, other: Union['Path', str]) -> 'Path':
        other = self._normalize_other(other)

        return other.__sub__(self)

    def __rshift__(self, other: int) -> 'Path':
        _, result = self.lpop(other)
        return result

    def __lshift__(self, other: int) -> 'Path':
        result, _ = self.rpop(other)
        return result

    def __getitem__(self, key) -> 'Path':
        segs = self.segments[key]
        if not isinstance(segs, tuple):
            segs = (segs,)
        return self.__class__(*segs)

    def __reversed__(self) -> 'Path':
        return self.__class__(*reversed(self.segments))
