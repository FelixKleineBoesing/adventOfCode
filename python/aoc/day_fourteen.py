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
    for y in range(cave.max_y):
        for x in range(cave.max_x):
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
    cave = Cave(max_x + 1 - min_x , max_y + 1 - min_y)
    cave = build_cave(cave, standardized_stone_lines)
    space_full = False
    number_sands = 0
    while not space_full:
        particle_settled = False
        current_pos = sand_entry
        while not particle_settled:
            particle_settled, current_pos = move_particle(current_pos, (0, 1))

        if current_pos[0] <= 0 or 0 > current_pos[1] > cave.max_y:
            space_full = True
        else:
            cave[current_pos] = 2
        number_sands += 1
        if current_pos == sand_entry:
            space_full = True

    print_cave(cave)
    return cave, number_sands


def check_if_move_possible(cave, current_pos):
    if place_free(cave, current_pos, (-1, 0)):
        new_pos = move_particle(current_pos, (1, 0))
        return True, new_pos
    elif place_free(cave, current_pos, (-1, -1)):
        new_pos = move_particle(current_pos, (0, -1))
        return True, new_pos
    elif place_free(cave, current_pos, (-1, 1)):
        new_pos = move_particle(current_pos, (0, 1))
        return True, new_pos
    return False, current_pos


def place_free(cave, current_pos, direction):
    if cave[current_pos[0] + direction[0], current_pos[1] + direction[1]] == 0:
        return True
    return False


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
        self.grid = [[0 for _ in range(len_x)] for _ in range(len_y)]

    def __getitem__(self, item):
        return self.grid[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.grid[key[0]][key[1]] = value

    def shape(self):
        return self.len_x, self.len_y


def day_fourteen_part_two(file_path):
    pass


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
            x, y = (int(x), int(y))
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
            diff_value = max(diff)
            index = argmax(diff)
            for i in range(diff_value + 1):
                if index == 0:
                    cave[next_node[0] + i, node[1]] = 1
                else:
                    cave[node[0], next_node[1] + i] = 1

    return cave