#Imports grabbed from generator.py I thought I might need
import os
import dotenv
from dotenv import load_dotenv
import requests
from igdb.wrapper import IGDBWrapper
import json

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
post = 'https://id.twitch.tv/oauth2/token?client_id='
post += client_id
post += '&client_secret='
post += client_secret
post += '&grant_type=client_credentials'

#page = requests.get(post) #404
page = requests.post(post) #gives access token we can use
print(page.text)
#input("Here we pause")

#wrapper = IGDBWrapper("YOUR_CLIENT_ID", "YOUR_APP_ACCESS_TOKEN")
received = json.loads(page.text)
access_token = received["access_token"]
#print(access_token)
wrapper = IGDBWrapper(client_id, access_token)
#input("Here we pause")

from igdb.igdbapi_pb2 import GameResult
igdb_request = wrapper.api_request(
            'games.pb', # Note the '.pb' suffix at the endpoint
            #'fields name, rating; limit 5; offset 0;'
            'fields name, rating; offset 0;'
          )
games_message = GameResult()
games_message.ParseFromString(igdb_request) # Fills the protobuf message object with the response
games = games_message.games
#print(games)
#input("Here we pause")

query = input("Enter your query for the IGDB API here. Make sure to use the proper syntax to not have an error\n")
print(query)
"""
check_string = 'fields *; exclude age_ratings, alternative_names, artworks, checksum, collections, cover, '
check_string += 'created_at, follows, game_localizations, genres, involved_companies, keywords, language_supports, '
check_string += 'player_perspectives, rating_count, release_dates, screenshots, similar_games, tags, themes, '
check_string += 'updated_at, videos, websites; '
check_string += 'where name = "'
check_string += game.strip()
check_string += '" & version_parent = null; offset 0;' #6 is cancelled,  & status != 6

Test query for Pokemon Red: 'fields *; where id = '1561'; offset 0;'
Additional query for Pokemon Red: 'fields *; where name = 'Pokémon Red Version'; offset 0;'
"""

igdb_request = wrapper.api_request(
    'games.pb',  # Note the '.pb' suffix at the endpoint
    query
)
games_message = GameResult()
games_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
games = games_message.games

print(games)

print("Successfully completed! Goodbye!")

#POKEMON RED VERSION PAGE: https://www.igdb.com/games/pokemon-red-version

#SPECIAL CASES KNOWN SO FAR:
"""
Pokemon Red Version (what about blue?): IGDB ID: 1561
God of War 2018: IGDB ID: 19560
Pokemon Gold Version (what about silver?): IGDB ID: 1558
"""