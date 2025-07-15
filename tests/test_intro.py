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

#Look into optional conftest.py chatgpt was recommending: would have a fixture with a sample_game?

#Referencing this tutorial: https://betterstack.com/community/guides/testing/pytest-guide/