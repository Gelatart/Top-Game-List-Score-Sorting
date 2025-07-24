import json
import pytest

from src.generator.igdb_client import IGDB_Client

@pytest.fixture
def mock_igdb_client(monkeypatch):
    class MockWrapper:
        def api_request(self, endpoint, query):
            data = [{
                "id": 12345,
                "name": "Test Game",
                "genres": [{"name": "Adventure"}]
            }]
            return json.dumps(data).encode("utf-8")  # Simulate bytes from requests
    class Mock_IGDB_Client:
        def __init__(self):
            self.wrapper = MockWrapper()
            self.client = IGDB_Client()

        def search_game_by_title_bytes(self, title):
            #return IGDB_Client(self.wrapper).search_game_by_title(title)
            #return self.wrapper.search_game_by_title(title)
            self.client.wrapper = self.wrapper
            #monkeypatch.setattr(self.client.wrapper, "api_request", fake_api_request)
            return self.client.search_game_by_title(title)

        def search_game_by_title_list(self, title):
            #client = IGDB_Client()

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

            monkeypatch.setattr(self.client.wrapper, "api_request", fake_api_request)
            #return self.client
            return self.client.search_game_by_title(title)
    return Mock_IGDB_Client()

#client.search_game = lambda title: {"id": 123, "genres": [{"name": "Action"}], ...}

def test_mock_search_game_by_title_bytes_returns_expected_result(mock_igdb_client):
    result = mock_igdb_client.search_game_by_title_bytes("Test Game")
    print(result)
    assert result["id"] == 12345
    assert result["name"] == "Test Game"
    assert result["genres"][0]["name"] == "Adventure"

#MAKE A NEW TEST FUNCTION THAT SEARCHES IN A NON-BYTES WAY, LIKE ORIGINAL
def test_mock_search_game_by_title_list_returns_expected_result(mock_igdb_client):
    result = mock_igdb_client.search_game_by_title_list("Test Game")
    print(result)
    assert result["id"] == 12345
    assert result["name"] == "Test Game"
    assert result["genres"][0]["name"] == "Adventure"