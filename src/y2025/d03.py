class Solution:
    def solve1(input: str) -> int:
        total = 0
        for line in input.splitlines():
            bank = [int(i) for i in line]
            total += solve(bank, 2)

        return total

    @staticmethod
    def solve2(input: str) -> int:
        total = 0
        for line in input.splitlines():
            bank = [int(i) for i in line]
            total += solve(bank, 12)

        return total

def solve(bank: list[int], depth: int) -> int:
    stop = len(bank) - (depth - 1)
    i, v = max_with_index(bank[:stop])
    if depth <= 1:
        return v
    
    rest_of_bank = bank[i + 1:]
    other_numbers = solve(rest_of_bank, depth - 1)
    total_number = str(v) + str(other_numbers)
    return int(total_number)
        
def max_with_index(numbers: list[int]) -> (int, int):
    value = max(numbers)
    index = numbers.index(value)
    return (index, value)