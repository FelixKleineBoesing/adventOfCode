from pathlib import Path

from python.aoc.shared import read_file_clean


def day_four(file_path: Path):
    day_four_part_one(file_path)
    day_four_part_two(file_path)


def day_four_part_one(file_path: Path):
    lines = read_file_clean(file_path)
    number_complete_intersections = 0
    for line in lines:
        range_one, range_two = line.split(",")
        range_one = split_range(range_one)
        range_two = split_range(range_two)
        if check_if_subset(range_one, range_two):
            number_complete_intersections += 1
    print("Number of complete intersections: {}".format(number_complete_intersections))


def day_four_part_two(file_path: Path):
    lines = read_file_clean(file_path)
    number_any_intersections = 0
    for line in lines:
        range_one, range_two = line.split(",")
        range_one = split_range(range_one)
        range_two = split_range(range_two)
        if check_if_intersection(range_one, range_two):
            number_any_intersections += 1
    print("Number of any intersections: {}".format(number_any_intersections))


def split_range(range: str):
    low, high = range.split("-")
    return int(low), int(high)


def check_if_subset(range_one, range_two):
    def _check_if_subset(r_one, r_two):
        low_one, high_one = r_one
        low_two, high_two = r_two
        if low_one <= low_two and high_one >= high_two:
            return True
        return False

    return _check_if_subset(range_one, range_two) or _check_if_subset(range_two, range_one)


def check_if_intersection(range_one, range_two):
    low_one, high_one = range_one
    low_two, high_two = range_two
    if low_two <= high_one and low_one <= high_two or low_one <= high_two and low_two <= high_one:
        return True
    return False