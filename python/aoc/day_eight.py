from pathlib import Path

from shared import read_file_clean


def day_eight(file_path: Path):
    print("Part 1")
    day_eight_part_one(file_path)
    print("Part 2")
    day_eight_part_two(file_path)


def day_eight_part_two(file_path: Path):
    lines = read_file_clean(file_path)
    tree_array, (rows, cols) = get_tree_array(lines)
    scenic_scores = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            scenic_scores[i][j] = get_scenic_score(tree_array, rows, cols, i, j)
    print("Max scenic score: {}".format(max([max(row) for row in scenic_scores])))


def get_scenic_score(tree_array, rows, cols, row, col):
    up, down, left, right = 1, 1, 1, 1
    for i in range(row + 1, rows):
        if tree_array[i][col] >= tree_array[row][col] or i == rows - 1:
            down = i - row
            break
    for i in range(row - 1, -1, -1):
        if tree_array[i][col] >= tree_array[row][col] or i == 0:
            up = row - i
            break
    for i in range(col + 1, cols):
        if tree_array[row][i] >= tree_array[row][col] or i == cols - 1:
            right = i - col
            break
    for i in range(col - 1, -1, -1):
        if tree_array[row][i] >= tree_array[row][col] or i == 0:
            left = col - i
            break
    return right * left * down * up


def day_eight_part_one(file_path: Path):
    lines = read_file_clean(file_path)
    tree_array, (rows, cols) = get_tree_array(lines)
    visibility = [[0 for _ in range(cols)] for _ in range(rows)]
    update_visibility_array_rowwise(visibility, tree_array, rows, cols)
    update_visibility_array_rowwise(visibility, tree_array, rows, cols, -1)
    update_visibility_array_colunwise(visibility, tree_array, rows, cols)
    update_visibility_array_colunwise(visibility, tree_array, rows, cols, -1)
    print("NUmber visible trees: {}".format(sum([sum(row) for row in visibility])))


def update_visibility_array_rowwise(visibility, tree_array, rows, cols, direction=1):
    for i in range(rows):
        last_height = -1
        range_ = get_range(cols, direction)
        for j in range(*range_):
            if tree_array[i][j] > last_height:
                visibility[i][j] = 1
                last_height = tree_array[i][j]


def update_visibility_array_colunwise(visibility, tree_array, rows, cols, direction=1):
    for j in range(cols):
        last_height = -1
        range_ = get_range(rows, direction)
        for i in range(*range_):
            if tree_array[i][j] > last_height:
                visibility[i][j] = 1
                last_height = tree_array[i][j]


def get_range(number, direction=1):
    if direction == 1:
        range_ = (0, number, 1)
    else:
        range_ = (number-1, -1, -1)
    return range_


def get_tree_array(lines):
    tree_array = []
    for line in lines:
        tree_array.append([int(char) for char in line])
    return tree_array, (len(lines), len(lines[0]))