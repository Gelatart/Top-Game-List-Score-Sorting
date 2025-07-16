from src.generator.game_object import GameObject

def test_gameobject_creation_defaults():
    g = GameObject(title="Test Game", ranked_score=90, list_source="list1.txt", total_count=100)
    assert g.ranked_score == 90
    assert g.list_count == 1
    assert g.completed is False
    assert g.lists_referencing == ["list1.txt"]

def test_gameobject_to_dict():
    g = GameObject(title="Test Game", ranked_score=80, list_source="src.txt", total_count=200)
    d = g.to_dict()
    assert isinstance(d, dict)
    assert d["ranked_score"] == 80
    assert "main_platform" in d