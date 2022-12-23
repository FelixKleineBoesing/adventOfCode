from pathlib import Path

from python.aoc.shared import read_file_clean


def day_five(file_path: Path):
    lines = read_file_clean(file_path)
    stack_lines = []
    move_lines = []
    stack_positions = None
    for i, line in enumerate(lines):
        # matches the starting stacks
        if "[" in line:
            stack_lines.append(line)
        elif "move" in line:
            move_lines.append(line)
        elif line != "":
            stack_positions = line

    stacks = get_stacks(stack_positions, stack_lines)
    moves = parse_moves(move_lines)
    for move in moves:
        from_, to, n = move
        for i in range(n):
            stacks[to].append(stacks[from_].pop())

    top_level_items = [s.pop() for s in stacks.values()]
    print("Top level items: {}".format("".join(top_level_items)))


def get_stacks(stack_positions, stack_lines):
    stack_positions = {int(i): index for index, i in enumerate(stack_positions) if i != " "}
    stacks = {i: [] for i in stack_positions}
    for line in reversed(stack_lines):
        for i, pos in stack_positions.items():
            if pos < len(line):
                if line[pos] != " ":
                    stacks[i].append(line[pos])
    return stacks


def parse_moves(move_lines):
    """
    Parses the move lines into a list of tuples (from, to, number_items
    :param move_lines:
    :return:
    """
    moves = []
    for line in move_lines:
        _, n, _, from_, _, to = line.split()
        moves.append((int(from_), int(to), int(n)))
    return moves