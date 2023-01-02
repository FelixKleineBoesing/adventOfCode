from pathlib import Path
from typing import Tuple

from shared import read_file_clean


def day_fourteen(file_path: Path):
    print("Part 1")
    day_fourteen_part_one(file_path)
    print("Part 2")
    day_fourteen_part_two(file_path)


value_mapping = {0: ".", 1: "#", 2: "o"}


def print_cave(cave):
    for y in range(cave.len_y-1, -1, -1):
        print(str(y).zfill(3), end = "")
        for x in range(cave.len_x):
            value = value_mapping[cave[x, y]]
            print(value, end="")
        print()


def day_fourteen_part_one(file_path):
    sand_entry = (500, 0)
    lines = read_file_clean(file_path)
    stone_lines, min_x, max_x, min_y, max_y = parse_lines(lines)
    min_x = min(min_x, sand_entry[0])
    max_x = max(max_x, sand_entry[0])
    min_y = min(min_y, sand_entry[1])
    max_y = max(max_y, sand_entry[1])
    standardized_stone_lines = standardize_cave(stone_lines, min_x, min_y)
    sand_entry = (sand_entry[0] - min_x, sand_entry[1] - min_y)
    cave = Cave(max_x + 1 - min_x, max_y + 1 - min_y)
    cave = build_cave(cave, standardized_stone_lines)
    space_full = False
    number_sands = 0
    sands = set()
    while not space_full:
        particle_settled = False
        current_pos = sand_entry
        while not particle_settled:
            move_possible, move_out_of_bound, current_pos = check_if_move_possible(cave, current_pos)
            if not move_possible:
                particle_settled = True

        if move_out_of_bound or current_pos[1] < 0:
            space_full = True
        else:
            cave[current_pos] = 2
            number_sands += 1
            sand_re_stand = (current_pos[0] + min_x, -(current_pos[1] + min_y))
            sands.add(sand_re_stand)
        if current_pos == sand_entry:
            space_full = True

    print("Number of sands: ", number_sands)
    return cave, number_sands


def check_if_move_possible(cave, current_pos):
    inbound_down, free_down = place_free(cave, current_pos, (0, -1))
    inbound_left, free_left = place_free(cave, current_pos, (-1, -1))
    inbound_right, free_right = place_free(cave, current_pos, (1, -1))

    if inbound_down and free_down:
        new_pos = move_particle(current_pos, (0, -1))
        return free_down, inbound_down, new_pos
    elif inbound_left and free_left:
        new_pos = move_particle(current_pos, (-1, -1))
        return free_left, inbound_left, new_pos
    elif inbound_right and free_right:
        new_pos = move_particle(current_pos, (1, -1))
        return inbound_right, free_right, new_pos
    return False, not (inbound_right and inbound_left and inbound_right), current_pos


def place_free(cave, current_pos, direction):
    xn, yn = current_pos[0] + direction[0], current_pos[1] + direction[1]
    if cave.inbound(xn, yn):
        if cave[xn, yn] == 0:
            return True, True
    else:
        return False, False
    return True, False


def move_particle(current_pos, direction):
    return current_pos[0] + direction[0], current_pos[1] + direction[1]


def check_if_space_empty(cave, current_pos, direction: tuple):
    if cave[current_pos[0] + direction[0], current_pos[1] + direction[1]] == 0:
        return
    return False


class Cave:

    def __init__(self, len_x, len_y):
        self.len_x = len_x
        self.len_y = len_y
        self.grid = [[0 for _ in range(len_y)] for _ in range(len_x)]

    def __getitem__(self, item):
        if item[0] >= self.len_x or item[0] < 0:
            raise IndexError("X Axis out of bounds with value {}".format(item[0]))
        if item[1] >= self.len_y or -self.len_y > item[1]:
            raise IndexError("Y Axis out of bounds with value: {}".format(item[1]))
        return self.grid[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.grid[key[0]][key[1]] = value

    def shape(self):
        return self.len_x, self.len_y

    def inbound(self, x = None, y = None):
        inbound = True
        inbound = inbound and x < self.len_x and x >= 0
        inbound = inbound and y < self.len_y and -self.len_y < y
        return inbound


def standardize_cave(stone_lines, x_min: int, y_min: int):
    standardized_stone_lines = []
    for stone_line in stone_lines:
        nodes = []
        for node in stone_line:
            nodes.append((node[0] - x_min, node[1] - y_min))
        standardized_stone_lines.append(nodes)
    return standardized_stone_lines


def parse_lines(lines):
    stone_lines = []
    min_x, max_x, min_y, max_y = 1e10, 0, 1e10, 0
    for line in lines:
        nodes_strings = line.split(" -> ")
        nodes = []
        for node in nodes_strings:
            x, y = node.split(",")
            # i change every y value to zero, since they are decreasing (0 is top and 9 is bottom)
            x, y = (int(x), -int(y))
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            nodes.append((int(x), int(y)))
        stone_lines.append(nodes)
    return stone_lines, min_x, max_x, min_y, max_y


def argmax(tuple_):
    return tuple_.index(max(tuple_))


def build_cave(cave, stone_lines):
    for stone_line in stone_lines:
        for i in range(len(stone_line)-1):
            node, next_node = stone_line[i], stone_line[i + 1]
            diff = node[0] - next_node[0], node[1] - next_node[1]
            diff_value = [d for d in diff if d != 0][0]
            index = diff.index(diff_value)
            if diff_value < 0:
                range_ = (diff_value, 1, 1)
            else:
                range_ = (0, diff_value + 1, 1)
            for i in range(*range_):
                if index == 0:
                    cave[next_node[0] + i, next_node[1]] = 1
                else:
                    cave[next_node[0], next_node[1] + i] = 1

    return cave