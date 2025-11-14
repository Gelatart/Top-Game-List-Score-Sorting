import os
import json
import re
import requests
import unicodedata
from datetime import datetime
from igdb.wrapper import IGDBWrapper

from .config import get_env_var
from .cache_manager import CacheManager

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
        self.cache = CacheManager()

    def parse_igdb_release_dates(self, raw_dates):
        """
        Parse IGDB release_dates array into a list of dicts.
        Each release date from IGDB has: date (unix timestamp), platform (object with id/name), region (id), human (string)
        """
        release_dates = []
        for rd in raw_dates:
            date_timestamp = rd.get("date")
            date_str = datetime.utcfromtimestamp(date_timestamp).strftime("%Y-%m-%d") if date_timestamp else None
            
            # Platform can be either an ID or an object with name
            platform_data = rd.get("platform")
            platform_name = None
            if isinstance(platform_data, dict):
                platform_name = platform_data.get("name")
            
            release_dates.append({
                "platform_name": platform_name,
                "region_id": rd.get("region"),
                "release_date": date_str,
                "human_readable": rd.get("human")
            })
        return release_dates

    def search_game_by_ID(self, igdb_id: int) -> dict:
        cached = self.cache.get(igdb_id)
        if cached:
            print("We already have this!")
            print(cached)
            return cached

        query = f'fields id, name, genres.name, themes.name, game_modes.name, platforms.name, release_dates.date, release_dates.platform.name, release_dates.region, release_dates.human, involved_companies.company.name, involved_companies.developer, involved_companies.publisher; limit 1; where id = {igdb_id};'
        response = self.wrapper.api_request("games", query)
        games_data = json.loads(response.decode("utf-8"))
        result = games_data[0] if games_data else {}

        if result.get("id"):
            self.cache.set(result["id"], result)
        return result

    def search_game_by_title(self, title: str) -> dict:
        """
        Search IGDB for a game title and return the most relevant result.
        """
        #Add logic for parsing when it starts with <> at the start of the name
        if (title.startswith('<')):
            new_title = title.strip()
            pattern_match = r'[0-9]+'
            substring = re.findall(pattern_match, new_title)
            #input(new_title)
            title_ID = substring[0]
            removal = '<' + title_ID + '> '
            modified_title = title.strip(removal)

            # Check the cache to see if we already got the IGDB info we need
            #cached = self.cache.get(modified_title)
            #if cached:
                #return cached
            return self.search_game_by_ID(title_ID)
        else:
            #Normalize the title so it doesn't have any characters that will cause the IGDB API request to fail
            normalized_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("utf-8")

            #Check the cache to see if we already got the IGDB info we need
            #cached = self.cache.get(normalized_title)
            #if cached:
                #return cached

            #If it's not cached, time for an API call
            #Come up with functionality where if this normalized version isn't found, bring it to user's attention? So we can know to use IGDB ID instead?
            query = f'search "{normalized_title}"; fields id, name, genres.name, themes.name, game_modes.name, platforms.name, release_dates.date, release_dates.platform.name, release_dates.region, release_dates.human, involved_companies.company.name, involved_companies.developer, involved_companies.publisher; limit 1;'
            #print(title)
            #query = f'search "{title}"; fields id, name; limit 1;'
            print(query)
            #query = f'search "zelda"; fields id, name; limit 1;'
            #query = f'fields name, rating; limit 1;'
            #is developer and publisher a little overkill for now?
            response = self.wrapper.api_request("games", query)
            """
            response = self.wrapper.api_request(
                'games.pb',  # Note the '.pb' suffix at the endpoint
                'fields name, rating; limit 5; offset 0;'
            )
            """
            #print(response)
            #print(type(response))
            #print(response[0]) if response else print("")
            if isinstance(response, bytes):
                games_data = json.loads(response.decode("utf-8"))
            elif isinstance(response, str):
                games_data = json.loads(response)
            else:
                games_data = response
            #print(type(games_data))
            #print(type(games_data[0])) if games_data else print("")
            #Trying out json approach instead of protobuf response I used to use
            #return response[0] if response else {}
            #return response if response else {}
            result = games_data[0] if games_data else {}

            if result.get("id"):
                cached = self.cache.get(result["id"])
                if cached:
                    print("We already have this!")
                    print(cached)
                    return cached
                else:
                    self.cache.set(result["id"], result)

            #Store the title in our cache
            #self.cache.set(normalized_title, result)

            return result

    #make a search_game_by_igdb_id function

    def enrich_game_object(self, game_obj):
        """
        Update GameObject fields based on IGDB API result. Should get all fields we will need.
        """
        igdb_data = self.search_game_by_title(game_obj.title)
        #input(f"IGDB_DATA: {igdb_data}")
        #give option to search by igdb_ID?

        if not igdb_data:
            return

        game_obj.igdb_ID = igdb_data.get("id")
        game_obj.igdb_found = True
        
        # Parse release dates
        raw_release_dates = igdb_data.get("release_dates", [])
        if raw_release_dates:
            game_obj.release_dates = self.parse_igdb_release_dates(raw_release_dates)
            # Set the earliest release date as the main release_date for backward compatibility
            earliest = min((rd for rd in game_obj.release_dates if rd.get("release_date")), 
                          key=lambda x: x["release_date"], default=None)
            # How do we settle tie-breakers?
            #Make sure that we also account for only doing games that actually released so we don't get 1970 values
            game_obj.release_date = earliest["release_date"] if earliest else "Unknown"
        else:
            game_obj.release_date = "Unknown"

        platforms = igdb_data.get("platforms", [])
        game_obj.list_platforms = [p.get("name") for p in platforms if p.get("name")]
        #derive a main_platform?

        genres = igdb_data.get("genres", [])
        #input(genres)
        themes = igdb_data.get("themes", [])
        #input(themes)
        player_counts = igdb_data.get("game_modes", [])
        #input(player_counts)
        game_obj.genres = [g.get("name") for g in genres if g.get("name")]
        game_obj.themes = [t.get("name") for t in themes if t.get("name")]
        game_obj.player_counts = [p.get("name") for p in player_counts if p.get("name")]

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

    """
    TYPES FOR GAME_MODES (Based on id #):
    1: Singleplayer?
        2, 3: Multiplayer? (2 might just be some form of singleplayer? multi against npcs's?)
    2: Multiplayer?
    3: Co-op?
    4: Split-screen?
    5: MMO?
    6: Battle Royale?
    No others at this time?

    FOR INVOLVED_COMPANIES, WE WILL LIKELY NEED TO USE A DIFFERENT ENDPOINT TO FIGURE OUT WHAT THEY ALL ARE,
    BECAUSE SO MANY POTENTIAL ID NUMBERS

    TYPE FOR PLATFORM FAMILIES (Based on id #):
    1: PlayStation
    2: Xbox
    3: Sega
    4: Linux
    5: Nintendo
    No others at this time?
    """