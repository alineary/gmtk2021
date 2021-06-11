def clamp(num: int, min_value: int, max_value: int):
    return max(min(num, max_value), min_value)


def is_in_range(num, min, max):
    return min <= num <= max
