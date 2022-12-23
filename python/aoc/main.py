from pathlib import Path

from day_eight import day_eight
from day_seven import day_seven
from day_six import day_six
from python.aoc.day_five import day_five
from python.aoc.day_one import day_one
from python.aoc.day_two import day_two
from python.aoc.day_three import day_three
from python.aoc.day_four import day_four


def main():
    file_path_general = "../../data/day_{}"
    print("Day 1")
    day_one(Path(file_path_general.format(1)))

    print("Day 2")
    day_two(Path(file_path_general.format(2)))

    print("Day 3")
    day_three(Path(file_path_general.format(3)))

    print("Day 4")
    day_four(Path(file_path_general.format(4)))

    print("Day 5")
    day_five(Path(file_path_general.format(5)))

    print("Day 6")
    day_six(Path(file_path_general.format(6)))

    print("Day 7")
    day_seven(Path(file_path_general.format(7)))

    print("Day 8")
    day_eight(Path(file_path_general.format(8)))

if __name__ == "__main__":
    main()