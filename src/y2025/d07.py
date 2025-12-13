from ..helper.grid import Grid2D, Direction, Coordinate2D
from enum import StrEnum
from typing import Self

class Solution:
    @staticmethod
    def solve1(input: str) -> int:
        grid = Grid2D.from_str(input, Manifold)
        start = list(grid.get_coords_by_type(Manifold.START))[0]
        start.walk(Direction.SOUTH)

        new_beams: set[Coordinate2D] = set([start])

        total_splits = 0
        while True:
            if len(new_beams) == 0:
                break

            active_beams = new_beams
            new_beams: set[Coordinate2D] = set()
            for b in active_beams:
                b.walk(Direction.SOUTH)

                if not grid.in_bounds(b):
                    continue

                if grid.get(b) == Manifold.SPLITTER:
                    total_splits += 1
                    left, right = b.copy(), b.copy()
                    left.walk(Direction.WEST)
                    right.walk(Direction.EAST)
                    
                    new_beams.add(left)
                    new_beams.add(right)
                    continue

                new_beams.add(b)

        return total_splits
            
    @staticmethod
    def solve2(input: str) -> int:
        grid = Grid2D.from_str(input, Manifold)
        start = list(grid.get_coords_by_type(Manifold.START))[0]
        start.walk(Direction.SOUTH)

        new_beams: dict[Coordinate2D, int] = {start: 1}
        last_new_beams: dict[Coordinate2D, int] = dict()
        while True:
            if len(new_beams) == 0:
                return sum(last_new_beams.values())

            last_new_beams = new_beams
            active_beams = new_beams
            new_beams: dict[Coordinate2D, int] = dict()
            for b, v in active_beams.items():
                b.walk(Direction.SOUTH)

                if not grid.in_bounds(b):
                    continue

                if grid.get(b) == Manifold.SPLITTER:
                    left, right = b.copy(), b.copy()
                    left.walk(Direction.WEST)
                    right.walk(Direction.EAST)
                    if new_beams.get(left) is not None:
                        new_beams[left] += v
                    else:
                        new_beams[left] = v

                    if new_beams.get(right) is not None:
                        new_beams[right] += v
                    else:
                        new_beams[right] = v

                    continue

                if new_beams.get(b) is not None:
                    new_beams[b] += v
                else:
                    new_beams[b] = v
        return 0

class Manifold(StrEnum):
    START = 'S'
    BEAM = '|'
    SPLITTER = '^'
    EMPTY = '.'
