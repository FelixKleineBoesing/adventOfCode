import string
from pathlib import Path
from typing import List

from python.aoc.shared import read_file

PRIORITY_MAPPING = {c: i + 1 for i, c in enumerate(string.ascii_lowercase)}
PRIORITY_MAPPING.update({k.upper(): v + 26 for k, v in PRIORITY_MAPPING.items()})


def day_three(file_path: Path):
    # First part
    priority_sums = first_part(file_path)
    print("Priority sums: {}".format(priority_sums))

    # Second part
    prio_sum_second = second_part(file_path)
    print("Priority sums second part: {}".format(prio_sum_second))
    return priority_sums


def second_part(file_path: Path):
    sum_prio = 0
    lines = read_file(file_path)
    for i in range(0, len(lines), 3):
        group = [set(l.replace("\n", "")) for l in lines[i:(i+3)]]
        inter = group[0] & group[1] & group[2]
        sum_prio += PRIORITY_MAPPING[inter.pop()]

    return sum_prio


def first_part(file_path: Path):
    lines = read_file(file_path)
    priority_sums = get_priority_sum(lines)
    return priority_sums


def get_priority_sum(lines: List[str]):
    sum_prio = 0
    for line in lines:
        line = line.replace("\n", "")
        mid = len(line)//2
        first = line[:mid]
        second = line[mid:]
        duplicate = find_duplicate(first, second)
        if duplicate:
            sum_prio += PRIORITY_MAPPING[duplicate]
    return sum_prio


def find_duplicate(*args):
    first, others = args[0], args[1:]
    for f in first:
        for arg in others:
            if f not in arg:
                break
            return f

if __name__ == "__main__":
    pass