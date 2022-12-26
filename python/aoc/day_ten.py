from pathlib import Path

from python.aoc.shared import read_file_clean


def day_ten_part_two(file_path):
    cycle_values_during = get_cycle_values(file_path)
    activated = []
    for cycle, value in cycle_values_during.items():
        cycle -= 1
        if value-1 <= cycle % 40 <= value+1:
            activated.append("#")
        else:
            activated.append(" ")
    for i in range(0, 6):
        print("".join(activated[i*40:(i+1)*40]))


def day_ten(file_path: Path):
    print("Part 1")
    cycles = [20, 60, 100, 140, 180, 220]
    day_ten_part_one(file_path, cycles)
    print("Part 2")
    day_ten_part_two(file_path)
    
    
def day_ten_part_one(file_path: Path, cycles):
    cycle_values_during = get_cycle_values(file_path)
    signal_strength = [cyc * value for cyc, value in cycle_values_during.items() if cyc in cycles]
    print("Signal strength: {}".format(sum(signal_strength)))


def get_cycle_values(file_path):
    lines = read_file_clean(file_path)
    cycle_values = {0: 1}
    cycle = 0
    for line in lines:
        info = line.split(" ")
        if len(info) == 1:
            cycle += 1
            cycle_values[cycle] = cycle_values[cycle - 1]
        else:
            val = int(info[1])
            last_val = cycle_values[cycle]
            cycle_values.update({cycle + 1: last_val, cycle + 2: last_val + val})
            cycle += 2

    cycle_values_during = {k + 1: v for k, v in cycle_values.items()}
    return cycle_values_during

