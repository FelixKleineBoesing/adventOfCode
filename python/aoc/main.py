from pathlib import Path

from python.aoc.day_one import day_one
from python.aoc.day_two import day_two
from python.aoc.day_three import day_three

def main():
    file_path_general = "../../data/day_{}.txt"
    print("Day 1")
    day_one(Path(file_path_general.format(1)))
    print("Day 2")
    day_two(Path(file_path_general.format(2)))

    print("Day 3")
    day_three(Path(file_path_general.format(3)))


if __name__ == "__main__":
    main()