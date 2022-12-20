from pathlib import Path

from python.aoc.day_one import day_one

def main():
    file_path_general = "../../data/day_{}.txt"
    day_one(Path(file_path_general.format(1)))



if __name__ == "__main__":
    main()