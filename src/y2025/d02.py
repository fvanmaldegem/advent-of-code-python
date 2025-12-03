class Solution:
    @staticmethod
    def solve1(input: str) -> int:
        answer = 0
        for r in input.replace("\n", "").split(','):
            for id in get_ids_from_range(r):
                if is_invalid_id_1(str(id)):
                    answer += id
        
        return answer

    @staticmethod
    def solve2(input: str) -> int:
        answer = 0
        for r in input.replace("\n", "").split(','):
            for id in get_ids_from_range(r):
                if is_invalid_id_2(str(id)):
                    answer += id
        
        return answer

def get_ids_from_range(r: str) -> list[int]:
    ids = []
    [start, stop] = r.split('-')
    for i in range(int(start), int(stop)+1):
        ids.append(i)

    return ids

def is_invalid_id_1(s: str) -> bool:
    h = int(len(s)/2)
    return s[:h] == s[h:]

def is_invalid_id_2(s: str) -> bool:
    l = len(s)
    dividable_by = [i for i in range(2, l+1) if l % i == 0]

    for d in dividable_by:
        parts = split_str(s, d)
        if parts.count(parts[0]) == len(parts):
            return True
        
    return False

def split_str(s: str, i: int) -> list[str]:
    part_len = int(len(s) / i)

    parts = []
    tmp_s = ""
    for j in range(len(s)):
        tmp_s += s[j]
        if (j + 1) % part_len == 0:
            parts.append(tmp_s)
            tmp_s = ""


    return parts