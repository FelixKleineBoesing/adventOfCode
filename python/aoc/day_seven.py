from pathlib import Path

from shared import read_file_clean


def day_seven(file_path: Path):
    print("Part 1")
    day_seven_part_one(file_path)
    print("Part 2")
    day_seven_part_two(file_path)


def day_seven_part_two(file_path: Path):
    dir_hierarchy = calculate_total_sums(file_path)
    total_disk_size = 70000000
    size_unused_space = total_disk_size - dir_hierarchy["total_sum"]
    needed_space = 30000000 - size_unused_space
    dir_sizes = get_directories_over_size(dir_hierarchy, filter_size=needed_space)
    print("Size min dir: {}".format(min(dir_sizes)))


def day_seven_part_one(file_path: Path):
    dir_hierarchy = calculate_total_sums(file_path)
    filter_size = 100000
    dirs_under_size = sum(get_directories_under_size(dir_hierarchy, filter_size))

    print("Total sum: {} with directories under {} size".format(dirs_under_size, filter_size))


def calculate_total_sums(file_path):
    lines = read_file_clean(file_path)
    dir_hierarchy = {"subdirs": {}, "files": {}}
    dir_files = {}
    last_command = None
    current_dir = None
    for line in lines:
        if line[0] == "$":
            last_command, command_dir = parse_command(line)
            if last_command == "cd":
                if command_dir == "..":
                    current_dir = current_dir[:-1]
                else:
                    if current_dir is None:
                        current_dir = (command_dir,)
                        add_subdir(dir_hierarchy, tuple(), command_dir)
                    else:
                        add_subdir(dir_hierarchy, current_dir, command_dir)
                        current_dir = current_dir + (command_dir, )
                if current_dir not in dir_files:
                    dir_files[current_dir] = {}
        elif last_command == "ls":
            first_val, sec_val = line.split(" ")
            if first_val == "dir":
                add_subdir(dir_hierarchy, current_dir, sec_val)
            # if not dir, its a file
            else:
                add_file(dir_hierarchy, current_dir, sec_val, int(first_val))
                #dir_files[current_dir][sec_val] = int(first_val)

    sum_files = sum_directories(dir_files)
    _ = recursive_sum_directories(sum_files, dir_hierarchy)
    return dir_hierarchy


def get_directories_under_size(dir_hierarchy: dict, filter_size: int):
    dirs = []
    for dir, sub_dirs in dir_hierarchy["subdirs"].items():
        if len(sub_dirs) > 0:
            dirs.extend(get_directories_under_size(sub_dirs, filter_size))
    if dir_hierarchy["total_sum"] < filter_size:
        dirs.append(dir_hierarchy["total_sum"])
    return dirs


def get_directories_over_size(dir_hierarchy: dict, filter_size: int):
    dirs = []
    for dir, sub_dirs in dir_hierarchy["subdirs"].items():
        if len(sub_dirs) > 0:
            dirs.extend(get_directories_over_size(sub_dirs, filter_size))
    if dir_hierarchy["total_sum"] > filter_size:
        dirs.append(dir_hierarchy["total_sum"])
    return dirs


def sum_directories(dir_files: dict):
    sum_files = {k: sum(v.values()) for k, v in dir_files.items()}
    return sum_files


def recursive_sum_directories(sum_dirs: dict, dir_hierarchy: dict):
    sums = {}
    for dir, sub_dirs in dir_hierarchy["subdirs"].items():
        sums[dir] = recursive_sum_directories(sum_dirs, sub_dirs)
    total_sum = sum(sums.values()) + sum(dir_hierarchy["files"].values())
    dir_hierarchy["total_sum"] = total_sum
    return total_sum


def add_subdir(dir_hierarchy: dict, current_dir: tuple, new_dir: str):
    if len(current_dir) > 0:
        tmp_dir = dir_hierarchy
        for dir in current_dir:
            tmp_dir = tmp_dir["subdirs"][dir]
        if new_dir not in tmp_dir["subdirs"]:
            tmp_dir["subdirs"][new_dir] = {"subdirs": {}, "files": {}}
    else:
        dir_hierarchy["subdirs"][new_dir] = {"subdirs": {}, "files": {}}


def add_file(dir_hierarchy: dict, current_dir: tuple, new_file: str, file_size: int):
    if len(current_dir) > 0:
        tmp_dir = dir_hierarchy
        for dir in current_dir:
            tmp_dir = tmp_dir["subdirs"][dir]
        tmp_dir["files"][new_file] = file_size
    else:
        dir_hierarchy["files"][new_file] = file_size


def parse_command(command: str):
    if " cd " in command:
        dir = command.split(" ")[-1]
        return "cd", dir
    elif " ls" in command:
        return "ls", None
    else:
        print("Unknown command: {}".format(command))
