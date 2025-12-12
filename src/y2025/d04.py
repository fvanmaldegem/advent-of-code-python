from ..helper.grid import Grid2D, Coordinate2D, Direction
from enum import StrEnum

class Solution:
    def solve1(input: str) -> int:
        count = 0
        grid = Grid2D.from_str(input, P)
    
        for pos in grid.get_coords_by_type(P.PAPERROLL):
            adjacent_roll_count = 0
            for adjacent_pos in pos.adjacent():
                if adjacent_pos not in grid:
                    continue

                if grid.get(adjacent_pos) == P.PAPERROLL:
                    adjacent_roll_count += 1

            if adjacent_roll_count < 4:
                count += 1

        return count

    @staticmethod
    def solve2(input: str) -> int:
        count = 0
        grid = Grid2D.from_str(input, P)
    
        while True:
            marks: set[Coordinate2D] = set()

            for pos in grid.get_coords_by_type(P.PAPERROLL):
                adjacent_roll_count = 0
                for adjacent_pos in pos.adjacent():
                    if adjacent_pos not in grid:
                        continue

                    if grid.get(adjacent_pos) == P.PAPERROLL:
                        adjacent_roll_count += 1

                if adjacent_roll_count < 4:
                    marks.add(pos)
            
            if len(marks) == 0:
                break

            for mark in marks:
                grid[mark] = P.EMPTY

            count += len(marks)
        return count

class P(StrEnum):
    EMPTY     = '.'
    PAPERROLL = '@'
    MARK      = 'x'
