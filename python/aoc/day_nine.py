from pathlib import Path

from shared import read_file_clean


def day_nine(file_path: Path):
    print("Part 1")
    day_nine_part_one(file_path)
    print("Part 2")
    day_nine_part_two(file_path)


def day_nine_part_one(file_path: Path):
    lines = read_file_clean(file_path)
    position_tail = [0, 0]
    position_head = [0, 0]
    tail_trajectory = []
    for line in lines:
        coord_index, direction, steps = parse_direction(line)
        for i in range(steps):
            position_tail[coord_index] += direction
            tail_trajectory.append(tuple(position_tail))



def day_nine_part_two(file_path: Path):
    pass


def parse_direction(line: str) -> (int, int, int):
    """

    :param line:
    :return: coord index, direction, distance
    """
    direction, steps = line.split(" ")
    if direction == "R":
        return 1, 1, int(steps)
    if direction == "L":
        return 1, -1, int(steps)
    if direction == "U":
        return 0, -1,  int(steps)
    if direction == "D":
        return 0, 1, int(steps)
