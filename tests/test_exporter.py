from src.generator.exporter import export_to_text
from src.generator.game_object import GameObject

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