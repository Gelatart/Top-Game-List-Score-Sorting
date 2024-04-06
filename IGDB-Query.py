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
(Seems like using the & symbol can break queries even when it's in the name?)

1080 Snowboarding: IGDB ID: 3328
Command & Conquer: Red Alert 2 (name seems to be crashing request?): IGDB ID: 245
Contra NES: IGDB ID: 186207
Daytona USA Sega Saturn: IDGB ID: 177619
Donkey Kong '94: IGDB ID: 1089
Donkey Kong Country GBC: IGDB ID: 152752
Doom 2016: IGDB ID: 7351
Dragon Warrior III GBC: IGDB ID: 205600
Final Fantasy XIV Online (A Realm Reborn) (Online reboot 2013): IGDB ID: 386
Fire Emblem Fates: Birthright (and Conquest and Revelation): IGDB ID: 24220
FTL: Advanced Edition (not matching for some reason?): IGDB ID: 20098
God of War 2018: IGDB ID: 19560
Harry Potter and the Chamber of Secrets GBC: IGDB ID: 117322
Harry Potter and the Sorcerer's Stone GBC: IGDB ID: 118554
Ivan "Ironman" Stewart's Super Off Road (name seems to be crashing IGDB API request?): IGDB ID: 12735
Mario Golf GBC: IGDB ID: 135389
Mario Tennis GBC: IGDB ID: 128874
Metal Gear Solid GBC: IGDB ID: 5600
Mr. Driller GBC: IGDB ID: 254519
Nights Into Dreams (2008 PC Version, because Nights + Christmas Nights): IGDB ID: 19903
Ninja Gaiden 2004: IGDB ID: 5972
Ninja Gaiden NES: IGDB ID: 210484 (Will it be an issue that this is a port with a parent, the arcade original?)
Ōkami/Okami: IGDB ID: 1271
Ōkami/Okami HD: IGDB ID: 20744
Perfect Dark GBC: IGDB ID: 1464
Pokemon Black Version (what about white?): IGDB ID: 1521
Pokemon Black Version 2 (what about white 2?): IGDB ID: 8284
Pokemon Crystal Version: IGDB ID: 1514
Pokemon Diamond Version (what about peral?): IGDB ID: 1560
Pokemon Emerald Version): IGDB ID: 1517
Pokemon Fire Red Version (what about leaf green?): IGDB ID: 1559
Pokemon Gold Version (what about silver?): IGDB ID: 1558
Pokemon Heart Gold Version (what about soul silver?): IGDB ID: 1556
Pokemon Mystery Dungeon: Explorers of Sky: IGDB ID: 2323
Pokemon Pinball: IGDB ID: 4068
Pokemon Puzzle Challenge: IGDB ID: 49857
Pokemon Red Version (what about blue?): IGDB ID: 1561
Pokemon Ruby Version (what about Sapphire?): IGDB ID: 1557
Pokemon Trading Card Game GBC: IGDB ID: 4567
Pokemon XD: Gale of Darkness: IGDB ID: 2724
Pokemon Yellow Version: IGDB ID: 1512
Ratchet and Clank (name seems to be crashing IGDB API request?): IGDB ID: 1289
Ratchet and Clank: Up Your Arsenal (name seems to be crashing IGDB API request?): IGDB ID: 1773
Rayman GBC: IGDB ID: 85578
Resident Evil 2 2019: IGDB ID: 19686
Resident Evil 4 2023: IGDB ID: 132181
Singstar 2007 (had in my list that we had a 2008 one?): IGDB ID: 15180
Teenage Mutant Ninja Turtles NES: IGDB ID: 86386
Trials of Mana 2020: IGDB ID: 119391
Warcraft II Battle.net edition (name doesn't seem to match?): IGDB ID: 127782
"""