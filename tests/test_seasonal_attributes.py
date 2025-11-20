"""Tests for seasonal attributes in GameObject"""

from src.generator.game_object import GameObject


class TestSeasonalAttributes:
    def test_seasonal_defaults(self):
        """Test that seasonal attributes default to False"""
        game = GameObject(title="Test Game", ranked_score=100, total_count=50)
        
        assert game.seasonal_spring is False
        assert game.seasonal_summer is False
        assert game.seasonal_fall_halloween is False
        assert game.seasonal_winter_christmas is False

    def test_seasonal_multiple_flags(self):
        """Test that multiple seasonal flags can be True simultaneously"""
        game = GameObject(
            title="Animal Crossing: New Horizons",
            ranked_score=100,
            total_count=50,
            seasonal_spring=True,
            seasonal_summer=True
        )
        
        assert game.seasonal_spring is True
        assert game.seasonal_summer is True
        assert game.seasonal_fall_halloween is False
        assert game.seasonal_winter_christmas is False

    def test_seasonal_in_to_dict(self):
        """Test that to_dict() includes seasonal attributes"""
        game = GameObject(
            title="Test Game",
            ranked_score=100,
            total_count=50,
            seasonal_spring=True,
            seasonal_winter_christmas=True
        )
        
        game_dict = game.to_dict()
        
        assert "seasonal_spring" in game_dict
        assert "seasonal_summer" in game_dict
        assert "seasonal_fall_halloween" in game_dict
        assert "seasonal_winter_christmas" in game_dict
        
        assert game_dict["seasonal_spring"] is True
        assert game_dict["seasonal_summer"] is False
        assert game_dict["seasonal_fall_halloween"] is False
        assert game_dict["seasonal_winter_christmas"] is True

    def test_all_seasonal_flags_true(self):
        """Test that all seasonal flags can be True at once"""
        game = GameObject(
            title="Multi-Season Game",
            ranked_score=100,
            total_count=50,
            seasonal_spring=True,
            seasonal_summer=True,
            seasonal_fall_halloween=True,
            seasonal_winter_christmas=True
        )
        
        assert game.seasonal_spring is True
        assert game.seasonal_summer is True
        assert game.seasonal_fall_halloween is True
        assert game.seasonal_winter_christmas is True
