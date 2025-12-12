def get_largest_str(l: list[str]) -> str:
    largest_str = ""
    for entry in l:
        if len(entry) > len(largest_str):
            largest_str = l

    return largest_str