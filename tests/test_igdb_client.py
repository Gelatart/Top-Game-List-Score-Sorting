from dataclasses import dataclass, field
import json
import pytest
import re
import unicodedata

from src.generator.igdb_client import IGDB_Client

@pytest.fixture
def mock_igdb_client(monkeypatch):
    class MockWrapper:
        def api_request(self, endpoint, query):
            data = [{
                "id": 12345,
                "name": "Untitled Test Game",
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
            if (title.startswith('<')):
                new_title = title.strip()
                pattern_match = r'[0-9]+'
                substring = re.findall(pattern_match, new_title)
                title_ID = substring[0]
                title = title_ID
            else:
                normalized_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("utf-8")
                title = normalized_title
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
                    "name": "Untitled Test Game",
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
    result = mock_igdb_client.search_game_by_title_bytes("Untitled Test Game")
    print(result)
    assert result["id"] == 12345
    assert result["name"] == "Untitled Test Game"
    assert result["genres"][0]["name"] == "Adventure"

#MAKE A NEW TEST FUNCTION THAT SEARCHES IN A NON-BYTES WAY, LIKE ORIGINAL
def test_mock_search_game_by_title_list_returns_expected_result(mock_igdb_client):
    result = mock_igdb_client.search_game_by_title_list("Untitled Test Game")
    print(result)
    assert result["id"] == 12345
    assert result["name"] == "Untitled Test Game"
    assert result["genres"][0]["name"] == "Adventure"

@dataclass
class GameTitleTestCase:
    input_title: str
    expected_output: str
    id: str

test_cases = [
    GameTitleTestCase("üntitled Test Game", "Untitled Test Game", "special"),
    GameTitleTestCase("Untitled Test Game", "Untitled Test Game", "standard"),
    GameTitleTestCase("<1234> Untitled Test Game", "Untitled Test Game", "IGDB ID")
]

"""
@pytest.mark.parametrize(
    "input_title, expected_output",
    [
        pytest.param("üntitled Test Game", "Untitled Test Game", id="special"),       # special character
        #("Brutal Legend", "Brütal Legend"),       # normalized fallback
        pytest.param("Untitled Test Game", "Untitled Test Game", id="standard"),                     # standard
        pytest.param("<1234> Untitled Test Game", "Untitled Test Game", id="IGDB ID"),  # pattern with leading ID
    ])
def test_search_game_title_variants_bytes(mock_igdb_client, input_title, expected_output):
"""
@pytest.mark.parametrize("test_case", test_cases, ids=lambda tc: tc.id)
def test_search_game_title_variants_bytes(mock_igdb_client, test_case):
    result = mock_igdb_client.search_game_by_title_bytes(test_case.input_title)
    assert result["name"] == test_case.expected_output