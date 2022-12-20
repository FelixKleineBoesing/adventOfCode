from pathlib import Path
from typing import List

from python.aoc.shared import read_file

SIGN_POINTS = {"R": 1, "P": 2, "S": 3}
MAPPING_SIGNS = {"A": "R", "B": "P", "C": "S", "X": "R", "Y": "P", "Z": "S"}
OUTCOME_POINTS = {"W": 6, "L": 0, "D": 3}

OUTCOME_MAPPING = {"X": "L", "Y": "D", "Z": "W"}
WIN_MAPPING = {"P": "R", "S": "P", "R": "S"}
LOSS_MAPPING = {v: k for k, v in WIN_MAPPING.items()}


def day_two(file_path: Path):
    lines = read_file(file_path)

    # first part
    outcomes = get_match_outcomes_first_part(lines)
    sum_points_first = sum(outcomes)
    print("Outcomes First Part: {}".format(sum_points_first))

    # second part
    outcomes = get_match_outcomes_second_part(lines)
    sum_points_second = sum(outcomes)
    print("Outcomes Second Part: {}".format(sum_points_second))
    return sum_points_first, sum_points_second


def get_match_outcomes_second_part(lines: List[str]):
    matches = []
    for line in lines:
        line = line.replace("\n", "")
        opp, outcome = line.split(" ")
        opp, = get_signs(opp)
        outcome = OUTCOME_MAPPING[outcome]
        own = get_outcome_sign(opp, outcome)
        points = get_points(outcome, own)
        matches.append(points)
    return matches


def get_match_outcomes_first_part(lines: List[str]):
    matches = []
    for line in lines:
        line = line.replace("\n", "")
        opp, own = get_signs(*line.split(" "))
        outcome = get_outcome(opp, own)
        points = get_points(outcome, own)
        matches.append(points)
    return matches


def get_outcome_sign(opp: str, outcome: str):
    if outcome == "D":
        return opp
    elif outcome == "W":
        return LOSS_MAPPING[opp]
    else:
        return WIN_MAPPING[opp]


def get_outcome(opp: str, own: str):
    win_sign = WIN_MAPPING[own]
    if opp == own:
        return "D"
    elif win_sign == opp:
        return "W"
    else:
        return "L"


def get_points(outcome: str, sign: str):
    return OUTCOME_POINTS[outcome] + SIGN_POINTS[sign]


def get_signs(*arg):
    return [MAPPING_SIGNS[sign] for sign in arg]
