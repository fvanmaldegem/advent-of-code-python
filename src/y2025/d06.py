from ..helper.grid import Grid2D
from enum import Enum
from ..helper import common
import math

class Solution:
    @staticmethod
    def solve1(input: str) -> int:
        grid = Grid2D.from_str(input, Value, sep_h=None)
        total = 0
        for col in grid.get_columns():
            total_col = 0
            operator = col[-1].value
            numbers = [int(v.value) for v in col[:-1]]
            total += handle_operator(numbers, operator)
        return total

    @staticmethod
    def solve2(input: str) -> int:
        lines = input.splitlines()
        n_lines = len(lines)
        operator_line: int = lines[-1]
        
        total = 0
        start_index = 0
        for i in range(1, len(operator_line)):
            c = operator_line[i]
            if c != ' ':
                col: list[str] = [s[start_index:i - 1] for s in lines[:-1]]
                total += cephalopod_math(col, operator_line[start_index])
                start_index = i

        col: list[str] = [s[start_index:] for s in lines[:-1]]
        total += cephalopod_math(col, operator_line[start_index])

        return total


def cephalopod_math(numbers: list[str], operator: str) -> int:
    l = len(numbers[0])
    new_numbers = list()
    for i in range(l):
        i = l - i - 1
        new_number = int(''.join([n[i] for n in numbers]))
        new_numbers.append(new_number)

    return handle_operator(new_numbers, operator)

def handle_operator(numbers: list[int], operator: str) -> int:
    match operator:
        case '+':
            return sum(numbers)
        case '*':
            return math.prod(numbers)




class Value:
    def __init__(self, v):
        self.value = v
