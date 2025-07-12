import os
import json
import requests
from igdb.wrapper import IGDBWrapper

from .config import get_env_var

class IGDB_Client:
    def __init__(self):
        self.client_id = get_env_var("CLIENT_ID")
        self.client_secret = get_env_var("CLIENT_SECRET")
        #self.access_token = get_env_var("IGDB_ACCESS_TOKEN")
        #can't just get access_token like this, need to request from IGDB to grab it
        post = f'https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials'
        page = requests.post(post)  # gives access token we can use
        received = json.loads(page.text)
        self.access_token = received["access_token"]
        self.wrapper = IGDBWrapper(self.client_id, self.access_token)

    def search_game_by_title(self, title: str) -> dict:
        """
        Search IGDB for a game title and return the most relevant result.
        """
        query = f'search "{title}"; fields id, name, genres.name, release_dates.date, platforms.name, involved_companies.company.name, involved_companies.developer, involved_companies.publisher; limit 1;'
        #is developer and publisher a little overkill for now?
        response = self.wrapper.api_request("games", query)
        #Trying out json approach instead of protobuf response I used to use
        #games_data = json.loads(response.decode('utf-8'))
        return response[0] if response else {}

    #make a search_game_by_igdb_id function

    def enrich_game_object(self, game_obj):
        """
        Update GameObject fields based on IGDB API result.
        """
        igdb_data = self.search_game_by_title(game_obj.list_source)
        #give option to search by igdb_ID?

        if not igdb_data:
            return

        game_obj.igdb_ID = igdb_data.get("id")
        #consider doing get("id", "N/A") instead?
        game_obj.igdb_found = True
        game_obj.release_date = str(igdb_data.get("release_dates", [{}])[0].get("date", "Unknown"))
        #^consider giving a null value or clearly wrong datetime if not date found?
        #try to make it some format other than string?

        platforms = igdb_data.get("platforms", [])
        game_obj.list_platforms = [p.get("name") for p in platforms if p.get("name")]
        if game_obj.list_platforms:
            game_obj.main_platform = game_obj.list_platforms[0]

        genres = igdb_data.get("genres", [])
        game_obj.genres = [g.get("name") for g in genres if g.get("name")]

        companies = igdb_data.get("involved_companies", [])
        for c in companies:
            name = c.get("company", {}).get("name")
            if not name:
                continue
            if c.get("developer"):
                game_obj.list_developers.append(name)
            if c.get("publisher"):
                game_obj.list_publishers.append(name)
            game_obj.list_companies.append(name)
