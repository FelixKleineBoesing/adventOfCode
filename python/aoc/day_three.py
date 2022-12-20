import string
from pathlib import Path
from typing import List

from python.aoc.shared import read_file

PRIORITY_MAPPING = {c: i + 1 for i, c in enumerate(string.ascii_lowercase)}
PRIORITY_MAPPING.update({k: v + 26 for k, v in PRIORITY_MAPPING})


def day_three(file_path: Path):
    lines = read_file(file_path)


def get_priority_sum(lines: List[str]):
    sum_prio = 0
    for line in lines:
        mid = len(line)/2
        first = set(list(line[:mid]))
        second = set(list(line[mid:]))
        diff = first.intersection(second)
        sum_prio += get_prio_values(diff)
    return sum_prio

def get_prio_values(diff: set):
    return [PRIORITY_MAPPING[char] for char in diff]

