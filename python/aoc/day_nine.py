import math
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
            position_head[coord_index] += direction
            position_tail = update_knot(position_tail, position_head)
            tail_trajectory.append(tuple(position_tail))

    distinct_positions = set(tail_trajectory)
    print("There are {} distinct positions".format(len(distinct_positions)))


def day_nine_part_two(file_path: Path):
    lines = read_file_clean(file_path)
    number_of_knots = 10
    positions = {i: [0, 0] for i in range(number_of_knots)}
    tail_trajectory = []
    for line in lines:
        coord_index, direction, steps = parse_direction(line)
        for i in range(steps):
            positions[0][coord_index] += direction
            for j in range(1, number_of_knots):
                positions[j] = update_knot(positions[j], positions[j - 1])
            tail_trajectory.append(tuple(positions[number_of_knots - 1]))
    distinct_positions = set(tail_trajectory)
    print("There are {} distinct positions with {} knots".format(len(distinct_positions),number_of_knots))


def update_knot(position_tail, pos_head):
    x_diff, y_diff = position_tail[0] - pos_head[0], position_tail[1] - pos_head[1]
    distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
    sum_distances = int(abs(x_diff) + abs(y_diff))
    distance_diagonal = math.sqrt(2)
    # distance when head is moving straight vertical/horzitontally
    if sum_distances == 2.0 and not distance == distance_diagonal:
        if x_diff == 0:
            y_pos_change = y_diff // 2
            x_pos_change = 0
        else:
            x_pos_change = x_diff // 2
            y_pos_change = 0
    # distance when head is moving diagonally
    elif sum_distances == 3:
        if abs(x_diff) > abs(y_diff):
            x_pos_change = x_diff // 2
            y_pos_change = y_diff
        else:
            x_pos_change = x_diff
            y_pos_change = y_diff // 2
    elif sum_distances == 4:
        x_pos_change = x_diff // 2
        y_pos_change = y_diff // 2
    else:
        x_pos_change = 0
        y_pos_change = 0
    if sum_distances > 4:
        raise Exception("Distance is too large")
    new_tail_pos = [position_tail[0] - x_pos_change, position_tail[1] - y_pos_change]
    return new_tail_pos


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
