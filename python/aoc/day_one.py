import os
from pathlib import Path
from typing import List


def day_one(file_path: Path):
    lines = read_file(file_path)
    max_calorie_elf, max_calories = find_max_calorie_elf(lines)
    print("Max calorie elf: {}, max_calories: {}".format(max_calorie_elf, max_calories))


def read_file(file_path: Path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines


def find_max_calorie_elf(lines: List[str]):
    max_calorie_elf = 1
    max_calories = 0
    current_calories = 0
    current_elf = 1
    for line in lines:
        line = line.replace("\n", "")
        if len(line) == 0:
            if current_calories > max_calories:
                max_calories = current_calories
                max_calorie_elf = current_elf

            current_elf += 1
            current_calories = 0
        else:
            current_calories += int(line)

    return max_calorie_elf, max_calories
