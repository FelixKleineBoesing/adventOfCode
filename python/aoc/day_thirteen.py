from shared import read_file_clean
import json


def day_thirteen(file_path):
    print("Part 1")
    day_thirteen_part_one(file_path)
    print("Part 2")
    day_thirteen_part_two(file_path)


def day_thirteen_part_one(file_path):
    lines = read_file_clean(file_path)
    pairs = parse_pairs(lines)
    ordered = [correct_order(pair) for pair in pairs]
    indices = [i for i in range(1, len(ordered) + 1)]
    print("Sum of indices: {}".format(sum([i for i, o in zip(indices, ordered) if o])))


def day_thirteen_part_two(file_path):
    lines = read_file_clean(file_path)
    lines = [json.loads(line) for line in lines if line != ""]
    lines.extend([[[2]], [[6]]])
    sorted_lines = []
    all_sorted = False
    while not all_sorted:
        for i in range(len(lines) - 1):
            l0, l1 = lines[i], lines[i + 1]
            if correct_order((l0, l1)):
                continue
            else:
                lines[i], lines[i + 1] = l1, l0
        all_sorted = True
        for i in range(len(lines) - 1):
            l0, l1 = lines[i], lines[i + 1]
            if correct_order((l0, l1)):
                continue
            else:
                all_sorted = False
                break

    dec_1, dec_2 = None, None
    for i, line in enumerate(lines):
        if line == [[2]]:
            dec_1 = i + 1
        if line == [[6]]:
            dec_2 = i + 1


    print("Dec 1: {}, Dec 2: {}, Product: {}".format(dec_1, dec_2, dec_1*dec_2))


def parse_pairs(lines):
    pairs = []
    pair = []
    for i, line in enumerate(lines):
        if i == len(lines) - 1:
            pair.append(json.loads(line))
            pairs.append(pair)
            break
        if line == "":
            pairs.append(pair)
            pair = []
        else:
            pair.append(json.loads(line))

    return pairs


def correct_order(pair):
    l, r = pair
    len_l, len_r = len(l), len(r)
    for i in range(max(len_l, len_r)):
        # if left list runs out first
        if i >= len_l:
            return True
        # if right list runs out first
        if i >= len_r:
            return False

        # if one element is a list
        if isinstance(l[i], list) or isinstance(r[i], list):
            if not isinstance(l[i], list):
                l_list = [l[i]]
            else:
                l_list = l[i]
            if not isinstance(r[i], list):
                r_list = [r[i]]
            else:
                r_list = r[i]
            ordered = correct_order((l_list, r_list))
            if ordered is None:
                continue
            else:
                return ordered

        elif isinstance(l[i], int) and isinstance(r[i], int):
            l_int, r_int = int(l[i]), int(r[i])
            if l_int < r_int:
                return True
            elif l_int > r_int:
                return False
            else:
                continue
        else:
            raise ValueError("Unknown type: {} and {}".format(type(l[i]), type(r[i])))
