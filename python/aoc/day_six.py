from pathlib import Path

from shared import read_file_clean


def day_six(file_path: Path):
    print("Part 1")
    day_six_part_one(file_path)
    print("Part 2")
    day_six_part_two(file_path)


def day_six_part_one(file_path: Path):
    search_marker(file_path, 4)


def day_six_part_two(file_path: Path):
    search_marker(file_path, 14)


def search_marker(file_path: Path, len_distinct: int = 4):
    lines = read_file_clean(file_path)
    string = lines[0]
    for i in range(len_distinct, len(string)):
        if len(set(string[(i - len_distinct):i])) == len_distinct:
            break
    print("Starter pos: {}".format(i))