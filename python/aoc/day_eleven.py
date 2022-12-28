import copy
from pathlib import Path

from python.aoc.shared import read_file_clean


def day_eleven(file_path: Path):
    print("Part 1")
    day_eleven_part_one(file_path)
    print("Part 2")
    day_eleven_part_two(file_path)


def day_eleven_part_two(file_path: Path):
    lines = read_file_clean(file_path)
    number_rounds = 10000
    monkeys = parse_monkeys(lines)

    modulu_all = 1
    for monkey_id in monkeys.keys():
        monkey = monkeys[monkey_id]
        modulu_all *= int(monkey["divisor"])

    def worry_level_func(a):
        return a % modulu_all

    number_items_seen = {m: 0 for m in monkeys}
    for i in range(number_rounds):
        for monkey_id in monkeys.keys():
            tmp_seen_items = simulate_monkey(monkey_id, monkeys, worry_level_func=worry_level_func)
            number_items_seen[monkey_id] += tmp_seen_items

    most_active_monkeys = sorted(number_items_seen.values(), key=lambda x: x, reverse=True)
    print("This is the monkey business: {}".format(most_active_monkeys[0] * most_active_monkeys[1]))


def day_eleven_part_one(file_path: Path):
    lines = read_file_clean(file_path)
    number_rounds = 20
    monkeys = parse_monkeys(lines)
    number_items_seen = {m: 0 for m in monkeys}

    def worry_level_func(a):
        return a / 3

    for i in range(number_rounds):
        for monkey_id in monkeys.keys():
            tmp_seen_items = simulate_monkey(monkey_id, monkeys, worry_level_func=worry_level_func)
            number_items_seen[monkey_id] += tmp_seen_items

    most_active_monkeys = sorted(number_items_seen.values(), key=lambda x: x, reverse=True)
    print("This is the monkey business: {}".format(most_active_monkeys[0] * most_active_monkeys[1]))


def multiply(*args):
    result = 1
    for arg in args:
        result *= arg
    return result


def simulate_monkey(monkey_id, monkeys, worry_level_func):
    monkey = monkeys[monkey_id]
    number_seen_items = len(monkey["items"])
    original_items = copy.copy(monkey["items"])
    for i, item in enumerate(original_items):
        worry_level = monkey["op_func"](item)
        worry_level = worry_level_func(worry_level)
        if monkey["test_func"](worry_level):
            monkeys[monkey["if_true"]]["items"].append(worry_level)
        else:
            monkeys[monkey["if_false"]]["items"].append(worry_level)
    monkey["items"] = []
    return number_seen_items


def parse_monkeys(lines):
    monkeys = {}
    monkey_id, items, op_func, test_func, if_true, if_false = None, None, None, None, None, None
    for i, line in enumerate(lines):
        if "Monkey" in line:
            _, monkey_id = line.split(" ")
            monkey_id = int(monkey_id.replace(":", " "))
        elif "Starting items" in line:
            _, items = line.split(": ")
            items = [int(i) for i in items.split(", ")]
        elif "Operation" in line:
            _, operation = line.split("= ")
            op_val1, op, op_val2 = operation.split(" ")
            op_func = get_operation_func(op_val1, op, op_val2)
        elif "Test" in line:
            _, divisor = line.split("divisible by ")
            test_func = get_test_func(int(divisor))
        elif "If true" in line:
            _, if_true = line.split("to monkey ")
            if_true = int(if_true)
        elif "If false" in line:
            _, if_false = line.split("to monkey ")
            if_false = int(if_false)
        elif len(line) == 0 or i == len(lines) - 1:
            monkeys[monkey_id] = {
                "items": items,
                "op_func": op_func,
                "test_func": test_func,
                "if_true": if_true,
                "if_false": if_false,
                "divisor": divisor
            }
    monkeys[monkey_id] = {
        "items": items,
        "op_func": op_func,
        "test_func": test_func,
        "if_true": if_true,
        "if_false": if_false,
        "divisor": divisor
    }
    return monkeys


def get_test_func(divisor):
    def test_func(val):
        return val % divisor == 0
    return test_func


def get_operation_func(op_val1, op, op_val2):
    def operation_func(old):
        if "old" in op_val1:
            val_1 = old
        else:
            val_1 = int(op_val1)
        if "old" in op_val2:
            val_2 = old
        else:
            val_2 = int(op_val2)
        if "+" in op:
            return val_1 + val_2
        elif "-" in op:
            return val_1 - val_2
        elif "*" in op:
            return val_1 * val_2
        elif "/" in op:
            return val_1 / val_2
        else:
            raise ValueError("Unknown operation")
    return operation_func