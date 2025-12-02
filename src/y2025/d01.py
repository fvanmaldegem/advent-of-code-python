from enum import Enum
from typing import Self

class Solution:
    @staticmethod
    def solve1(input: str) -> int:
        dial = Dial()
        for line in input.splitlines():
            direction = Direction.from_char(line[0])
            amount = int(line[1::])
            dial.move(direction, amount)

        return dial.ponted_to_zero_after_move

    @staticmethod
    def solve2(input: str) -> int:
        dial = Dial()
        for line in input.splitlines():
            direction = Direction.from_char(line[0])
            amount = int(line[1::])
            dial.move(direction, amount)

        return dial.pointed_to_zero_after_click

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

    @staticmethod
    def from_char(c: str) -> Self:
        match c.lower():
            case 'l':
                return Direction.LEFT
            case 'r':
                return Direction.RIGHT
        
        raise Exception(f"could not convert '{c}' to a Direction")

class Dial:
    pointer = 50
    pointed_to_zero_after_click = 0
    ponted_to_zero_after_move = 0

    def __move_r(self) -> None:
        self.pointer += 1
        if self.pointer > 99:
            self.pointer = 0
            

    def __move_l(self) -> None:
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = 99

    def move(self, direction: Direction, amount: int) -> None:
        while(amount > 0):
            match direction:
                case Direction.LEFT:
                    self.__move_l()
                case Direction.RIGHT:
                    self.__move_r()
            if self.pointer == 0:
                self.pointed_to_zero_after_click += 1
            
            amount -= 1

        if self.pointer == 0:
            self.ponted_to_zero_after_move += 1

