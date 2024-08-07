# import required module
import os
import math
# Writing to an excel sheet using Python
import xlwt
from xlwt import Workbook
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from igdb.wrapper import IGDBWrapper
import json
import pandas
import re

#Store a version of the games database externally so we can refer to it rather than keep having to override it each time?
#Unless we pick a manual option to clear it? option to just update scores based on new lists?
#check to see if already in database before we bother to get info
#Have different phases of external database?
#First phase would be purely the names we grab from lists
#Second phase would be after IGDB information put into it
#we send off the second phase info to mongo, maybe give option just to do only that off of what we already have
#then we pull the mongo info in to a real listed sortable form

#add ability to put comments in text files? ex. jackbox party pack quintpack is actually jackbox party pack 1-6

load_dotenv()
#^To actually populate what we will need from mongo connection

# assign directory
#directory = 'C:\Users\danie\Documents\Top-Game-List-Score-Sorting\GameLists\Ranked'
directory = r'GameLists\Ranked'
#then do unranked and former

#LOOK INTO PANDAS FOR DEALING WITH TABULAR DATA IN PYTHON

#START FLESHING OUT GLITCHWAVE USAGE
    #FILL OUT RATINGS, COLLECTION, PLAYTHROUGHS, ETC.
    #IMPORT REVIEWS
    #START LOOKING AT GENRE (INFLUENCE?), YEAR, PLATFORM, ETC. CHARTS
#SEE IF BACKLOGGD CHARTS COMPARE, IF CAN DO SIMILAR THINGS TO GLITCHWAVE (ALSO LOOK INTO GROUVEE?)

#ONCE CLEARED ALL OF AN UP TO LIST, THEN CONSIDER EXPANDING THE RANGE (LIKE FROM UP TO 100 TO UP TO 150)

"game_DB is a dict of string titles and game object values"
game_DB = {}
#modified_DB is meant to hold modified entries that originally had <> names, and put back into game_DB later
modified_DB = {}
"game object needs two scores"
class GameObject:
    def __init__(self, rank):
        #Add seasonal attribute? Would have to set manually in my own text files?
        self.igdb_ID = None
        self.igdb_found = False
        self.ranked_score = rank
        self.list_count = 1
        self.lists_referencing = []
        self.total_count = 0
        self.completed = False
        self.main_platform = 'None'
        self.list_platforms = []
        self.release_date = 'Unknown' #Can I set this to some date value?
        self.player_counts = []
        self.list_developers = []
        self.list_publishers = []
        self.list_companies = []
        self.genres = []
        self.themes = []

    #consider storing a constantly updated average score?

    def __init__(self, rank, list):
        self.igdb_ID = None
        self.igdb_found = False
        self.ranked_score = rank
        self.list_count = 1
        self.lists_referencing = []
        self.lists_referencing.append(list)
        self.total_count = 0
        self.completed = False
        self.main_platform = 'None'
        self.list_platforms = []
        self.release_date = 'Unknown'  # Can I set this to some date value?
        self.player_counts = []
        self.list_developers = []
        self.list_publishers = []
        self.list_companies = []
        self.genres = []
        self.themes = []

    def __init__(self, rank, list, total):
        self.igdb_ID = None
        self.igdb_found = False
        self.ranked_score = rank
        self.list_count = 1
        self.lists_referencing = []
        self.lists_referencing.append(list)
        self.total_count = total
        self.completed = False
        self.main_platform = 'None'
        self.list_platforms = []
        self.release_date = 'Unknown'
        self.player_counts = []
        self.list_developers = []
        self.list_publishers = []
        self.list_companies = []
        self.genres = []
        self.themes = []

    #CONSIDER MAKING AN EXPORT FUNCTION FOR THE CLASS TO CONVERT TO DICTIONARY?

#Start collecting the lists used in a list, put to a new collection in MongoDB
games_lists = []

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

ranked_file_count = 0
unranked_file_count = 0
former_file_count = 0

"Loop of getting the database information"
#RANKED DIRECTORY
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # Using readlines()
        file1 = open(f, 'r', encoding="utf-8")
        ranked_file_count += 1
        starting_line = file1.readline()
        Lines = file1.readlines()
        #count = int(starting_line)
        count = len(Lines)
        #input('Wait to review\n')
        original_count = count
        # Strips the newline character
        for line in Lines:
            stripped_line = line.strip()
            line = stripped_line
            if stripped_line in game_DB:
                game_DB[line].ranked_score += count
                game_DB[line].list_count += 1
                game_DB[line].lists_referencing.append(f)
                game_DB[line].total_count += original_count
            else:
                newObj = GameObject(count, f, original_count)
                game_DB[line] = newObj
            #searchObj = game_DB.get(newObj, 0) + 1
            #game_DB[line].list_count = game_DB.get(newObj, 0) + 1
            #print("Score of {}: {}".format(count, line.strip()))
            print(f"Score of {count}: {line.strip()}")
            count -= 1
        games_lists.append(filename)

directory = r'GameLists\Unranked'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        # Using readlines()
        file1 = open(f, 'r', encoding="utf-8")
        unranked_file_count += 1
        starting_line = file1.readline()
        Lines = file1.readlines()
        float_count = float(starting_line)
        count = math.floor(float_count)
        count = len(Lines)
        print(count)
        original_count = count
        #do a sum of all numbers in that count
        count = original_count * (original_count + 1) // 2
        #divide the factorial by the original count
        count //= original_count
        print(count)
        print(f)
        #input('Wait to review\n')
        # Strips the newline character
        for line in Lines:
            stripped_line = line.strip()
            line = stripped_line
            if stripped_line in game_DB:
                game_DB[line].ranked_score += count
                game_DB[line].list_count += 1
                game_DB[line].lists_referencing.append(f)
                game_DB[line].total_count += original_count
            else:
                newObj = GameObject(count, f, original_count)
                game_DB[line] = newObj
            #searchObj = game_DB.get(newObj, 0) + 1
            #game_DB[line].list_count = game_DB.get(newObj, 0) + 1
            # print("Score of {}: {}".format(count, line.strip()))
            print(f"Score of {count}: {line.strip()}")
            #count -= 1
        games_lists.append(filename)

directory = r'GameLists\Former'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        # Using readlines()
        # file1 = open(f, 'r')
        file1 = open(f, 'r', encoding="utf-8")
        former_file_count += 1
        starting_line = file1.readline()
        Lines = file1.readlines()
        #count = 1
        count = int(starting_line)
        original_count = count
        #^find out how to read the line amount ahead of time
        #original_count = len(Lines)
        print(original_count)
        # Strips the newline character
        for line in Lines:
            stripped_line = line.strip()
            line = stripped_line
            if stripped_line in game_DB:
                game_DB[line].ranked_score += count
                game_DB[line].list_count += 1
                game_DB[line].lists_referencing.append(f)
                game_DB[line].total_count += original_count
            else:
                newObj = GameObject(count, f, original_count)
                game_DB[line] = newObj
            #searchObj = game_DB.get(newObj, 0) + 1
            #game_DB[line].list_count = game_DB.get(newObj, 0) + 1
            # print("Score of {}: {}".format(count, line.strip()))
            print(f"Score of {count}: {line.strip()}")
            #count -= 1
        games_lists.append(filename)

completeFile = open('Completions.txt', 'r')
completeLines = completeFile.readlines()
for line in completeLines:
    stripped_line = line.strip()
    line = stripped_line
    if line in game_DB:
        game_DB[line].completed = True
    #else: raise error because not in database? create it with 0 score? probably just ignore it?

"""
#ADD SECTION WHERE WE START GRABBING ADDITIONAL ATTRIBUTES FOR GAME DATABASE?
#Purposefully naming this wrong for now so we don't grab from it, only from IGDB for now?
print("Time for attributes!")
attributesFile = open('AdditionalAttributes.txt', 'r')
attributesLines = attributesFile.readlines()
itr = iter(attributesLines)
#for line in attributesLines:
try:
    #if line in game_DB:
    while True:
        #Properly parse through line and indented lines?
        title = next(itr)
        if title in game_DB:
            print(title)
            #main_platform
            attribute = next(itr)
            print(attribute)
            game_DB[title].main_platform = attribute
            #list_platforms
            attribute = next(itr)
            print(attribute)
            game_DB[title].list_platforms = attribute
            #release_date
            attribute = next(itr)
            print(attribute)
            game_DB[title].release_date = attribute
            #player_counts
            attribute = next(itr)
            print(attribute)
            game_DB[title].player_counts = attribute
            #list_developers
            attribute = next(itr)
            print(attribute)
            game_DB[title].list_developers = attribute
            print('')
        #else: supposed to be in database?
except StopIteration:
        pass
"""

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

#Taking custom class objects and making them JSON exportable
export_DB = {}
#export_DB["games"] = []
#export_DB = []

import itertools

for game, details in game_DB.items():
#for game, details in itertools.islice(game_DB.items(),0,3):
    #export_DB[game] = json.loads(details.__dict__)
    export_DB[game] = json.loads(json.dumps(details.__dict__))
    #export_DB["games"].append(json.dumps(details.__dict__))
    #export_string = json.dumps(details.__dict__)
    #export_DB.append(export_string)

print(export_DB)

json_string = ','.join(export_DB)
#json_dict = json.loads(export_DB)
#json_dict = json.loads(json_string)

#Initial print of what we have in the games database
with open ("games_pre.json", "w") as outfile:
    out_json = json.dump(export_DB, outfile)
    #out_json = json.dump(json_dict, outfile)
    #out_json = json.dump(json_string, outfile)
    print(out_json)

import_DB = {}
#import_DB = []
#import_DB["games"] = []

input("Let's test pulling from JSON!\n")

with open("games_pre.json", "r") as json_file:
    #Reading the first character throws everything off
    #import_DB = json.load(json_file)
    #first_char = json_file.read(1)
    #if not first_char:
    if(os.stat("games_pre.json").st_size == 0):
        print("Looks like we don't have anything in games_pre.json yet")
    else:
        import_DB = json.load(json_file)
        #import_DB = json.loads(json_file.read())
        #import_DB = json.loads(json_file)
        #for line in json_file:
            #import_DB.append(json.loads(line))
            #import_DB["games"].append(json.loads(line))
            #import_DB.append(json.loads(line))
        print(import_DB)
        input()

#having issue with jsondecodeerror: extra data, s, end OR str object has no attribute read (load vs. loads)
#seems like putting all into a "games" array doesn't help things

#Make sure fresh for actual process once done testing
import_DB.clear()
export_DB.clear()

#eventually try for functionality where we only update the games that have updated scores? or new games?

with open("games.json") as json_file:
    #first_char = json_file.read(1)
    #if not first_char:
    if (os.stat("games.json").st_size == 0):
        print("Looks like we don't have anything in games.json yet")
    else:
        import_DB = json.load(json_file)
print(import_DB)
print(game_DB.items().__class__)
input()

#This is where the user sets whether they want to grab from the IGDB API or not
#Maybe add options for how much to grab? How many games? What types of info? Other qualifiers?
#Maybe do a quick pass and long pass version? Quick pass doesn't use additional endpoints? Long pass makes more user facing?
igdb_check = False
igdb_answer = None
scratch_answer = False
limit_answer = False
limit_number = 0
while(igdb_check == False):
    print("Would you like to grab additional game data from the IGDB API at this moment? Y or N")
    igdb_answer = input("Make your selection: ")
    if(igdb_answer == 'Y' or igdb_answer == 'Yes'):
        while True:
            print("Would you like to start from scratch? Or only deal with games that don't already have IGDB information?")
            print("1. Start from scratch")
            print("2. Only deal with games without IGDB info already")
            scratch_option = input()
            if(scratch_option == "1"):
                scratch_answer = True
                break
            elif(scratch_option == "2"):
                scratch_answer = False
                break
            else:
                print("Please enter a valid response")
                print()
                continue
        while True:
            print("Would you like to set a limit on how many games to grab info for? This process can take a long time, so this can help get your foot in the door")
            print("1. Set a limit")
            print("2. Just try for all games")
            limit_option = input()
            if (limit_option == "1"):
                limit_answer = True
                while True:
                    print("Would you like to set the limit to? Please provide a valid number")
                    limit_set = input()
                    if(limit_set.isnumeric()):
                        limit_number = int(limit_set)
                        break
                    else:
                        print("Please enter a valid response")
                        print()
                        continue
                break
            elif (limit_option == "2"):
                limit_answer = False
                break
            else:
                print("Please enter a valid response")
                print()
                continue
        # START SCRAPING FOR ATTRIBUTES
        # (Look into close-enough matches that can match when it’s not exact?)
        # (Have the option to replace data manually when database info isn’t good enough or is missing?)
        """
        Most of the requests to the API will use the POST method
        The base URL is: https://api.igdb.com/v4
        You define which endpoint you wish to query by appending /{endpoint name} to the base URL eg. https://api.igdb.com/v4/games
        Include your Client ID and Access Token in the HEADER of your request so that your headers look like the following.
            Client-ID: Client ID
            Authorization: Bearer access_token
        Take special care of the capitalisation. Bearer should be hard-coded infront of your access_token
        You use the BODY of your request to specify the fields you want to retrieve as well as any other filters, sorting etc
    
        Example
        If your Client ID is abcdefg12345 and your access_token is access12345token, a simple request to get information about 10 games would be.
            POST: https://api.igdb.com/v4/games
            Client-ID: abcdefg12345
            Authorization: Bearer access12345token
            Body: "fields *;"
    
        """
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

        # page = requests.get(post) #404
        page = requests.post(post)  # gives access token we can use
        print(page.text)

        # wrapper = IGDBWrapper("YOUR_CLIENT_ID", "YOUR_APP_ACCESS_TOKEN")
        received = json.loads(page.text)
        access_token = received["access_token"]
        print(access_token)
        wrapper = IGDBWrapper(client_id, access_token)

        from igdb.igdbapi_pb2 import GameResult
        from igdb.igdbapi_pb2 import GameModeResult
        from igdb.igdbapi_pb2 import PlatformResult
        from igdb.igdbapi_pb2 import PlatformFamilyResult
        from igdb.igdbapi_pb2 import InvolvedCompanyResult
        from igdb.igdbapi_pb2 import CompanyResult
        from igdb.igdbapi_pb2 import GenreResult
        from igdb.igdbapi_pb2 import ThemeResult

        igdb_request = wrapper.api_request(
            'games.pb',  # Note the '.pb' suffix at the endpoint
             'fields name, rating; limit 5; offset 0;'
            # 'fields name, rating; offset 0;'
        )
        games_message = GameResult()
        games_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
        games = games_message.games
        print(games)
        # input("Here we pause")

        #Figure out if I can be more efficient with endpoints to make it take quicker? taking very long now
        print("Time to go looking around")
        time_speedup = 0;
        #^A feature I'm implementing to cut down how many games parsed through so that we can have an easier first attempt
        for game, details in itertools.islice(game_DB.items(),0,limit_number):
            #if(scratch_answer == False and game in import_DB and details.igdb_found == True):
            if (scratch_answer == False and game in import_DB):
                print("Hey, we already got this one!")
                game_DB[game] = import_DB[game]
                continue
            #Set time speedup back to 0 if want full and accurate database for all items
            #need to set value in both if and elif to work properly
            if(time_speedup < 0):
                print("SKIPPING!!")
                time_speedup += 1
                continue
            elif(time_speedup == 0):
                time_speedup = 0
            check_string = 'fields *; exclude age_ratings, aggregated_rating, aggregated_rating_count, alternative_names, '
            check_string += 'artworks, bundles, checksum, collection, collections, cover, created_at, expanded_games, '
            check_string += 'external_games, follows, franchises, game_localizations, '
            check_string += 'keywords, language_supports, player_perspectives, '
            check_string += 'rating, rating_count, release_dates, screenshots, similar_games, standalone_expansions, '
            check_string += 'storyline, tags, total_rating, total_rating_count, updated_at, videos, websites; '
            # Check if <> comes first, where we use ID instead of name, for titles hard to specify
            #if (game[0] == '<'): #Replacing after discovering startswith() function?
            #poem.startswith('All')
            if(game.startswith('<')):
                print(details)
                print(game.strip())
                #input("Turns out this is a special case!\n")
                game_title = game.strip()
                # pull the ID from the <> part of the string
                check_string += 'where id = '
                # pattern_match = r'<[0-9]+>'
                pattern_match = r'[0-9]+'
                substring = re.findall(pattern_match, game_title)
                title_ID = substring[0]
                #Try to use some info from the substring so we can grab the name of the game better for logging?
                #consider string.replace() function?
                removal = '<' + title_ID + '> '
                #modified_title = game_title.strip(str(substring))
                modified_title = game_title.strip(removal)
                #input(substring)
                #input(modified_title)
                check_string += title_ID
                #Maybe grab the name from IGDB here, to update the name before it gets sent to the cluster?
                #Otherwise it might have <ID> in front of the name there?
                #modified_DB[modified_title] = details
                #input(modified_DB[modified_title])
            else:
                check_string += 'where name = "'
                check_string += game.strip()
                check_string += '"'
            check_string += '; '
            #if (limit_answer):
                #check_string += f'limit {limit_number}; '
            check_string += 'offset 0;'  # 6 is cancelled,  & status != 6
            # Had & version_parent = null in the check_string before, but probably won't work in cases we do want port, might just want
            # more specificity in some cases
            # | category = 3  (attempted to insert this into the query)
            # Category is an enum, 3 means it's a bundle, is | the right way to do an or?
            # Exclude versions that aren't the parent
            # Exclude cancelled, unreleased, TBD versions?
            # Figure out how to deal with children versions? How to give points and pass on points to parent too?
            # Also dealing with compilation games? Add points to individual games? Create field to track subgames in a compilation?
            # check_string += ';'
            print(check_string)
            print(details.lists_referencing)
            igdb_request = wrapper.api_request(
                'games.pb',  # Note the '.pb' suffix at the endpoint
                check_string
            )
            games_message = GameResult()
            games_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            games = games_message.games
            if (len(games) > 1):
                versions_counter = 0
                # print(games[0])
                # earliest_release = int(round(games[0].first_release_date))
                # earliest_release = games[0].first_release_date
                # earliest_release = games[0].first_release_date.to_pydatetime()
                earliest_release = games[0].first_release_date.ToDatetime()
                earliest_game = games[0]
                # print(earliest_release)
                # input("Here is a release!")
                for result in games:
                    # how do I compare timestamps?
                    potential_release = result.first_release_date.ToDatetime()
                    if (potential_release < earliest_release and result.status != 6):
                        # Also check for parent_game field?
                        # print("New earliest release!")
                        # print(result.status)
                        # earliest_release = result.first_release_date
                        earliest_release = potential_release
                        earliest_game = result
                        # input(earliest_release)
                    #print(result)
                # print(earliest_game.slug)
                # print(earliest_game.url)
                # print(earliest_game.id)
                # print(earliest_game.platforms)
                # print(earliest_release)
                # input("Here we pause")
                # Time to put the IGDB attributes into the game we are putting out to the cluster
                game_DB[game].igdb_ID = earliest_game.id
                game_DB[game].igdb_found = True
                #game_DB[game].release_date = earliest_release
                game_DB[game].release_date = earliest_release.isoformat() #To make Json serializable?
                # print("Time to go through platforms")
                # Spin this while loop off into its own function eventually?
                plat_counter = 0
                #plat_counter not defined error?
                main_plat = None
                plat_name = None
                list_plats = []
                #REPLACE THIS WITH A REQUEST THAT LOOKS AT THE ID AND THEN CONSULTS PLATFORMS ENDPOINT?
                while (plat_counter < len(earliest_game.platforms)):
                    #plat_next = plat_counter + 1
                    plat_ID = earliest_game.platforms[plat_counter]
                    # print(plat_ID)
                    # print(plat_ID.value)
                    # print(plat_ID.id)
                    # match plat_ID:
                    sub_query = 'fields name; where id=' + str(plat_ID.id) + ';'
                    sub_request = wrapper.api_request(
                        'platforms.pb',  # Note the '.pb' suffix at the endpoint
                        sub_query
                    )
                    platforms_message = PlatformResult()
                    platforms_message.ParseFromString(
                        sub_request)  # Fills the protobuf message object with the response
                    platforms = platforms_message.platforms
                    #input(platforms)
                    plat_name = platforms[0].name
                    if (plat_counter == 0):
                        main_plat = plat_name
                    # print(plat_name)
                    list_plats.append(plat_name)
                    """
                    sub_query = 'fields name; where id=' + str(plat_ID.platform_family) + ';'
                    sub_request = wrapper.api_request(
                        'platform_families.pb',  # Note the '.pb' suffix at the endpoint
                        sub_query
                    )
                    platforms_message = PlatformFamilyModeResult()
                    platforms_message.ParseFromString(sub_request)  # Fills the protobuf message object with the response
                    platformfamilies = platforms_message.platformfamilies
                    input(platformfamilies)
                    """
                    plat_counter += 1
                # input("There they are!")
                # game_DB[game].main_platform = earliest_game.platforms[0]
                game_DB[game].main_platform = main_plat  # Will this always pull best choice?
                #^Seriously consider revising this to pull the first format with the earliest release date
                #Because platform ID's are overruling too much (ex. wii is an early ID so overrides earlier releases)
                # game_DB[game].list_platforms = earliest_game.platforms
                if(len(list_plats) > 0):
                    game_DB[game].list_platforms = list_plats  # Will only pull ID's for now, need to tackle later?
                modes = earliest_game.game_modes
                #input(modes)
                if(len(modes) > 0):
                    for mode in modes:
                        mode_type = None
                        #input(mode)
                        #sub_query = 'fields *;'
                        sub_query = 'fields name; where id=' + str(mode.id) + ';'
                        sub_request = wrapper.api_request(
                            'game_modes.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query
                        )
                        modes_message = GameModeResult()
                        modes_message.ParseFromString(sub_request)  # Fills the protobuf message object with the response
                        new_modes = modes_message.gamemodes
                        #print(new_modes)
                        mode_type = new_modes[0].name
                        game_DB[game].player_counts.append(mode_type)
                        #input(mode_type)
                    #game_DB[game].player_counts = modes # Changes approach but for the better?
                # ^Also consider multiplayer_modes? (they use more of a boolean/integer approach?)
                developers = earliest_game.involved_companies
                #^consider a check for developer boolean? porting? supporting?
                #do we count publishers?
                #consider more categories for game objects later like publishers
                #input(developers)
                #print(developers)
                if(len(developers) > 0):
                    for dev in developers:
                        dev_name = None
                        #input(dev)
                        #FIX THE REST OF THIS!!! (involved company, company?)
                        #first query to look at involved companies
                        #sub_query = 'fields *;'
                        #sub_query_1 = 'fields *; where id=' + str(dev.id) + ' & developer=true;'
                        sub_query_1 = 'fields *; where id=' + str(dev.id) + ';'
                        sub_request_1 = wrapper.api_request(
                            'involved_companies.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query_1
                        )
                        inv_companies_message = InvolvedCompanyResult()
                        inv_companies_message.ParseFromString(sub_request_1)  # Fills the protobuf message object with the response
                        inv_companies = inv_companies_message.involvedcompanies
                        #print(inv_companies)
                        #print(len(inv_companies))
                        if(len(inv_companies) == 0):
                            continue
                        #second query to look at the company specifically
                        is_dev = inv_companies[0].developer
                        print(is_dev)
                        is_pub = inv_companies[0].publisher
                        print(is_pub)
                        sub_query_2 = 'fields name; where id=' + str(inv_companies[0].company.id) + ';'
                        sub_request_2 = wrapper.api_request(
                            'companies.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query_2
                        )
                        companies_message = CompanyResult()
                        companies_message.ParseFromString(sub_request_2)  # Fills the protobuf message object with the response
                        companies = companies_message.companies
                        #print(companies)
                        dev_name = companies[0].name
                        game_DB[game].list_companies.append(dev_name)
                        #if dev true: add to devs
                        #if pub true: add to pubs
                        #also consider supporting boolean in addition to developer and publisher? porting?
                        if(is_dev):
                            game_DB[game].list_developers.append(dev_name)
                        if (is_pub):
                            game_DB[game].list_publishers.append(dev_name)
                        #input(dev_name)
                    # game_DB[game].list_developers = developers  # Will this grab the most definitive list?
                #ADD GENRES
                genres = earliest_game.genres
                if (len(genres) > 0):
                    for genre in genres:
                        genre_type = None
                        sub_query = 'fields name; where id=' + str(genre.id) + ';'
                        sub_request = wrapper.api_request(
                            'genres.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query
                        )
                        genres_message = GenreResult()
                        genres_message.ParseFromString(sub_request)  # Fills the protobuf message object with the response
                        new_genres = genres_message.genres
                        genre_type = new_genres[0].name
                        game_DB[game].genres.append(genre_type)
                        #input(genre_type)
                #ADD THEMES
                themes = earliest_game.themes
                if (len(themes) > 0):
                    for theme in themes:
                        theme_type = None
                        sub_query = 'fields name; where id=' + str(theme.id) + ';'
                        sub_request = wrapper.api_request(
                            'themes.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query
                        )
                        themes_message = ThemeResult()
                        themes_message.ParseFromString(
                            sub_request)  # Fills the protobuf message object with the response
                        new_themes = themes_message.themes
                        theme_type = new_themes[0].name
                        game_DB[game].themes.append(theme_type)
                        #input(theme_type)
            elif (len(games) == 1):
                try:
                    current_game = games[0]
                    try:
                        game_DB[game].igdb_ID = current_game.id
                    except IndexError as e:
                        print("Error:", e)
                        #print("Index", i, "is out of range")
                    game_DB[game].igdb_found = True
                    #game_DB[game].release_date = current_game.first_release_date.ToDatetime()
                    game_DB[game].release_date = current_game.first_release_date.ToDatetime().isoformat() #To make JSON serializable?

                    #this version gave animal crossing: new horizons switch and n64
                    #current approach giving that game nothing for platforms?
                    """
                    plat_ID = current_game.platforms[0]
                    plat_name = None
                    sub_query = 'fields name; where id=' + str(plat_ID.id) + ';'
                    sub_request = wrapper.api_request(
                        'platforms.pb',  # Note the '.pb' suffix at the endpoint
                        sub_query
                    )
                    platforms_message = PlatformResult()
                    platforms_message.ParseFromString(sub_request)  # Fills the protobuf message object with the response
                    platforms = platforms_message.platforms
                    plat_name = platforms[0].name
                    if (plat_counter == 0):
                        main_plat = plat_name
                    # print(plat_name)
                    list_plats.append(plat_name)
                    game_DB[game].main_platform = plat_name
                    list_plats = []
                    list_plats.append(plat_name)
                    game_DB[game].list_platforms = list_plats  # Will only pull ID's for now, need to tackle later?
                    """
                    #PASTED FROM ABOVE WITHOUT COMMENTS
                    plat_counter = 0
                    main_plat = None
                    plat_name = None
                    list_plats = []
                    #input(current_game.platforms)
                    while (plat_counter < len(current_game.platforms)):
                        plat_ID = current_game.platforms[plat_counter]
                        sub_query = 'fields name; where id=' + str(plat_ID.id) + ';'
                        sub_request = wrapper.api_request(
                            'platforms.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query
                        )
                        platforms_message = PlatformResult()
                        platforms_message.ParseFromString(sub_request)  # Fills the protobuf message object with the response
                        platforms = platforms_message.platforms
                        plat_name = platforms[0].name
                        if (plat_counter == 0):
                            main_plat = plat_name
                        list_plats.append(plat_name)
                        plat_counter += 1
                    game_DB[game].main_platform = main_plat
                    if (len(list_plats) > 0):
                        game_DB[game].list_platforms = list_plats

                    modes = current_game.game_modes
                    if (len(modes) > 0):
                        for mode in modes:
                            mode_type = None
                            # input(mode)
                            # sub_query = 'fields *;'
                            sub_query = 'fields name; where id=' + str(mode.id) + ';'
                            sub_request = wrapper.api_request(
                                'game_modes.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query
                            )
                            modes_message = GameModeResult()
                            modes_message.ParseFromString(
                                sub_request)  # Fills the protobuf message object with the response
                            new_modes = modes_message.gamemodes
                            mode_type = new_modes[0].name
                            game_DB[game].player_counts.append(mode_type)
                            # input(mode_type)
                        # game_DB[game].player_counts = modes # Changes approach but for the better?
                    # ^Also consider multiplayer_modes? (they use more of a boolean/integer approach?)
                    developers = current_game.involved_companies
                    #print(developers)
                    if (len(developers) > 0):
                        for dev in developers:
                            dev_name = None
                            # FIX THE REST OF THIS!!! (involved company, company?)
                            # first query to look at involved companies
                            # sub_query = 'fields *;'
                            #sub_query_1 = 'fields *; where id=' + str(dev.id) + ' & developer=true;'
                            sub_query_1 = 'fields *; where id=' + str(dev.id) + ';'
                            sub_request_1 = wrapper.api_request(
                                'involved_companies.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query_1
                            )
                            inv_companies_message = InvolvedCompanyResult()
                            inv_companies_message.ParseFromString(
                                sub_request_1)  # Fills the protobuf message object with the response
                            inv_companies = inv_companies_message.involvedcompanies
                            #print(inv_companies)
                            #print(len(inv_companies))
                            if (len(inv_companies) == 0):
                                continue
                            # second query to look at the company specifically
                            is_dev = inv_companies[0].developer
                            print(is_dev)
                            is_pub = inv_companies[0].publisher
                            print(is_pub)
                            sub_query_2 = 'fields name; where id=' + str(inv_companies[0].company.id) + ';'
                            sub_request_2 = wrapper.api_request(
                                'companies.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query_2
                            )
                            companies_message = CompanyResult()
                            companies_message.ParseFromString(
                                sub_request_2)  # Fills the protobuf message object with the response
                            companies = companies_message.companies
                            dev_name = companies[0].name
                            game_DB[game].list_companies.append(dev_name)
                            if (is_dev):
                                game_DB[game].list_developers.append(dev_name)
                            if (is_pub):
                                game_DB[game].list_publishers.append(dev_name)
                    # ADD GENRES
                    #genre seems to be pulling in too many results right now, unrelated?
                    genres = earliest_game.genres
                    if (len(genres) > 0):
                        for genre in genres:
                            genre_type = None
                            sub_query = 'fields name; where id=' + str(genre.id) + ';'
                            sub_request = wrapper.api_request(
                                'genres.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query
                            )
                            genres_message = GenreResult()
                            genres_message.ParseFromString(sub_request)  # Fills the protobuf message object with the response
                            new_genres = genres_message.genres
                            genre_type = new_genres[0].name
                            game_DB[game].genres.append(genre_type)
                            #input(genre_type)
                    # ADD THEMES
                    #theme seems to be pulling in too many results right now, unrelated?
                    themes = earliest_game.themes
                    if (len(themes) > 0):
                        for theme in themes:
                            theme_type = None
                            sub_query = 'fields name; where id=' + str(theme.id) + ';'
                            sub_request = wrapper.api_request(
                                'themes.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query
                            )
                            themes_message = ThemeResult()
                            themes_message.ParseFromString(sub_request)  # Fills the protobuf message object with the response
                            new_themes = themes_message.themes
                            theme_type = new_themes[0].name
                            game_DB[game].themes.append(theme_type)
                            #input(theme_type)
                except Exception as e:
                    print("An error has occurred:", e)
                    #it starts hitting errors when it gets to some of the new games featured in metacritic user scores?
            else:
                # print(result)
                print("Not found with that name!")
                input("Maybe you need to alter the title somehow?\n")

        # When there is ID confusion, need to clarify ID when putting entries
        # Have a process that runs through when generating databases and pauses
        # when there are multiple options, so we can try to narrow down on that title
        # Use <> to contain ID number (from IGDB database)
        # Example: The ID we want to use for Super Mario World is 1070
        # retitle: a link to the past and other zelda games
        # ID for Final Fantasy VII: 427
        # ID for Ms. Pac-Man: 7452
        # investigate ways to test for what is the most parent version?
        # when multiple options to go with, for now go with the one that has
        # the most total_rating_count? earliest release date?

        # For now, Pokemon versions need to pick one over the other,for simplicity we go for the one that tends to be listed first
        # Pokémon Red Version seems to break the api request, probably the accented e
        # Doesn't get found with the title "Pokemon Red Version" either though
        # exit()

        """
        MEDIUM EXAMPLE:
        URL = 'https://www.bookdepository.com/top-new-releases'
        page = requests.get(URL)
        soup = BeautiulSoup(page.content, "html.parser")
        books = soup.find_all("div", class_ = "book-item")
        """
        igdb_check = True
    elif(igdb_answer == 'N' or igdb_answer == 'No'):
        print("Understood, skipping to next step.")
        igdb_check = True
    else:
        print("Answer not understood, try again.")
        print()

print(game_DB.items().__class__)
for game, details in itertools.islice(game_DB.items(),0,3):
    print(game)
    print(details)
    print(details.__class__)

#Once we've gotten the IGDB data we need, print it out to a JSON file to store long term
for game, details in game_DB.items():
    if(isinstance(details, str)):
        #if already made a json string
        if (details.igdb_found == False):
            print("Nothing found for this yet (string)")
            continue
        else:
            export_DB[game] = json.loads(details)  # Now it's already json formatted
    elif(isinstance(details, dict)):
        if (details['igdb_found'] == False):
            print("Nothing found for this yet (dict)")
            continue
        else:
            export_DB[game] = json.loads(json.dumps(details))
    else:
    #export_DB[game] = json.dumps(details.__dict__)
        if (details.igdb_found == False):
            print("Nothing found for this yet (other)")
            continue
        else:
            export_DB[game] = json.loads(json.dumps(details.__dict__))

with open ("games.json", "w") as outfile:
    json.dump(export_DB, outfile)

print("Games exported to games.json!")

#START USING PYMONGO FOR OUTPUTTING TO MONGODB DATABASE
#Used code sample from Atlas on how to connect with Pymongo for assistance here
#Connecting to env file to get private login data
mon_connect = os.getenv('MONGO_URI')
mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
monDB = mon_client["GameSorting"]
#input(mon_connect)
input("About to attempt connection to Mongo, press ENTER when you are ready")
try:
    mon_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
mon_col = monDB["games"]
list_col = monDB["lists"]

#Create index on title so can do partial title searching, don't mark as unique because some titles won't be
mon_col.create_index('Title')

#INSERT ALL GAMES INTO DATABASE
#Clear database to begin with?
while True:
    print("Would you like to clear the database to start? Y or N")
    clear_option = input()
    if(clear_option == "Y" or clear_option == "y"):
        print("Ok, clearing the game and list collections")
        mon_col.drop()
        list_col.drop()
        break
    elif (clear_option == "N" or clear_option == "n"):
        print("Ok, leaving it as is")
        break
    else:
        print("I'm sorry, I don't understand. Please enter valid input")
        continue
mongo_limit = len(game_DB.items())
while True:
    print("Would you like to set a limit on how many records to put into Mongo?")
    print("1. Same limit as for IGDB pulling")
    print("2. New set limit")
    print("3. No limit")
    mongo_option = input()
    if(mongo_option == '1'):
        mongo_limit = limit_number
        break
    elif(mongo_option == '2'):
        print("Set your limit here")
        #add input verification
        mongo_limit = input()
        break
    elif (mongo_option == '3'):
        break
    else:
        print("I'm sorry, I don't understand. Please enter valid input")
        continue
#export = []
print("INSERTING INTO MONGODB!")
for game, details in itertools.islice(game_DB.items(),0,mongo_limit):
    print(game_DB.items().__class__)
    print(details.__class__)
    #If they're all from scratch, details is a gameobject, otherwise it's a dict
    if(isinstance(details, GameObject)):
        print("This one's a game object!")
        details = json.loads(json.dumps(details.__dict__))
    print(details.__class__)
    #insertion = mon_col.insert_one(details)
    #insertion = mon_col.insert_one(game_DB[game])
    #export.append(details)
    export_dict = {}
    if (game.startswith('<')):
        #If I successfully improve how titles get put out to mongo cluster, make the IGDB ID the key I use there for ID
        print(game)
        pattern_match = r'[0-9]+'
        substring = re.findall(pattern_match, game)
        title_ID = substring[0]
        removal = '<' + title_ID + '> '
        modified_title = game.strip(removal)
        #input(modified_title)
        export_dict["Title"] = modified_title
    else:
        export_dict["Title"] = game
    #export_dict["IGDB ID"] = details.igdb_ID
    export_dict["IGDB ID"] = details['igdb_ID']
    #export_dict["Ranked Score"] = details.ranked_score
    export_dict["Ranked Score"] = details['ranked_score']
    #export_dict["Inclusion Score"] = details.list_count
    export_dict["Inclusion Score"] = details['list_count']
    #average_score = details.ranked_score / details.total_count
    average_score = details['ranked_score'] / details['total_count']
    export_dict["Average Score"] = average_score
    #export_dict["List of References"] = details.lists_referencing
    export_dict["List of References"] = details['lists_referencing']
    #export_dict["Completed"] = details.completed
    export_dict["Completed"] = details['completed']
    #export_dict["Main Platform"] = details.main_platform
    export_dict["Main Platform"] = details['main_platform']
    #export_dict["List of Platforms"] = details.list_platforms
    export_dict["List of Platforms"] = details['list_platforms']
    #export_dict["Release Date"] = details.release_date
    export_dict["Release Date"] = details['release_date']
    #export_dict["Player Counts"] = details.player_counts
    export_dict["Player Counts"] = details['player_counts']
    #export_dict["Developers"] = details.list_developers
    export_dict["Developers"] = details['list_developers']
    #export_dict["Publishers"] = details.list_publishers
    export_dict["Publishers"] = details['list_publishers']
    #export_dict["Companies"] = details.list_companies
    export_dict["Companies"] = details['list_companies']
    #export_dict["Genres"] = details.genres
    export_dict["Genres"] = details['genres']
    #export_dict["Themes"] = details.themes
    export_dict["Themes"] = details['themes']
    #export_dict["Total Count"] = details.total_count
    export_dict["Total Count"] = details['total_count']
    #export_dict = dict(game)
    #^need to expand and clarify more?
    #export_dict = dict('Title' = game, 'IGDB ID' = details.igdb_ID, 'Ranked Score' = details.ranked_score)
    #print(export_dict)
    insertion = mon_col.insert_one(export_dict)
#insertion = mon_col.insert_many(game_DB)
#insertion = mon_col.insert_many(export)
print("TIME TO INSERT THE LISTS INTO MONGODB!")
for list in games_lists:
    # could keep track of what type of list it is, other variables?
    #list_dict = {}
    #list_dict["Title"] = list
    list_dict = dict(Title = list)
    print(list_dict)
    list_insert = list_col.insert_one(list_dict)
    #list_dict["Title"].append(list)

#after printed out everything to excel, then make three printed sorted lists?
#each time, sort excel a certain way, then print out excel factors to list?

#further sort by keys after sorted by values?

#print totals of the numbers of lists in each category?

#Files to mark additional personal statuses of games so far:
#Completed

print(f"Ranked Lists: {ranked_file_count}")
print(f"Unranked Lists: {unranked_file_count}")
print(f"Former Lists: {former_file_count}")

print("LISTS USED IN PROCESS:")
for list in games_lists:
    print(list)

print()
print("Time to grab the games from the database!")
games_pulled = mon_col.find()
games_pulled_ranked = mon_col.find().sort("Ranked Score", -1)
games_pulled_inclusion = mon_col.find().sort("Inclusion Score", -1)
games_pulled_average = mon_col.find().sort("Average Score", -1)

#Opening the files that we are going to be writing to
file_ranked = open("Sorted by Ranked.txt","w", encoding="utf-8")
file_inclusion = open("Sorted by Inclusion.txt","w", encoding="utf-8")
file_average = open("Sorted by Average.txt","w", encoding="utf-8")
file_ranked_uncompleted = open("Sorted by Ranked (Uncompleted).txt", "w", encoding="utf-8")
file_inclusion_uncompleted = open("Sorted by Inclusion (Uncompleted).txt","w", encoding="utf-8")
file_average_uncompleted = open("Sorted by Average (Uncompleted).txt","w", encoding="utf-8")

for game in games_pulled_ranked:
    #print(game)

    entry = ""
    completed = game["Completed"]
    if (completed == True):
        entry += "[x]"
    """
    entry += game['Title'].strip()
    entry += " --> "
    entry += str(game['Ranked Score'])
    """
    print(game['Title'])
    print(game['Ranked Score'])
    entry += game['Title'].strip()
    if (igdb_answer == 'Y' or igdb_answer == 'Yes'):
        #Needed while we are using timespeedup
        if(game['IGDB ID'] != None):
            entry += " [IGDB ID: " + str(game['IGDB ID']) + "]"
    entry += " --> " + str(game['Ranked Score'])
    file_ranked.write(entry)
    file_ranked.write("\n")
    if (completed == False):
        file_ranked_uncompleted.write(entry)
        file_ranked_uncompleted.write("\n")

for game in games_pulled_inclusion:
    entry = ""
    completed = game["Completed"]
    if (completed == True):
        entry += "[x]"
    entry += game['Title'].strip()
    if (igdb_answer == 'Y' or igdb_answer == 'Yes'):
        # Needed while we are using timespeedup
        if (game['IGDB ID'] != None):
            entry += " [IGDB ID: " + str(game['IGDB ID']) + "]"
    entry += " --> " + str(game['Inclusion Score'])
    file_inclusion.write(entry)
    file_inclusion.write("\n")
    if (completed == False):
        file_inclusion_uncompleted.write(entry)
        file_inclusion_uncompleted.write("\n")

for game in games_pulled_average:
    entry = ""
    completed = game["Completed"]
    if (completed == True):
        entry += "[x]"
    entry += game['Title'].strip()
    if (igdb_answer == 'Y' or igdb_answer == 'Yes'):
        # Needed while we are using timespeedup
        if (game['IGDB ID'] != None):
            entry += " [IGDB ID: " + str(game['IGDB ID']) + "]"
    entry += " --> " + str(game['Average Score'])
    file_average.write(entry)
    file_average.write("\n")
    if (completed == False):
        file_average_uncompleted.write(entry)
        file_average_uncompleted.write("\n")

#Writing to excel using new approach from MongoDB Atlas
bold_style = xlwt.easyxf('font: bold 1;')
crossed_style = xlwt.easyxf('font: struck_out 1;')
sheet1.write(0, 0, 'TITLE', bold_style)
sheet1.write(0, 1, 'IGDB ID', bold_style)
sheet1.write(0, 2, 'RANKED SCORE', bold_style)
sheet1.write(0, 3, 'INCLUSION SCORE', bold_style)
sheet1.write(0, 4, 'AVERAGE SCORE', bold_style)
sheet1.write(0, 5, 'LISTS INCLUDED ON', bold_style)
sheet1.write(0, 6, 'COMPLETED', bold_style)
sheet1.write(0, 7, 'MAIN PLATFORM', bold_style)
sheet1.write(0, 8, 'LIST OF PLATFORMS', bold_style)
sheet1.write(0, 9, 'RELEASE DATE', bold_style)
sheet1.write(0, 10, 'PLAYER COUNTS', bold_style)
sheet1.write(0, 11, 'DEVELOPERS', bold_style)
sheet1.write(0, 12, 'PUBLISHERS', bold_style)
sheet1.write(0, 13, 'COMPANIES', bold_style)
sheet1.write(0, 14, 'GENRES', bold_style)
sheet1.write(0, 15, 'THEMES', bold_style)
excel_count = 1
for game in games_pulled:
    ranked_score = game['Ranked Score']
    inclusion_score = game['Inclusion Score']
    average_score = ranked_score / game['Total Count']
    completion_status = game['Completed']
    #if(game['Completed'] == True):
    if (completion_status == True):
        sheet1.write(excel_count, 0, game['Title'], crossed_style)
    else:
        sheet1.write(excel_count, 0, game['Title'])
    if (igdb_answer == 'Y' or igdb_answer == 'Yes'):
        # Needed while we are using timespeedup
        if (game['IGDB ID'] != None):
            sheet1.write(excel_count, 1, game['IGDB ID'])
    sheet1.write(excel_count, 2, ranked_score)
    sheet1.write(excel_count, 3, inclusion_score)
    sheet1.write(excel_count, 4, average_score)
    """
    #Replacing this approach with the newly discovered join() approach?
    output_lists = ""
    for ref_list in game['List of References']:
        output_lists += ref_list
        output_lists += ", "
    """
    output_lists = ', '.join(game['List of References'])
    sheet1.write(excel_count, 5, output_lists)
    sheet1.write(excel_count, 6, completion_status)
    #sheet1.write(excel_count, 5, game['Main Platform'].strip())
    sheet1.write(excel_count, 7, game['Main Platform'])
    #Create a loop to deal with printing the platforms in a comma approach
    """
    game_platforms = game['List of Platforms']
    #print(game_platforms)
    #print(len(game_platforms))
    #input("Here are the number of platforms")
    platforms_string = ""
    plat_next = 1
    #Replacing this approach with the newly discovered join() approach?
    for platform in game_platforms:
        platforms_string += platform
        if(plat_next < len(game_platforms)):
            platforms_string += ", "
        plat_next += 1
    """
    platforms_string = ', '.join(game['List of Platforms'])
    #sheet1.write(excel_count, 6, game['List of Platforms'])
    sheet1.write(excel_count, 8, platforms_string)
    #sheet1.write(excel_count, 7, game['Release Date'].strip())
    #^Try to strip escape chars out earlier or the items themselves
    sheet1.write(excel_count, 9, game['Release Date'])
    players_string = ', '.join(game['Player Counts'])
    #sheet1.write(excel_count, 8, game['Player Counts'])
    sheet1.write(excel_count, 10, players_string)
    devs_string = ', '.join(game['Developers'])
    sheet1.write(excel_count, 11, devs_string)
    pubs_string = ', '.join(game['Publishers'])
    sheet1.write(excel_count, 12, pubs_string)
    comps_string = ', '.join(game['Companies'])
    sheet1.write(excel_count, 13, comps_string)
    genres_string = ', '.join(game['Genres'])
    sheet1.write(excel_count, 14, genres_string)
    themes_string = ', '.join(game['Themes'])
    sheet1.write(excel_count, 15, themes_string)
    excel_count += 1
wb.save('Sorted Database.xls')

games_pulled = mon_col.find().limit(5)
for game in games_pulled:
    print("Here is a game")
    print(game)
    if(game["Main Platform"] == "Wii"):
        print("We found one!")
        print(game)
    print()

#Close connection to open up socket (seemed to cause problems when running generator then trying printreports?)
mon_client.close()
#Close cursors too?
games_pulled.close()
games_pulled_ranked.close()
games_pulled_average.close()
games_pulled_inclusion.close()

print("Successfully completed! Have a good day!")

""""
REFERENCES:
Iterate over files in directory: https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
Python dictionaries: https://www.w3schools.com/python/python_dictionaries.asp
https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
https://www.geeksforgeeks.org/convert-string-to-integer-in-python/
https://www.geeksforgeeks.org/python-initializing-dictionary-with-empty-lists/
https://linuxhint.com/initialize-dictionary-python/#:~:text=Another%20way%20to%20initialize%20a,print%20out%20the%20initialized%20dictionary.
https://www.geeksforgeeks.org/writing-excel-sheet-using-python/
https://stackoverflow.com/questions/9848299/importerror-no-module-named-xlwt
https://www.geeksforgeeks.org/python-increment-value-in-dictionary/
https://www.educative.io/answers/how-to-check-if-a-key-exists-in-a-python-dictionary
Factorial in python: https://www.geeksforgeeks.org/factorial-in-python/
https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file
https://kodify.net/python/math/round-integers/
https://stackoverflow.com/questions/27946595/how-to-manage-division-of-huge-numbers-in-python
Adding strings in Python: https://www.geeksforgeeks.org/python-add-one-string-to-another/
Counting the number of lines in file: https://pynative.com/python-count-number-of-lines-in-file/
https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
https://www.geeksforgeeks.org/reading-writing-text-files-python/
Converting integer to string in Python: https://www.geeksforgeeks.org/convert-integer-to-string-in-python/
Removing newline character from string in Python: https://www.geeksforgeeks.org/python-removing-newline-character-from-string/
https://github.com/python-excel/xlwt/blob/master/xlwt/Style.py
https://www.digitalocean.com/community/tutorials/python-wait-time-wait-for-input
https://www.tutorialspoint.com/sqlite/sqlite_python.htm
https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
Pymongo Tutorial: https://www.w3schools.com/python/python_mongodb_getstarted.asp
Mongodb Tutorial: https://www.w3schools.com/mongodb/mongodb_get_started.php
Add to a list: https://www.w3schools.com/python/python_lists_add.asp
How to keep sensitive data safe in an ENV file: https://forum.freecodecamp.org/t/how-to-store-a-mongodb-username-and-password-persistently-using-dotenv/50994
How to setup ENV file to work with Python: https://configu.com/blog/using-py-dotenv-python-dotenv-package-to-manage-env-variables/
Pre-commit safety: https://docs.gitguardian.com/ggshield-docs/integrations/git-hooks/pre-commit?utm_source=product&utm_medium=GitHub_checks&utm_campaign=check_run
Fix for UnicodeEncodeError after pre-commit safety integration: https://github.com/mwouts/jupytext/issues/770
Python Requests post: https://www.w3schools.com/python/ref_requests_post.asp
Python IGDB API Wrapper: https://github.com/twitchtv/igdb-api-python
Reading JSON files in python: https://www.geeksforgeeks.org/read-json-file-using-python/
Converting datetime to integer timestamp: https://www.geeksforgeeks.org/python-datetime-to-integer-timestamp/
Converting Pandas timestamp to python datetime: https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.to_pydatetime.html#pandas.Timestamp.to_pydatetime
Switch statement equivalent in Python: https://www.geeksforgeeks.org/switch-case-in-python-replacement/
Substringing a string in Python: https://www.geeksforgeeks.org/how-to-substring-a-string-in-python/
Regex Python: https://www.geeksforgeeks.org/python-regex-re-search-vs-re-findall/
Closing pymongo connection: https://stackoverflow.com/questions/18401015/how-to-close-a-mongodb-python-connection
Close cursors, try 'with' connections: https://www.mongodb.com/community/forums/t/i-am-using-pymongo-do-i-have-to-close-a-mongoclient-after-use/213511
Dealing with out of index in list errors: https://rollbar.com/blog/how-to-fix-python-list-index-out-of-range-error-in-for-loops/#
Python dict() function: https://www.w3schools.com/python/ref_func_dict.asp
Converting Python dictionary to JSON: https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
Converting class object to JSON: https://www.geeksforgeeks.org/convert-class-object-to-json-in-python/#
Solve JSON Type error: https://stackoverflow.com/questions/69270727/how-to-solve-typeerror-the-json-object-must-be-str-bytes-or-bytearray-not-t
Check if text file empty: https://www.geeksforgeeks.org/check-if-a-text-file-empty-in-python/
JSON Decode error, how to handle more than one JSON object imported: https://stackoverflow.com/questions/21058935/python-json-loads-shows-valueerror-extra-data
Dealing with JSON Decode error: https://stackoverflow.com/questions/48140858/json-decoder-jsondecodeerror-extra-data-line-2-column-1-char-190
Check if file is empty: https://stackoverflow.com/questions/2507808/how-to-check-whether-a-file-is-empty-or-not
Limiting iterations of loop: https://stackoverflow.com/questions/36106712/how-can-i-limit-iterations-of-a-loop
Creating index in Pymongo: https://www.geeksforgeeks.org/how-to-create-index-for-mongodb-collection-using-python/#
"""