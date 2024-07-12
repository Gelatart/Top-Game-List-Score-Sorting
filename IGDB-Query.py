#Imports grabbed from generator.py I thought I might need
import os
import dotenv
from dotenv import load_dotenv
import requests
from igdb.wrapper import IGDBWrapper
import json

from igdb.igdbapi_pb2 import GameResult
from igdb.igdbapi_pb2 import GameModeResult
from igdb.igdbapi_pb2 import PlatformResult
from igdb.igdbapi_pb2 import PlatformFamilyResult
from igdb.igdbapi_pb2 import InvolvedCompanyResult
from igdb.igdbapi_pb2 import CompanyResult
from igdb.igdbapi_pb2 import GenreResult
from igdb.igdbapi_pb2 import ThemeResult
from igdb.igdbapi_pb2 import ReleaseDateResult

#deal with query syntax errors better? here and in other progams? exception handling?

def query_loop(endpoint_option):
    while True:
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

        This works for FTL: Advanced Edition: fields *; where id = '20098'; offset 0;
        fields *; where id = '20098' & version_parent = null; offset 0; //Doesn't get result in this case
        
        fields *; exclude age_ratings, aggregated_rating, aggregated_rating_count, alternative_names, artworks, bundles, checksum, collection, collections, cover, created_at, expanded_games, external_games, follows, franchises, game_localizations, keywords, language_supports, player_perspectives, rating, rating_count, release_dates, screenshots, similar_games, standalone_expansions, storyline, tags, total_rating, total_rating_count, updated_at, videos, websites; where name = "Animal Crossing: New Horizons"; offset 0;
        """

        # igdb_request = None

        if (endpoint_option == "games"):
            igdb_request = wrapper.api_request(
                'games.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            games_message = GameResult()
            games_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            games = games_message.games

            print(games)
            print(len(games))

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return #To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        elif (endpoint_option == "1"):
            # Game_Modes
            igdb_request = wrapper.api_request(
                'game_modes.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            modes_message = GameModeResult()
            modes_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            modes = modes_message.gamemodes  # Correct syntax for it is gamemodes

            print(modes)
            # Doing the fields *; query for this helped me find all of the types of game_modes

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return  # To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        elif (endpoint_option == "2"):
            # Platforms
            igdb_request = wrapper.api_request(
                'platforms.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            platforms_message = PlatformResult()
            platforms_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            platforms = platforms_message.platforms  # Correct syntax for it is gamemodes

            print(platforms)

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return  # To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        elif (endpoint_option == "3"):
            # Platform Families
            igdb_request = wrapper.api_request(
                'platform_families.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            platforms_message = PlatformFamilyResult()
            platforms_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            platform_families = platforms_message.platformfamilies  # Correct syntax for it is gamemodes

            print(platform_families)

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return  # To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        elif (endpoint_option == "4"):
            # Involved Company
            igdb_request = wrapper.api_request(
                'involved_companies.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            company_message = InvolvedCompanyResult()
            company_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            companies = company_message.involvedcompanies

            print(companies)

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return  # To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        elif (endpoint_option == "5"):
            # Company
            igdb_request = wrapper.api_request(
                'companies.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            company_message = CompanyResult()
            company_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            companies = company_message.companies

            print(companies)

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return  # To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        elif (endpoint_option == "6"):
            #GENRE
            igdb_request = wrapper.api_request(
                'genres.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            #GENRE SEEMS TO BE BROKEN STILL?
            genre_message = GenreResult() #not finding this quite yet?
            genre_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            genres = genre_message.genres

            print(genres)

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return  # To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        elif (endpoint_option == "7"):
            # THEME
            igdb_request = wrapper.api_request(
                'themes.pb',  # Note the '.pb' suffix at the endpoint
                query
            )
            #TEST THIS!!!
            theme_message = ThemeResult()  # not finding this quite yet?
            theme_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            themes = theme_message.themes

            print(themes)

            while True:
                print()
                print("Would you like to keep going with this endpoint?")
                quit_answer = input()
                if (quit_answer == 'Y' or quit_answer == 'Yes' or quit_answer == 'y' or quit_answer == 'yes'):
                    print()
                    print("Alright! Back to querying!")
                    print()
                    break
                elif (quit_answer == 'N' or quit_answer == 'No' or quit_answer == 'n' or quit_answer == 'no'):
                    print()
                    print("Alright! Let's finish up with this endpoint!")
                    print()
                    return  # To get out of function and back to main code
                else:
                    print()
                    print("Sorry, I don't understand. Try again")
                    continue
        else:
            print("Sorry, I don't understand. Try again")
            continue

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
"""
post = 'https://id.twitch.tv/oauth2/token?client_id='
post += client_id
post += '&client_secret='
post += client_secret
post += '&grant_type=client_credentials'
"""
post = f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'

#page = requests.get(post) #404
page = requests.post(post) #gives access token we can use
print(page.text)

#wrapper = IGDBWrapper("YOUR_CLIENT_ID", "YOUR_APP_ACCESS_TOKEN")
received = json.loads(page.text)
access_token = received["access_token"]
#print(access_token)
wrapper = IGDBWrapper(client_id, access_token)

igdb_request = wrapper.api_request(
            'games.pb', # Note the '.pb' suffix at the endpoint
            #'fields name, rating; limit 5; offset 0;'
            'fields name, rating; offset 0;'
          )
games_message = GameResult()
games_message.ParseFromString(igdb_request) # Fills the protobuf message object with the response
games = games_message.games

endpoint_types = { '1': 'Game Modes', '2': 'Platforms', '3': 'Platform Family', '4': 'Involved Company', '5': 'Company', '6': 'Genre', '7': 'Theme'}

while True:
#give option to return back here or just to option already set upon
    print("Would you like to use the games endpoint or another?")
    print("1. Games")
    print("2. Another")
    print("3. Quit Program")
    endpoint_option_1 = input()
    if(endpoint_option_1 == "1"):
        print()
        print("You have selected Games, the usual. Let's get started!")
        print()
        query_loop('games')
    elif(endpoint_option_1 == "2"):
        print()
        print("You have selected another. Which endpoint would you like to use?")
        print("1. Game Modes")
        print("2. Platform")
        print("3. Platform Family")
        print("4. Involved Company")
        print("5. Company")
        print("6. Genre")
        print("7. Theme")
        #...
        endpoint_option_2 = input()
        print()
        print(f"You have selected: {endpoint_types[endpoint_option_2]}")
        print()
        query_loop(endpoint_option_2)
    elif (endpoint_option_1 == "3"):
        print()
        print("Alright! Wrapping up the program!")
        print()
        break
    else:
        print()
        print("Sorry, I don't understand. Try again")
        print()
        continue

print("Successfully completed! Goodbye!")

#create a function/program that scans IGDB ID's for duplicates so I can give them consistent formatting
#display all titles found for a certain ID so I can compare and determine best title
#give functionality to rewrite them in the files based on that?
#process would likely take long so leave it in the background to come back to
#have it pause itself, or keep track of what noted to have me review through the end of the process?
#build up a stack to go through at the very end

#SPECIAL CASES KNOWN SO FAR:
"""
(Seems like using the & symbol can break queries even when it's in the name?)
(Seems like it has difficulty picking up the names of games that are bundles at this time?)

(Need to make a page for Out of the Park Baseball 2007, get more proof of existence)
(Need to make a page for Anito Legends)

(Sonic the Hedgehog 8-bit from Master System seems not to be in API?)

1080 Snowboarding: IGDB ID: 3328
Baku Baku [Master System]: IGDB ID: 69785
Batman the Video Game GB: IGDB ID: 49227
Batman: Arkham City - Game of the Year Edition (not matching some reason?): IGDB ID: 21704
Battletoads GB: IGDB ID: 136619
Blade Runner [1997]: IGDB ID: 322
Chrono Trigger DS: IGDB ID: 20398
Command & Conquer: Red Alert 2 (name seems to be crashing request?): IGDB ID: 245
Contra NES: IGDB ID: 186207
Cyberpunk 2077: Ultimate Edition (not matching some reason?): IGDB ID: 277807
Dante's Inferno [2010]: IGDB ID: 6958
Daytona USA Sega Saturn: IDGB ID: 177619
Daytona USA 2001: IGDB ID: 22007
Dead Space 2023: IGDB ID: 159119
Disney's Aladdin SNES: IGDB ID: 2473
Disney's Aladdin GEN: IGDB ID: 8118
Disney's DuckTales GB: IGDB ID: 145268
Divinity: Original Sin II - Definitive Edition (not matching some reason?): IGDB ID: 103337
Donkey Kong '94: IGDB ID: 1089
Donkey Kong Country GBC: IGDB ID: 152752
Doom 2016: IGDB ID: 7351
Doom GBA: IGDB ID: 259941
Doom II: Hell on Earth GBA: IGDB ID: 202120
Dragon Warrior III GBC: IGDB ID: 205600
Fallout 3: Game of the Year Edition (not matching some reason?): IGDB ID: 21892
Final Fantasy IV [2008]: IGDB ID: 399
Final Fantasy XIV Online (A Realm Reborn) (Online reboot 2013): IGDB ID: 386
Fire Emblem Fates: Birthright (and Conquest and Revelation): IGDB ID: 24220
FTL: Advanced Edition (not matching for some reason?): IGDB ID: 20098
Ghosts 'n Goblins [NES]: IGDB ID: 39048
God of War 2018: IGDB ID: 19560
God of War Ragnarok: IGDB ID: 112875
Gothic II: Gold Edition (not matching for some reason?): IGDB ID: 29207
Gran Turismo PSP: IGDB ID: 20426
Harry Potter and the Chamber of Secrets GBC: IGDB ID: 117322
Harry Potter and the Sorcerer's Stone GBC: IGDB ID: 118554
Hitman 2016: IGDB ID: 11157
Ikari Warriors [NES]: IGDB ID: 274081
Ivan "Ironman" Stewart's Super Off Road (name seems to be crashing IGDB API request?): IGDB ID: 12735
Killer Instinct 2013: IGDB ID: 10354
Kirby's Return to Dream Land (name seems to crash it, maybe the apostrophe?): IGDB ID: 3725
Legend of Mana [Remastered]: IGDB ID: 143616
The Lost World: Jurassic Park [Arcade]: IGDB ID: 132135
The Lost World: Jurassic Park [Genesis]: IGDB ID: 8075
Mario Golf GBC: IGDB ID: 135389
Mario Tennis GBC: IGDB ID: 128874
Metal Gear NES: IGDB ID: 133917
Metal Gear Solid GBC: IGDB ID: 5600
Microsoft Flight Simulator 2020: IGDB ID: 119295
Mortal Kombat [2011]: IGDB ID: 119
Mr. Driller GBC: IGDB ID: 254519
Myst [2020]: IGDB ID: 
Need for Speed: Most Wanted 2012: IGDB ID: 3193
Nights Into Dreams (2008 PC Version, because Nights + Christmas Nights): IGDB ID: 19903
Ninja Gaiden 2004: IGDB ID: 5972
Ninja Gaiden NES: IGDB ID: 210484 (Will it be an issue that this is a port with a parent, the arcade original?)
Ōkami/Okami: IGDB ID: 1271
Ōkami/Okami HD: IGDB ID: 20744
Paper Mario: The Thousand-Year Door [2024]: IGDB ID: 266690
Perfect Dark GBC: IGDB ID: 1464
Pokemon Black Version (what about white?): IGDB ID: 1521
Pokemon Black Version 2 (what about white 2?): IGDB ID: 8284
Pokemon Crystal Version: IGDB ID: 1514
Pokemon Diamond Version (what about peral?): IGDB ID: 1560
Pokemon Emerald Version): IGDB ID: 1517
Pokemon Fire Red Version (what about leaf green?): IGDB ID: 1559
Pokemon GO: IGDB ID: 12515
Pokemon Gold Version (what about silver?): IGDB ID: 1558
Pokemon Heart Gold Version (what about soul silver?): IGDB ID: 1556
Pokemon: Let's Go, Pikachu! (what about eevee?): IGDB ID: 25877
Pokemon Mystery Dungeon: Explorers of Sky: IGDB ID: 2323
Pokemon Pinball: IGDB ID: 4068
Pokemon Platinum: IGBD ID: 1519
Pokemon Puzzle Challenge: IGDB ID: 49857
Pokemon Puzzle League: IGDB ID: 3574
Pokemon Red Version (what about blue?): IGDB ID: 1561
Pokemon Ruby Version (what about Sapphire?): IGDB ID: 1557
Pokemon SNAP: IGDB ID: 2324
Pokemon Stadium: IGDB ID: 2289
Pokemon Trading Card Game GBC: IGDB ID: 4567
Pokemon Ultra Sun (what about ultra moon?): IGDB ID: 36792
Pokemon X (what about y?): IGDB ID: 2286
Pokemon XD: Gale of Darkness: IGDB ID: 2724
Pokemon Yellow Version: IGDB ID: 1512
Polybius [2017]: IGDB ID: 24868
Prey [2017]: IGDB ID: 19531
Punch-Out!! [Wii]: IGDB ID: 2194
Ratchet and Clank (name seems to be crashing IGDB API request?): IGDB ID: 1289
Ratchet and Clank: Up Your Arsenal (name seems to be crashing IGDB API request?): IGDB ID: 1773
Rayman GBC: IGDB ID: 85578
Rayman 2: The Great Escape [Dreamcast]: IGDB ID: 193314
Resident Evil 2002: IGDB ID: 24869
Resident Evil 2002 HD REMASTER: IGDB ID: 8254
Resident Evil 2 2019: IGDB ID: 19686
Resident Evil 4 2023: IGDB ID: 132181
The Room [2012]: IGDB ID: 11625
Samurai Showdown 2019: IGDB ID: 109277
Sapiens 2022: IGDB ID: 117186
Shadow of the Colossus [2018]: IGDB ID: 37094
Shadowrun SNES: IGDB ID: 7640
SimCity SNES: IGDB ID: 180001
Singstar 2007 (had in my list that we had a 2008 one?): IGDB ID: 15180
Spider-Man [PlayStation]: IGDB ID: 3603
Stanley Parable [2013] (standalone): IGDB ID: 3035
Star Wars: Battlefront I/II are the originals, Star Wars Battlefront I/II are the EA post-Disney ones
System Shock [2023]: IGDB ID: 18375
Teenage Mutant Ninja Turtles ARCADE: IGDB ID: 3815
Teenage Mutant Ninja Turtles NES: IGDB ID: 86386
Tetris TENGEN: IGDB ID: 180278
Tomb Raider 2013: IGDB ID: 1164 
Tony Hawk's Pro Skater 2 GBA: IGDB ID: 229927
Trials of Mana 2020: IGDB ID: 119391
Twisted Metal [2012]: IGDB ID: 5416
Viva Piñata (the ñ might be throwing off the query?): IGDB ID: 7236
The Walking Dead: The Complete First Season (not matching for some reason?): IGDB ID: 41623
Warcraft II Battle.net edition (name doesn't seem to match?): IGDB ID: 127782
"""