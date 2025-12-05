from typing import Self

class Solution:
    @staticmethod
    def solve1(input: str) -> int:
        fresh_ranges: set[FreshRange] = set()
        input = input.split("\n\n")
        for r in input[0].splitlines():
            fresh_ranges.add(FreshRange.from_str(r))

        
        fresh_ingredient_count = 0
        for ingredient_id in [int(i) for i in input[1].splitlines()]:
            for fresh_range in fresh_ranges:
                if fresh_range.contains_id(ingredient_id):
                    fresh_ingredient_count += 1
                    break
        
        return fresh_ingredient_count
    
    @staticmethod
    def solve2(input: str) -> int:
        fresh_ranges: list[FreshRange] = list()
        input = input.split("\n\n")
        for r in input[0].splitlines():
            fresh_ranges.append(FreshRange.from_str(r))

        fresh_ranges.sort(key=lambda r: r.start)

        total_width = 0
        previous: FreshRange = None
        for current in fresh_ranges:
            if previous is None or previous.end < current.start:
                total_width += current.width()
            elif previous.end >= current.start and previous.end < current.end:
                current.start = previous.end + 1
                total_width += current.width()
            else:
                continue

            previous = current
        
        return total_width

class FreshRange():
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def contains_id(self, id: int) -> bool:
        return self.start < id <= self.end

    def width(self) -> int:
        return self.end - self.start + 1
    
    @staticmethod 
    def from_str(s: str) -> Self:
        numbers = s.split('-')
        return FreshRange(int(numbers[0]), int(numbers[1]))


