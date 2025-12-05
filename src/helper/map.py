from typing import Any, Self, TypeVar, Generic
from collections.abc import Iterator, Mapping, MutableMapping, Callable, Iterable, MappingView, ItemsView
from enum import Enum, StrEnum
from functools import total_ordering


class Position(StrEnum):
    EMPTY = '.'

T = TypeVar('T', bound=Position)
Identity = Callable[[T], T]

class Direction(tuple[int, int], Enum):
    NORTH      = (0, -1)
    NORTHEAST  = (1, -1)
    EAST       = (1, 0)
    SOUTHEAST  = (1, 1)
    SOUTH      = (0, 1)
    SOUTHWEST  = (-1, 1)
    WEST       = (-1, 0)
    NORTHWEST  = (-1, -1)

@total_ordering
class Coordinate2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_relative(self, direction: Direction, amount: int = 1) -> Self:
        new = Coordinate2D(self.x, self.y)
        new.walk(direction, amount)
        return new

    def adjacent(self) -> Iterator[Self]:
        for d in Direction:
            yield self.get_relative(d, 1)

    def walk(self, direction: Direction, amount: int = 1) -> None:
        x_amount = direction.value[0] * amount
        y_amount = direction.value[1] * amount
        self.x = self.x + x_amount
        self.y = self.y + y_amount

    def __repr__(self) -> str:
        return f"Coordinate2D({self.x},{self.y})"

    def __key(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Coordinate2D):
            return False
        
        return self.__key() == other.__key()

    def __lt__(self, other):
        return self.y < other.y or self.x < other.x

    def __le__(self, other):
        return self.y <= other.y or self.x <= other.x

class Map2D(MutableMapping[Coordinate2D, T]):
    def __init__(self, m: list[list[T]], t: T):
        if not hasattr(t, 'EMPTY'):
            raise Exception(f"{T} does not implement EMPTY")
        
        self.__t = t
        self.__map: list[list[T]] = m
        self.__size_x = len(self.__map[0])
        self.__size_y = len(self.__map)
        self.__max_x = self.__size_x - 1
        self.__max_y = self.__size_y - 1

    def __setitem__(self, k: Coordinate2D, v: T) -> None:
        self.__map[k.y][k.x] = v

    def __getitem__(self, k: Coordinate2D) -> T:
        return self.__map[k.y][k.x]

    def __delitem__(self, k: Coordinate2D):
        self.__map[k.y][k.x] = self.__t.EMPTY

    def __iter__(self):
        for y in range(self.__size_y):
            for x in range(self.__size_x):
                yield Coordinate2D(x, y)

    def __len__(self) -> int:
        return (self.__size_x) * (self.__size_y)

    def __repr__(self) -> str:
        s = ""
        for y in range(self.__size_y):
            for x in range(self.__size_x):
                v = self.get(Coordinate2D(x, y)).value
                s += v
            s += "\n"
        return s

    def __contains__(self, o: object) -> bool:
        if isinstance(o, Coordinate2D):
            return self.in_bounds(o)
        elif isinstance(o, self.__t):
            return o in self.values()
        return False

    def in_bounds(self, k: Coordinate2D) -> bool:
        if k.y < 0 or k.y > self.__max_y:
            return False

        if k.x < 0 or k.x > self.__max_x:
            return False
        
        return True
        
    def get_coords_by_type(self, t: T):
        return filter(lambda k: self.get(k) == t, self.keys())

    @staticmethod
    def from_str(s: str, t: T) -> Self:
        return Map2D[T]([[t(c) for c in l] for l in s.splitlines()], t)
