"""Integration tests for seasonal tagging in generator"""

import tempfile
import os
from pathlib import Path
from src.generator.file_loader import read_attributed_games
from src.generator.game_object import GameObject


class TestGeneratorSeasonal:
    def test_read_seasonal_files_missing(self):
        """Test that read_attributed_games returns empty list for missing files"""
        # Use a path that definitely doesn't exist
        result = read_attributed_games(Path("game_lists") / "NonExistent.txt")
        assert result == []

    def test_seasonal_tagging_logic(self):
        """Test the seasonal tagging logic with a mock game_DB"""
        # Create a mock game database
        game_DB = {
            "Animal Crossing: New Horizons": GameObject(
                title="Animal Crossing: New Horizons",
                ranked_score=100,
                total_count=50
            ),
            "The Legend of Zelda: Breath of the Wild": GameObject(
                title="The Legend of Zelda: Breath of the Wild",
                ranked_score=95,
                total_count=45
            ),
            "Super Mario Odyssey": GameObject(
                title="Super Mario Odyssey",
                ranked_score=90,
                total_count=40
            )
        }

        # Simulate seasonal title sets (as would be read from files)
        spring_titles = {"Animal Crossing: New Horizons"}
        summer_titles = {"Animal Crossing: New Horizons", "Super Mario Odyssey"}
        fall_titles = set()
        winter_titles = {"The Legend of Zelda: Breath of the Wild"}

        # Apply seasonal tags (mimicking generator logic)
        for title in spring_titles:
            if title in game_DB:
                game_DB[title].seasonal_spring = True

        for title in summer_titles:
            if title in game_DB:
                game_DB[title].seasonal_summer = True

        for title in fall_titles:
            if title in game_DB:
                game_DB[title].seasonal_fall_halloween = True

        for title in winter_titles:
            if title in game_DB:
                game_DB[title].seasonal_winter_christmas = True

        # Verify the tags were applied correctly
        ac = game_DB["Animal Crossing: New Horizons"]
        assert ac.seasonal_spring is True
        assert ac.seasonal_summer is True
        assert ac.seasonal_fall_halloween is False
        assert ac.seasonal_winter_christmas is False

        zelda = game_DB["The Legend of Zelda: Breath of the Wild"]
        assert zelda.seasonal_spring is False
        assert zelda.seasonal_summer is False
        assert zelda.seasonal_fall_halloween is False
        assert zelda.seasonal_winter_christmas is True

        mario = game_DB["Super Mario Odyssey"]
        assert mario.seasonal_spring is False
        assert mario.seasonal_summer is True
        assert mario.seasonal_fall_halloween is False
        assert mario.seasonal_winter_christmas is False

    def test_seasonal_file_with_content(self):
        """Test reading a seasonal file with actual content"""
        # Create a temporary file with game titles
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Animal Crossing: New Horizons\n")
            f.write("<1070> Super Mario World\n")
            f.write("The Legend of Zelda: Breath of the Wild\n")
            temp_path = f.name

        try:
            # Read the file
            titles = read_attributed_games(Path(temp_path))
            
            # Verify the content
            assert len(titles) == 3
            assert "Animal Crossing: New Horizons" in titles
            assert "<1070> Super Mario World" in titles
            assert "The Legend of Zelda: Breath of the Wild" in titles
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_seasonal_file_empty_lines(self):
        """Test that empty lines are ignored in seasonal files"""
        # Create a temporary file with empty lines
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Game One\n")
            f.write("\n")
            f.write("Game Two\n")
            f.write("   \n")
            f.write("Game Three\n")
            temp_path = f.name

        try:
            # Read the file
            titles = read_attributed_games(Path(temp_path))
            
            # Verify empty lines are ignored
            assert len(titles) == 3
            assert "Game One" in titles
            assert "Game Two" in titles
            assert "Game Three" in titles
        finally:
            # Clean up
            os.unlink(temp_path)
