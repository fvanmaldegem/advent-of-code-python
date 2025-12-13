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
class Coordinate2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_relative(self, direction: Direction, amount: int = 1) -> Self:
        new = self.copy()
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

    def copy(self) -> Self:
        return Coordinate2D(self.x, self.y)

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

class Grid2D(MutableMapping[Coordinate2D, T]):
    def __init__(self, m: list[list[T]], t: T):        
        self.__t = t
        self.__grid: list[list[T]] = m
        self.__size_x = len(self.__grid[0])
        self.__size_y = len(self.__grid)
        self.__max_x = self.__size_x - 1
        self.__max_y = self.__size_y - 1

    def __setitem__(self, k: Coordinate2D, v: T) -> None:
        self.__grid[k.y][k.x] = v

    def __getitem__(self, k: Coordinate2D) -> T:
        return self.__grid[k.y][k.x]

    def __delitem__(self, k: Coordinate2D):
        if not hasattr(t, 'EMPTY'):
            raise Exception(f"{self.__t} does not implement EMPTY")
        self.__grid[k.y][k.x] = self.__t.EMPTY

    def __iter__(self):
        for y in range(self.__size_y):
            for x in range(self.__size_x):
                yield Coordinate2D(x, y)

    def __len__(self) -> int:
        return (self.__size_x) * (self.__size_y)

    def __repr__(self) -> str:
        items: list[list[str]] = list()
        largest_item = 0
        for y in range(self.__size_y):
            r: list[str] = list()
            for x in range(self.__size_x):
                v = self.get(Coordinate2D(x, y)).value

                if largest_item < len(v):
                    largest_item = len(v)

                r.append(v)
            items.append(r)
        
        s = ""
        for r in items:
            for i, c in enumerate(r):
                spacer = ' '
                if i == len(r) - 1:
                    spacer = ''
                s += f"{c:>{largest_item}}{spacer}"
            s += '\n'

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
        
    def get_coords_by_type(self, t: T) -> Iterator[Coordinate2D]:
        return filter(lambda k: self.get(k) == t, self.keys())

    def get_columns(self) -> Iterable[list[T]]:
        for x in range(self.__size_x):
            yield [self.__grid[y][x] for y in range(self.__size_y)]

    def get_rows(self, i: int) -> Iterable[list[T]]:
        for y in range(self.__size_y):
            yield self.__grid[y]

    @staticmethod
    def from_str(s: str, t: T, sep_v: str = "\n", sep_h: str = None) -> Self:
        split_h = lambda s: s.split(sep_h)
        if sep_h is None:
            split_h = lambda s: list(s)
        
        return Grid2D[T]([[t(v) for v in split_h(h)] for h in s.split(sep_v) if h != ""], t)

