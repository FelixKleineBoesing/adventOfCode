from typing import Tuple, List

from shared import read_file_clean


def day_fifteen(file_path):
    print("Part 1")
    day_fifteen_part_one(file_path)
    print("Part 2")
    day_fifteen_part_two(file_path)


def day_fifteen_part_one(file_path):
    line = 2000000
    lines = read_file_clean(file_path)
    infos = parse_information(lines)
    beacons_sensors = set([info["sensor"] for info in infos] + [info["beacon"] for info in infos])
    calculate_distances(infos)
    x_r, y_r = get_ranges(infos)
    covered = set()
    for info in infos:
        x, y = info["sensor"]
        y_diff = abs(y - line)
        if y_diff > 0:
            i = 0
            covered.add((x, line))
            while True:
                i += 1
                left_diff = abs(manhattan_distance((x - i, line), info["sensor"]))
                left_point = (x - i, line)
                right_diff = abs(manhattan_distance((x + i, line), info["sensor"]))
                right_point = (x + i, line)
                not_stopping = False
                if left_diff <= info["distance"]:
                    covered.add(left_point)
                    not_stopping = not_stopping or True
                if right_diff <= info["distance"]:
                    covered.add(right_point)
                    not_stopping = not_stopping or True

                if not not_stopping:
                    break
    print("Length: {}".format(len(covered- beacons_sensors)))


def day_fifteen_part_two(file_path):
    lines = read_file_clean(file_path)
    infos = parse_information(lines)
    beacons_sensors = set([info["sensor"] for info in infos] + [info["beacon"] for info in infos])
    calculate_distances(infos)
    max_value = 4000000
    lines = {}

    for info in infos:
        sensor = info["sensor"]
        dist = info["distance"]
        top_rising = (True, sensor[1] - dist - 1 - sensor[0])
        top_descending = (False,  sensor[1] - dist - 1 + sensor[0])
        bottom_rising = (True, sensor[1] + dist + 1 - sensor[0])
        bottom_descending = (False, sensor[1] + dist + 1 + sensor[0])

        for line in [top_rising, top_descending, bottom_rising, bottom_descending]:
            """I'm counting the occurrences of each line"""
            if line in lines:
                lines[line] += 1
            else:
                lines[line] = 1

    rising_lines = []
    descending_lines = []

    for line, count in lines.items():
        if count > 1:
            if line[0]:
                descending_lines.append(line[1])
            else:
                rising_lines.append(line[1])

    points = []

    for rising_q in rising_lines:
        for descending_q in descending_lines:
            x = (rising_q - descending_q) // 2
            y = x + descending_q
            point = (x, y)
            points.append(point)

    value = None
    for point in points:
        if (
            (0 <= point[1] <= max_value)
            and (0 <= point[0] <= max_value)
            and point_is_not_in_sensor_range(point, infos)
        ):
            value = point[0] * 4000000 + point[1]
            print("Beacon Value: {}".format(value))
            break


def point_is_not_in_sensor_range(point: Tuple[int, int], infos: List[dict]) -> bool:
    for sensor in infos:
        if manhattan_distance(point, sensor["sensor"]) <= sensor["distance"]:
            return False
    return True


def parse_information(lines):
    infos = []
    for line in lines:
        sensor, beacon = line.split(":")
        info = {"sensor": split_loc(sensor), "beacon": split_loc(beacon)}
        infos.append(info)
    return infos


def split_loc(loc):
    x, y = loc.split(",")
    x = int(x.split("=")[1])
    y = int(y.split("=")[1])
    return x, y


def calculate_distances(infos):
    for info in infos:
        sensor = info["sensor"]
        beacon = info["beacon"]
        info["distance"] = manhattan_distance(sensor, beacon)


def manhattan_distance(p1, p2):
    x_dist = abs(p1[0] - p2[0])
    y_dist = abs(p1[1] - p2[1])
    return x_dist + y_dist


def get_ranges(infos):
    x_r = [0, 0]
    y_r = [0, 0]
    for info in infos:
        sensor = info["sensor"]
        beacon = info["beacon"]
        x_r[0] = min(x_r[0], sensor[0], beacon[0])
        x_r[1] = max(x_r[1], sensor[0], beacon[0])
        y_r[0] = min(y_r[0], sensor[1], beacon[1])
        y_r[1] = max(y_r[1], sensor[1], beacon[1])
    return x_r, y_r