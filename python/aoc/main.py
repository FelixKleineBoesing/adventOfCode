from pathlib import Path

from day_eight import day_eight
from day_eleven import day_eleven
from day_fourteen import day_fourteen
from day_seven import day_seven
from day_six import day_six
from day_thirteen import day_thirteen
from python.aoc.day_five import day_five
from python.aoc.day_nine import day_nine
from python.aoc.day_one import day_one
from python.aoc.day_ten import day_ten
from python.aoc.day_twelve import day_twelve
from python.aoc.day_two import day_two
from python.aoc.day_three import day_three
from python.aoc.day_four import day_four


def main(short_run: bool = False):
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

    print("Day 9")
    day_nine(Path(file_path_general.format(9)))

    print("Day 10")
    day_ten(Path(file_path_general.format(10)))

    print("Day 11")
    day_eleven(Path(file_path_general.format(11)))

    print("Day 12")
    if not short_run:
        day_twelve(Path(file_path_general.format(12)))
    else:
        print("Skipping day 12 due to long runtime")

    print("Day 13")
    day_thirteen(Path(file_path_general.format(13)))

    print("Day 14")
    day_fourteen(Path(file_path_general.format(14)))

if __name__ == "__main__":
    main(short_run=True)