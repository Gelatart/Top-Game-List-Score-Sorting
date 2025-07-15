import pytest

from src.generator.igdb_client import IGDB_Client

@pytest.fixture
def mock_igdb_client(monkeypatch):
    client = IGDB_Client()

    # Replace the actual API request method with a fake one
    def fake_api_request(endpoint, query):
        assert endpoint == "games"
        assert "search" in query
        return [{
            "id": 12345,
            "name": "Test Game",
            "genres": [{"name": "Adventure"}],
            "release_dates": [{"date": 1625097600}],
            "platforms": [{"name": "PC"}],
            "involved_companies": [
                {"company": {"name": "Cool Devs"}, "developer": True, "publisher": False}
            ]
        }]

    monkeypatch.setattr(client.wrapper, "api_request", fake_api_request)
    return client

#client.search_game = lambda title: {"id": 123, "genres": [{"name": "Action"}], ...}

def test_mock_search_game_by_title_returns_expected_result(mock_igdb_client):
    result = mock_igdb_client.search_game_by_title("Test Game")
    assert result["id"] == 12345
    assert result["name"] == "Test Game"
    assert result["genres"][0]["name"] == "Adventure"