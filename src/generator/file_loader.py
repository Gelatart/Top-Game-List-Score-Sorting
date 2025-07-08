#INITIAL OUTPUT FROM CHATGPT

import os
import numpy as np
import math

from typing import List, Tuple, Iterator
from enum import Enum

from .config import check_for_src

class ListType(Enum):
    RANKED = 1
    UNRANKED = 2
    FORMER = 3

#def read_game_list(file_path: str, ranked: bool = True) -> Iterator[Tuple[str, int, int]]:
def read_game_list(file_path: str, type: ListType) -> Iterator[Tuple[str, int, int]]:
    """
    Read a ranked, unranked or former game list from a file.
    Returns (game_title, score, total_in_list)
    """
    # Replace the ranked bool with an enum? Because we could be ranked, unranked, or former
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("There appears to be no lines in this file")
        return

    #list_name = lines[0]
    #lines[0] should be for the number that helps determine the scoring system
    #name will be gotten from the filepath
    games = lines[1:]
    count = len(games)
    #scores = list(range(count, 0, -1)) if ranked else [count // 2] * count
    scores = list(range(count, 0, -1)) if type.value == 1 else math.floor(np.mean(list(range(count, 0, -1)))) if type.value == 2 else int(lines[0])
    #^put former scoring as option within this

    if(type.value == 1):
        for title, score in zip(games, scores):
            yield title, score, count
    else:
        for title in games:
            yield title, scores, count

def get_files_in_dir(directory: str, extension: str = ".txt") -> List[str]:
    """
    Return a list of all files with a specific extension in a directory.
    """
    full_path = check_for_src(directory)
    #also check if it is a file with os.path.isfile(f)? endswith makes this redundant?
    return [os.path.join(full_path, f) for f in os.listdir(full_path) if f.endswith(extension)]

#def read_completed_games(file_path: str) -> List[str]:
def read_attributed_games(file_path: str) -> List[str]:
    """
    Return a list of game titles from a .txt file.
    This will start with Completions.txt, but could encompass other custom files with custom fields.
    """
    with open(check_for_src(file_path), 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]