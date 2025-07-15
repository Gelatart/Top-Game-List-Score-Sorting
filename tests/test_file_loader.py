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