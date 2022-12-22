from pathlib import Path


def read_file(file_path: Path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines


def read_file_clean(file_path: Path):
    with open(file_path, "r") as f:
        lines = [
            line.replace("\n", "") for line in f.readlines()
        ]
        return lines