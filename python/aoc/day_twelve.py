import copy
from pathlib import Path
from string import ascii_lowercase
from shared import read_file_clean
from heapq import heappop, heappush
hill_values = {a: i for i, a in enumerate(ascii_lowercase)}
hill_values["S"] = -1
hill_values["E"] = hill_values["z"] + 1


def day_twelve(file_path: Path):
    print("Part 1")
    day_twelve_part_one(file_path)
    print("Part 2")
    day_twelve_part_two(file_path)


def day_twelve_part_one(file_path: Path):
    lines = read_file_clean(file_path)
    hill, start = parse_hill(lines)
    shortest_path = find_shortest_path(hill, start,target=hill_values["E"])
    print("Shortest path: {}".format(len(shortest_path) - 1))
    print_shortest_path(hill, shortest_path)


class Hill:

    def __init__(self, data):
        self.data = data

    def __getitem__(self, item):
        return self.data[item[0]][item[1]]

    def shape(self):
        return len(self.data), len(self.data[0])


def find_shortest_path(hill, start, target=hill_values["E"]):
    seen_nodes = set()
    len_x, len_y = hill.shape()
    queue = []
    heappush(queue, (0, (start, )))
    while len(queue) > 0:
        current_cost, current_path = heappop(queue)
        current_node = current_path[-1]
        current_value = hill[current_node]
        if current_value == target:
            return current_path
        if current_node not in seen_nodes:
            seen_nodes.add(current_node)
            neighbors = [n for n in get_neighbor_nodes(hill, current_node, len_x, len_y)]
            for move in neighbors:
                if hill[move] == hill[current_node]:
                    cost = current_cost + 1
                elif hill[move] < hill[current_node]:
                    cost = current_cost + 1
                else:
                    cost = current_cost + 1
                heappush(queue, (cost, current_path + (move, )))
    raise NoPathFound()


def find_multiple_starts_shortest_path(hill, starts, target=hill_values["E"]):
    shortest_paths = []
    shortest_paths_infos = {}
    for start in starts:
        seen_nodes = set()
        len_x, len_y = hill.shape()
        queue = []
        heappush(queue, (0, (start, )))
        while len(queue) > 0:
            current_cost, current_path = heappop(queue)
            current_node = current_path[-1]
            current_value = hill[current_node]
            if current_value == target:
                shortest_paths.append(current_path)
                for i, node in enumerate(current_path):
                    shortest_paths_infos[node] = {"path_id": len(shortest_paths) - 1, "path_pos": i}
            elif current_node in shortest_paths_infos:
                path_id = shortest_paths_infos[current_node]["path_id"]
                path_pos = shortest_paths_infos[current_node]["path_pos"]
                combined_path = current_path + shortest_paths[path_id][path_pos + 1:]
                shortest_paths.append(combined_path)
                for i, node in enumerate(current_path):
                    shortest_paths_infos[node] = {"path_id": len(shortest_paths) - 1, "path_pos": i}

            if current_node not in seen_nodes:
                seen_nodes.add(current_node)
                neighbors = [n for n in get_neighbor_nodes(hill, current_node, len_x, len_y)]
                for move in neighbors:
                    if hill[move] == hill[current_node]:
                        cost = current_cost + 1
                    elif hill[move] < hill[current_node]:
                        cost = current_cost + 1
                    else:
                        cost = current_cost + 1
                    heappush(queue, (cost, current_path + (move, )))

    return shortest_paths

def get_neighbor_nodes(hill, current_node, len_x: int, len_y: int):
    n_nodes = []
    if current_node[0] > 0:
        n_nodes.append((current_node[0] - 1, current_node[1]))
    if current_node[0] < len_x - 1:
        n_nodes.append((current_node[0] + 1, current_node[1]))
    if current_node[1] > 0:
        n_nodes.append((current_node[0], current_node[1] - 1))
    if current_node[1] < len_y - 1:
        n_nodes.append((current_node[0], current_node[1] + 1))
    return [n for n in n_nodes if hill[n] - hill[current_node] <= 1]


def day_twelve_part_two(file_path: Path):
    lines = read_file_clean(file_path)
    hill, start = parse_hill(lines)
    x, y = hill.shape()
    starts = []
    for row in range(x):
        for col in range(y):
            if hill[row, col] == 0:
                starts.append((row, col))
    shortest_paths = []
    shortest_paths = find_multiple_starts_shortest_path(hill, starts, target=hill_values["E"])
    # for start in starts:
    #     try:
    #         shortest_path = find_shortest_path(hill, start, target=hill_values["E"])
    #         shortest_paths.append(shortest_path)
    #     except NoPathFound:
    #         pass
    len_shortest_paths = [len(p) for p in shortest_paths]
    min_steps = min(len_shortest_paths)
    print("Shortest path: {}".format(min_steps))


def parse_hill(lines):
    hill_data = []
    start = (0, 0)
    for x, line in enumerate(lines):
        row = []
        for y, char in enumerate(line):
            if char == "S":
                start = (x, y)
            row.append(hill_values[char])
        hill_data.append(row)
    hill = Hill(hill_data)
    return hill, start


class NoPathFound(Exception):
    pass


def print_shortest_path(hill, shortest_path):
    hill_data = copy.copy(hill.data)
    symbols = []
    for i in range(len(shortest_path) - 1):
        node, next_node = shortest_path[i], shortest_path[i + 1]
        if node[0] == next_node[0]:
            if node[1] < next_node[1]:
                symbols.append(">")
            else:
                symbols.append("<")
        else:
            if node[0] < next_node[0]:
                symbols.append("v")
            else:
                symbols.append("^")
    symbols.append("E")
    for sym, node in zip(symbols, shortest_path):
        hill_data[node[0]][node[1]] = sym
    for row in hill_data:
        print("".join([str(c) for c in row]))