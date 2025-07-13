from dataclasses import dataclass, field
import pytest
import os
from dotenv import load_dotenv
import json

from src.generator.exporter import export_to_text
from src.generator.file_loader import read_game_list, read_attributed_games
from src.generator.game_object import GameObject
from src.generator.sql_manager import SQLManager

def test_non_class_test():
    """
    This one exists just so we can call it with :: from the command line
    and not have to worry about being part of a class
    """
    assert("Test") == "Test"

#Split this file into separate testers for each of the individual classes based on what chatgpt said?


"""
Exporter Tests
"""
def test_export_to_text(tmp_path):
    path = tmp_path / "games.txt"
    games = [
        GameObject(title="Test 1", ranked_score=10, list_source="List1", total_count=100),
        GameObject(title="Test 2", ranked_score=20, list_source="List2", total_count=100),
    ]
    export_to_text(games, str(path))
    contents = path.read_text()
    assert "Test 1: 10" in contents
    assert "Test 2: 20" in contents

"""
File_Loader Tests
"""

def test_read_completed_games(tmp_path):
    file = tmp_path / "completed.txt"
    file.write_text("Game X\nGame Y\n")
    result = read_attributed_games(str(file))
    assert result == ["Game X", "Game Y"]

"""
SQL_Manager Tests
"""

def test_sql_insert_and_fetch_pre_ID():
    db = SQLManager(":memory:")
    game = GameObject(title="Test Game", ranked_score=50, list_source="list.txt", total_count=100)
    db.insert_or_update_game_pre_ID(game)
    results = db.get_all_games()
    assert len(results) == 1
    db.close()

#Referencing this tutorial: https://betterstack.com/community/guides/testing/pytest-guide/