import pytest

from src.generator.game_object import GameObject
from src.generator.sql_manager import SQLManager

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
    #Right now saying no such table: games, need to find need way to initialize?

def test_insert_raises_operational_error():
    db = SQLManager(":memory:")
    db.close()  # Simulate closed DB connection

    game = GameObject(title="Bad", ranked_score=1, list_source="src", total_count=1)

    with pytest.raises(Exception):  # or sqlite3.ProgrammingError
        db.insert_or_update_game_pre_ID(game)