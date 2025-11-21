from src.generator.file_loader import read_game_list, read_attributed_games

"""
File_Loader Tests
"""

#def test_read_game_list_ranked(tmp_path): Implement?

def test_read_completed_games(tmp_path):
    file = tmp_path / "completed.txt"
    file.write_text("Game X\nGame Y\n")
    result = read_attributed_games(str(file))
    assert result == ["Game X", "Game Y"]

def test_read_attributed_games_missing_file(tmp_path):
    """Test that read_attributed_games returns empty list when file doesn't exist"""
    non_existent_file = tmp_path / "nonexistent.txt"
    result = read_attributed_games(str(non_existent_file))
    assert result == []

def test_read_attributed_games_existing_file():
    """Test that read_attributed_games works with the actual Completions.txt file"""
    result = read_attributed_games('game_lists/Completions.txt')
    assert isinstance(result, list), "Should return a list"
    assert len(result) > 0, "Completions.txt should contain at least one game"
    # Verify all entries are non-empty strings
    assert all(isinstance(game, str) and game for game in result), "All entries should be non-empty strings"