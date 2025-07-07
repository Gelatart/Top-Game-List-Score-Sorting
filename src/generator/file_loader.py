#INITIAL OUTPUT FROM CHATGPT

import os
import numpy as np

from typing import List, Tuple, Iterator
from .config import check_for_src
from .generator import ListType

#def read_game_list(file_path: str, ranked: bool = True) -> Iterator[Tuple[str, int, int]]:
def read_game_list(file_path: str, type: ListType) -> Iterator[Tuple[str, int, int]]:
    """
    Read a ranked or unranked game list from a file.
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
    scores = list(range(count, 0, -1)) if type.value == 1 else math.floor(np.mean(list(range(count, 0, -1)))) if type.value == 2 else lines[0]
    #^put former scoring as option within this

    for title, score in zip(games, scores):
        yield title, score, count

    """
            file1 = open(f, 'r', encoding="utf-8")
            ranked_file_count += 1
            starting_line = file1.readline()
            Lines = file1.readlines()
            #count = int(starting_line)
            count = len(Lines)
            original_count = count
            # Strips the newline character
            for line in Lines:
                stripped_line = line.strip()
                line = stripped_line
                if stripped_line in game_DB:
                    game_DB[line].ranked_score += count
                    game_DB[line].list_count += 1
                    game_DB[line].lists_referencing.append(f)
                    game_DB[line].total_count += original_count
                else:
                    newObj = GameObject(count, f, original_count)
                    game_DB[line] = newObj
                #searchObj = game_DB.get(newObj, 0) + 1
                #game_DB[line].list_count = game_DB.get(newObj, 0) + 1
                print(f"Score of {count}: {line.strip()}")
                count -= 1
            games_lists.append(filename)
    """

def get_files_in_dir(directory: str, extension: str = ".txt") -> List[str]:
    """
    Return a list of all files with a specific extension in a directory.
    """
    full_path = check_for_src(directory)
    #also check if it is a file with os.path.isfile(f)?
    return [os.path.join(full_path, f) for f in os.listdir(full_path) if f.endswith(extension)]

def read_completed_games(file_path: str) -> List[str]:
    """
    Return a list of completed game titles from a .txt file.
    """
    with open(check_for_src(file_path), 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

"""
PART OF GENERATOR LOOP:


"""

"""
ORIGINAL FUNCTIONALITY FOR COMPARISON:
    games_lists = []
    ranked_file_count = 0
    unranked_file_count = 0
    former_file_count = 0
    "Loop of getting the database information"
    #RANKED DIRECTORY
    directory = check_for_src(r'GameLists\Ranked')
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # Using readlines()
            file1 = open(f, 'r', encoding="utf-8")
            ranked_file_count += 1
            starting_line = file1.readline()
            Lines = file1.readlines()
            #count = int(starting_line)
            count = len(Lines)
            original_count = count
            # Strips the newline character
            for line in Lines:
                stripped_line = line.strip()
                line = stripped_line
                if stripped_line in game_DB:
                    game_DB[line].ranked_score += count
                    game_DB[line].list_count += 1
                    game_DB[line].lists_referencing.append(f)
                    game_DB[line].total_count += original_count
                else:
                    newObj = GameObject(count, f, original_count)
                    game_DB[line] = newObj
                #searchObj = game_DB.get(newObj, 0) + 1
                #game_DB[line].list_count = game_DB.get(newObj, 0) + 1
                print(f"Score of {count}: {line.strip()}")
                count -= 1
            games_lists.append(filename)

    directory = check_for_src(r'GameLists\Unranked')

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            #print(f)
            # Using readlines()
            file1 = open(f, 'r', encoding="utf-8")
            unranked_file_count += 1
            starting_line = file1.readline()
            Lines = file1.readlines()
            float_count = float(starting_line)
            count = math.floor(float_count)
            count = len(Lines)
            print(count)
            original_count = count
            #do a sum of all numbers in that count
            count = original_count * (original_count + 1) // 2
            #divide the factorial by the original count
            count //= original_count
            print(count)
            print(f)
            #input('Wait to review\n')
            # Strips the newline character
            for line in Lines:
                stripped_line = line.strip()
                line = stripped_line
                if stripped_line in game_DB:
                    game_DB[line].ranked_score += count
                    game_DB[line].list_count += 1
                    game_DB[line].lists_referencing.append(f)
                    game_DB[line].total_count += original_count
                else:
                    newObj = GameObject(count, f, original_count)
                    game_DB[line] = newObj
                #searchObj = game_DB.get(newObj, 0) + 1
                #game_DB[line].list_count = game_DB.get(newObj, 0) + 1
                print(f"Score of {count}: {line.strip()}")
                #count -= 1
            games_lists.append(filename)

    directory = check_for_src(r'GameLists\Former')
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # Using readlines()
            # file1 = open(f, 'r')
            file1 = open(f, 'r', encoding="utf-8")
            former_file_count += 1
            starting_line = file1.readline()
            Lines = file1.readlines()
            #count = 1
            count = int(starting_line)
            original_count = count
            #^find out how to read the line amount ahead of time
            #original_count = len(Lines)
            print(original_count)
            # Strips the newline character
            for line in Lines:
                stripped_line = line.strip()
                line = stripped_line
                if stripped_line in game_DB:
                    game_DB[line].ranked_score += count
                    game_DB[line].list_count += 1
                    game_DB[line].lists_referencing.append(f)
                    game_DB[line].total_count += original_count
                else:
                    newObj = GameObject(count, f, original_count)
                    game_DB[line] = newObj
                #searchObj = game_DB.get(newObj, 0) + 1
                #game_DB[line].list_count = game_DB.get(newObj, 0) + 1
                print(f"Score of {count}: {line.strip()}")
                #count -= 1
            games_lists.append(filename)

    completeFile = open(check_for_src('Completions.txt'), 'r')
    completeLines = completeFile.readlines()
    for line in completeLines:
        stripped_line = line.strip()
        line = stripped_line
        if line in game_DB:
            game_DB[line].completed = True
        #else: raise error because not in database? create it with 0 score? probably just ignore it?
"""