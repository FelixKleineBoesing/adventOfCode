#
from pathlib import Path


def read_file(file_path: Path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines