import math
from pathlib import Path
from typing import List, Tuple, Set
from shared import read_file_clean
from heapq import heappush, heappop
import re
import time
from itertools import combinations
from collections import deque, defaultdict


def day_sixteen(file_path):
    print("Part 1")
    day_sixteen_part_one(file_path)
    print("Part 2")
    day_sixteen_part_two(file_path)


def solve(valves, n_agents, time: int):
    queue = []
    start = "AA"
    initial_state = State(
        rooms=((start, 0), ) * n_agents,
        valves=set(n for n in valves.values() if n.flow_rate > 0),
        flow=0,
        total=0,
        time=time
    )
    distances = calculate_distances(valves)
    heappush(queue, (0, initial_state))
    visited = set()
    max_value = 0
    while len(queue) > 0:
        cost_estim, current_state = heappop(queue)
        cost_estim = -cost_estim
        if current_state in visited:
            continue
        visited.add(current_state)
        potential = cost_estim
        for valve in current_state.valves:
            potential += max(
                (
                    valves[valve.id].flow_rate * (current_state.time - distances[room, valve.id] - age - 1)
                    for room, age in current_state.rooms
                    if distances[room, valve.id] - age in range(current_state.time)
                ), default=0
            )

        if cost_estim > max_value:
            max_value = cost_estim
        if potential < max_value:
            continue

        moves_by_time = defaultdict(lambda: defaultdict(list))
        for valve in current_state.valves:
            for i, (room, age) in enumerate(current_state.rooms):
                delta = distances[room, valve.id] - age
                if delta in range(current_state.time):
                    moves_by_time[delta][i].append(valve)
        if not moves_by_time:
            continue

        for delta, moves_by_agent in moves_by_time.items():
            indices = [None] * n_agents
            while True:
                for i, index in enumerate(indices):
                    index = 0 if index is None else index + 1
                    if index < len(moves_by_agent[i]):
                        indices[i] = index
                        break
                    indices[i] = None
                else:
                    break
                valves_curr = [
                    (i, moves_by_agent[i][index])
                    for i, index in enumerate(indices)
                    if index is not None
                ]
                if len(valves_curr) != len(set(valve for _, valve in valves_curr)):
                    continue
                new_rooms = [(room, age + delta + 1) for room, age in current_state.rooms]
                for i, valve in valves_curr:
                    new_rooms[i] = valve, 0
                rate = sum(valves[valve.id].flow_rate for _, valve in valves_curr)
                new_state = State(
                    rooms=tuple(sorted(new_rooms)),
                    valves=current_state.valves - set(valve for _, valve in valves_curr),
                    flow=current_state.flow + rate,
                    total=current_state.total + current_state.flow * (delta + 1),
                    time=current_state.time - delta - 1,
                )
                heappush(queue, (-cost_estim - rate * new_state.time, new_state))

    return max_value


class State:
    def __init__(self, rooms: Tuple[Tuple[int, str]], valves: Set[str], flow: int, total: int, time: int):
        self.rooms = rooms
        self.valves = valves
        self.flow = flow
        self.total = total
        self.time = time


def calculate_distances(graph: dict):
    nodes, distances = set(), defaultdict(lambda: math.inf)
    for source, valve in graph.items():
        neighbors = valve.leading_to
        nodes.add(source)
        distances[source, source] = 0
        for neighbor in neighbors:
            nodes.add(neighbor)
            distances[neighbor, neighbor] = 0
            distances[source, neighbor] = 1

    for mid in nodes:
        for source in nodes:
            for target in nodes:
                distances[source, target] = min(distances[source, target], distances[source, mid] + distances[mid, target])
    return distances


def parse_information(lines):
    valves = {}
    for line in lines:
        source, target = line.split(";")
        source_valve, flow = source.split(" ")[1], int(source.split("flow rate=")[-1])
        target_valves = parse_target_valves(target)
        valves[source_valve] = Valve(source_valve, flow, target_valves)
    return valves


def parse_target_valves(target_string):
    if "tunnel leads to valve " in target_string:
        return [target_string.split("tunnel leads to valve ")[-1]]
    elif "tunnels lead to valves " in target_string:
        return list(target_string.split("tunnels lead to valves ")[-1].split(", "))
    else:
        raise Exception("Unknown target string: {}".format(target_string))


class Valve:

    def __init__(self, id_: str, flow_rate: int, leading_to: List[str]):
        self.id = id_
        self.flow_rate = flow_rate
        self.leading_to = leading_to


def day_sixteen_part_one(file_path: Path):
    start_time = time.time()

    valves = {}
    flow_rates = {}
    lines = read_file_clean(file_path)
    for line in lines:
        tokens = line.strip().split(' ')

        valve = tokens[1]
        flow_rate = int(re.findall(r'\d+', tokens[4])[0])
        neighbors = set([node for node in ''.join(tokens[9:]).split(',')])

        valves[valve] = neighbors
        flow_rates[valve] = flow_rate

    # memoization helper
    def memoize(fn):
        memo = {}

        def memozied(*args):
            if args in memo:
                return memo[args]
            else:
                result = fn(*args)
                memo[args] = result
                return result

        return memozied

    # BFS the valve graph to return the shortest path length
    # betweent two valves
    @memoize
    def shorest_path_length(start, end):
        q = deque([[start]])
        visited = set()

        if start == end:
            return len([start]) - 1

        while len(q) > 0:
            path = q.popleft()
            node = path[-1]

            if node not in visited:
                neighbors = valves[node]

                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    q.append(new_path)

                    if neighbor == end:
                        return len(new_path) - 1

                visited.add(node)

        return None

    # DFS of every possible order we could open the valves in
    #
    # cut down on the search space by eliminating valves with flow rate of 0
    # we will never stop at those valves to open them
    def should_try_to_open_valve(valve):
        return flow_rates[valve] != 0

    valves_to_open = list(filter(should_try_to_open_valve, valves.keys()))

    start_location = 'AA'
    time_limit = 30
    maximum_pressure = 0

    # a stack of our current branches - [path], minutes_elapsed, { valve: <minute opened> }
    s = [[[start_location], 0, {}]]

    while len(s):
        path, minutes_elapsed, open_valves = s.pop()
        current_valve = path[-1]

        # if we've opened all the valves, calculate the maximum pressure
        # if we've run out of time, calculate the pressure and abandon this "branch"
        if minutes_elapsed >= time_limit or len(path) == len(valves_to_open) + 1:
            pressure_released = 0

            for valve, minute_opened in open_valves.items():
                minutes_opened = max(time_limit - minute_opened, 0)
                pressure_released += flow_rates[valve] * minutes_opened

            maximum_pressure = max(maximum_pressure, pressure_released)
        else:
            for next_valve in valves_to_open:
                if next_valve not in open_valves.keys():
                    # each edge in the graph takes 1 minute to cross
                    # so our travel time to the next valve we're trying to open
                    # is the length of the shortest path
                    # taking anything longer than the shortest possible path
                    # would obviously be sub-optimal
                    travel_time = shorest_path_length(current_valve, next_valve)

                    # plus we'll stop at the valve for an additional minute to open it
                    time_to_open_valve = 1

                    new_minutes_elapsed = minutes_elapsed + travel_time + time_to_open_valve

                    new_open_valves = open_valves.copy()
                    new_open_valves[next_valve] = new_minutes_elapsed

                    new_path = list(path)
                    new_path.append(next_valve)

                    s.append([new_path, new_minutes_elapsed, new_open_valves])

    print(maximum_pressure)
    print("%s seconds" % (time.time() - start_time))


def day_sixteen_part_two(file_path: Path):
    start_time = time.time()

    valves = {}
    flow_rates = {}
    lines = read_file_clean(file_path)
    for line in lines:
        tokens = line.strip().split(' ')

        valve = tokens[1]
        flow_rate = int(re.findall(r'\d+', tokens[4])[0])
        neighbors = set([node for node in ''.join(tokens[9:]).split(',')])

        valves[valve] = neighbors
        flow_rates[valve] = flow_rate


    # memoization helper
    def memoize(fn):
        memo = {}

        def memozied(*args):
            if args in memo:
                return memo[args]
            else:
                result = fn(*args)
                memo[args] = result
                return result

        return memozied


    # yield all possible partitions of a list into k subsets
    def subsets_k(collection, k): yield from partition_k(collection, k, k)


    def partition_k(collection, min, k):
        if len(collection) == 1:
            yield [collection]
            return

        first = collection[0]
        for smaller in partition_k(collection[1:], min - 1, k):
            if len(smaller) > k: continue

            if len(smaller) >= min:
                for n, subset in enumerate(smaller):
                    yield smaller[:n] + [[first] + subset] + smaller[n + 1:]

            if len(smaller) < k: yield [[first]] + smaller


    # BFS the valve graph to return the shortest path length
    # betweent two valves
    @memoize
    def shorest_path_length(start, end):
        q = deque([[start]])
        visited = set()

        if start == end:
            return len([start]) - 1

        while len(q) > 0:
            path = q.popleft()
            node = path[-1]

            if node not in visited:
                neighbors = valves[node]

                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    q.append(new_path)

                    if neighbor == end:
                        return len(new_path) - 1

                visited.add(node)

        return None


    @memoize
    def valve_choose_r(serialized_valves, r):
        return combinations(serialized_valves.split(','), r)


    # DFS of every possible order we could open the valves in
    #
    # cut down on the search space by eliminating valves with flow rate of 0
    # we will never stop at those valves to open them
    def should_try_to_open_valve(valve):
        return flow_rates[valve] != 0


    valves_to_open = list(filter(should_try_to_open_valve, valves.keys()))

    start_location = 'AA'
    time_limit = 26

    maximum_pressure = 0
    pressure_by_path = defaultdict(lambda: 0)

    # a stack of our current branches - [path], minutes_elapsed, { valve: <minute opened> }
    s = [[[start_location], 0, {}]]

    while len(s):
        path, minutes_elapsed, open_valves = s.pop()
        current_valve = path[-1]

        pressure_released = 0

        for valve, minute_opened in open_valves.items():
            minutes_opened = max(time_limit - minute_opened, 0)
            pressure_released += flow_rates[valve] * minutes_opened

        maximum_pressure = max(maximum_pressure, pressure_released)

        # sort the valves lexically and use it as a key
        # so we can determine which ordering of these valves
        # nets the greatest pressure released
        path_key = ','.join(sorted(path))
        pressure_by_path[path_key] = max(pressure_by_path[path_key], pressure_released)

        # if we've run out of time, abandon this "branch"
        if minutes_elapsed >= time_limit or len(path) == len(valves_to_open) + 1:
            # because we may not have opened all of the valves, all other possible ways
            # of adding the remaining valves need to be added to the lookup
            # but the pressure will be the same
            remaining_valves = [valve for valve in valves_to_open if valve not in path]

            for r in range(1, len(remaining_valves)):
                for combination in valve_choose_r(','.join(sorted(remaining_valves)), r):
                    key = ','.join(sorted(path + list(combination)))
                    pressure_by_path[key] = max(pressure_by_path[key], pressure_released)

            continue
        else:
            for next_valve in valves_to_open:
                if next_valve not in open_valves.keys():
                    # each edge in the graph takes 1 minute to cross
                    # so our travel time to the next valve we're trying to open
                    # is the length of the shortest path
                    # taking anything longer than the shortest possible path
                    # would obviously be sub-optimal
                    travel_time = shorest_path_length(current_valve, next_valve)

                    # plus we'll stop at the valve for an additional minute to open it
                    time_to_open_valve = 1

                    new_minutes_elapsed = minutes_elapsed + travel_time + time_to_open_valve

                    new_open_valves = open_valves.copy()
                    new_open_valves[next_valve] = new_minutes_elapsed

                    new_path = list(path)
                    new_path.append(next_valve)

                    s.append([new_path, new_minutes_elapsed, new_open_valves])

    # check if we can increase the pressure by training the elephants
    #
    # generate all of the possible ways to split the valves
    # between me and the elephants, it doesn't matter who takes which subset
    #
    # https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind
    for i, subsets in enumerate(subsets_k(valves_to_open, 2)):
        my_pressure = pressure_by_path[','.join(sorted(['AA'] + subsets[0]))]
        elephant_pressure = pressure_by_path[','.join(sorted(['AA'] + subsets[1]))]

        maximum_pressure = max(maximum_pressure, my_pressure + elephant_pressure)

    print(maximum_pressure)
