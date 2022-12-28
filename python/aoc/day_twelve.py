from pathlib import Path
from string import ascii_lowercase
from shared import read_file_clean


hill_values = {a: i for i, a in enumerate(ascii_lowercase)}
hill_values["S"] = "S"
hill_values["E"] = "E"


def day_twelve(file_path: Path):
    print("Part 1")
    day_twelve_part_one(file_path)
    print("Part 2")
    day_twelve_part_two(file_path)


def day_twelve_part_one(file_path: Path):
    lines = read_file_clean(file_path)
    hill, start = parse_hill(lines)


class Hill:

    def __init__(self, data):
        self.data = data

    def __getitem__(self, item):
        return self.data[item[0]][item[1]]

    def shape(self):
        return len(self.data), len(self.data[0])


def find_destination(hill, start):
    current_node = start
    seen_nodes = set()
    len_x, len_y = hill.shape()
    queue = [[start]]
    while True:
        seen_nodes.add(current_node)
        current_value = hill[current_node]
        not_seen_nodes = [n for n in get_neighbor_nodes(current_node, len_x, len_y) if n not in seen_nodes]
        possible_moves = [n for n in not_seen_nodes if abs(hill[n] - current_value) <= 1]
        possible_values = [hill[n] for n in possible_moves]
        if "E" in possible_values:
            break

        if len(possible_moves) > 1:
            for move in possible_moves:
                queue.append(move)



def get_neighbor_nodes(current_node, len_x: int, len_y: int):
    n_nodes = []
    if current_node[0] > 0:
        n_nodes.append((current_node[0] - 1, current_node[1]))
    if current_node[0] < len_x - 1:
        n_nodes.append((current_node[0] + 1, current_node[1]))
    if current_node[1] > 0:
        n_nodes.append((current_node[0], current_node[1] - 1))
    if current_node[1] < len_y - 1:
        n_nodes.append((current_node[0], current_node[1] + 1))
    return n_nodes


def day_twelve_part_two(file_path: Path):
    lines = read_file_clean(file_path)


def parse_hill(lines):
    hill_data = []
    start = (0, 0)
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == "S":
                start = (x, y)
            hill_data.append((x, y, hill_values[char]))
    hill = Hill(hill_data)
    return hill, start