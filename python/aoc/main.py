from pathlib import Path

from python.aoc.day_one import day_one
from python.aoc.day_two import day_two


def main():
    file_path_general = "../../data/day_{}.txt"
    print("Day 1")
    day_one(Path(file_path_general.format(1)))
    print("Day 2")
    day_two(Path(file_path_general.format(2)))



if __name__ == "__main__":
    main()