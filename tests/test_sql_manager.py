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