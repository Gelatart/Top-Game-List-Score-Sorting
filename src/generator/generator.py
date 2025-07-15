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
import datetime

import sqlite3

from .config import check_for_src, get_env_var
from .game_object import GameObject
from .file_loader import ListType, get_files_in_dir, read_game_list, read_attributed_games
from .database_interface import DatabaseInterface

load_dotenv()
#^To actually populate what we will need from mongo connection

#Make a function to append to file names based on src? To add ..\ if they need to go back up on directory
"""
def check_for_src(potential_filename):
    cwd = os.getcwd()
    #input("We are currently in " + cwd)
    if_src = cwd[-3:]
    #input(if_src)
    if(if_src == "src"):
        potential_filename = "..\\" + potential_filename
    return potential_filename
"""

def mongo_connect():
    #Replace the part where this originally happened later in the code with this function?
    #mon_connect = os.getenv('MONGO_URI')
    mon_connect = get_env_var('MONGO_URI')
    mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
    monDB = mon_client["GameSorting"]
    #^Have this part happen before the function actually goes?
    connect_message = ""
    try:
        mon_client.admin.command('ping')
        connect_message = "Pinged your deployment. You successfully connected to MongoDB!"
        #print("Pinged your deployment. You successfully connected to MongoDB!")
        print(connect_message)
    except Exception as e:
        print(e)
        connect_message = e
    return connect_message

def load_list(files, file_count, game_DB, games_lists, type: ListType):
    """
    Function for loading and processing different directories of lists, rather than rewriting the logic multiple times slightly differently
    """
    #Do I make some of these variables global? Declared outside any specific functions?
    for filepath in files:
        file_count += 1
        for title, score, total in read_game_list(filepath, type):
            if title not in game_DB:
                game_DB[title] = GameObject(title, ranked_score=score, list_source=filepath, total_count=total)
            else:
                game = game_DB[title]
                game.ranked_score += score
                game.total_count += total
                game.list_count += 1
                game.lists_referencing.append(filepath)
            print(f"Score of {score}: {title}")
        games_lists.append(filepath)

def run_generator():
    """
    The main logic of the generator function, that calls other functions from other files
    """

    "game_DB is a dict of string titles and game object values"
    game_DB = {}
    "modified_DB is meant to hold modified entries that originally had <> names, and put back into game_DB later"
    modified_DB = {}

    "Start collecting the lists used in a list, put to a new collection in MongoDB"
    #Find way to track what type of list it is?
    games_lists = []

    completed_titles = set(read_attributed_games("game_lists\Completions.txt"))

    ranked_file_count = 0
    unranked_file_count = 0
    former_file_count = 0

    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')

    # Step 1: Load and process ranked lists
    ranked_files = get_files_in_dir("game_lists/ranked")
    for filepath in ranked_files:
        ranked_file_count += 1
        for title, score, total in read_game_list(filepath, ListType.RANKED):
            game = game_DB.get(title)
            if not game:
                game = GameObject(game, ranked_score=score, list_source=filepath, total_count=total)
                game_DB[title] = game
            else:
                game.ranked_score += score
                game.total_count += total
                game.list_count += 1
                game.lists_referencing.append(filepath)
            print(f"Score of {score}: {title}")
        games_lists.append(filepath)

    # Step 2: Load and process unranked lists
    unranked_files = get_files_in_dir("game_lists/unranked")
    for filepath in unranked_files:
        unranked_file_count += 1
        for title, score, total in read_game_list(filepath, ListType.UNRANKED):
            game = game_DB.get(title)
            if not game:
                game = GameObject(game, ranked_score=score, list_source=filepath, total_count=total)
                game_DB[title] = game
            else:
                game.ranked_score += score
                game.total_count += total
                game.list_count += 1
                game.lists_referencing.append(filepath)
            print(f"Score of {score}: {title}")
        games_lists.append(filepath)

    # Step 3: Load and process former lists
    former_files = get_files_in_dir("game_lists/former")
    for filepath in former_files:
        former_file_count += 1
        for title, score, total in read_game_list(filepath, ListType.FORMER):
            game = game_DB.get(title)
            if not game:
                game = GameObject(game, ranked_score=score, list_source=filepath, total_count=total)
                game_DB[title] = game
            else:
                game.ranked_score += score
                game.total_count += total
                game.list_count += 1
                game.lists_referencing.append(filepath)
            print(f"Score of {score}: {title}")
        games_lists.append(filepath)

    # Step 4: Mark completed games
    for title in completed_titles:
        if title in game_DB:
            game_DB[title].completed = True

    # Step 5: Save to database
    #Doing basic insert to mongo at this point, and then we can add other values later on? After IGDB pulling?
    #Have the user be able to set a flag if they want use_mongo at this point, so they don't have to deal with trying to connect?

    #First testing the mongo connection and notifying user
    input("About to attempt connection to Mongo, press ENTER when you are ready")
    mongo_connect()

    db = DatabaseInterface(use_mongo=True, use_sql=True)
    for game in game_DB.values():
        db.insert_game_pre_ID(game)
    db.close() #close later on? like when program concludes? or when user sets they want to close connections?
    #or just set database manager whenever we want to connect to do stuff again and don't leave open?

    input(print(f"Successfully processed {len(game_DB)} games."))

    #REST OF FORMER MAIN FUNCTION FOLLOWS:

    # Taking custom class objects and making them JSON exportable
    export_DB = {}
    # export_DB["games"] = []

    import itertools

    # Breaks at this point because doesn't have game_DB? Make sure game_DB can be accessed by exporter? In run_generator()?

    for game, details in game_DB.items():
        export_DB[game] = json.loads(json.dumps(details.__dict__))
        #^See if I can use the new to_dict functionality?

    print(export_DB)

    json_string = ','.join(export_DB)
    # json_dict = json.loads(export_DB)
    # json_dict = json.loads(json_string)

    # Initial print of what we have in the games database
    with open(check_for_src("games_pre.json"), "w") as outfile:
        out_json = json.dump(export_DB, outfile)
        # out_json = json.dump(json_dict, outfile)
        # out_json = json.dump(json_string, outfile)
        print(out_json)

    import_DB = {}
    # import_DB["games"] = []

    input("Let's test pulling from JSON!\n")

    with open(check_for_src("games_pre.json"), "r") as json_file:
        # Reading the first character throws everything off
        # import_DB = json.load(json_file)
        # first_char = json_file.read(1)
        # if not first_char:
        if (os.stat(check_for_src("games_pre.json")).st_size == 0):
            print("Looks like we don't have anything in games_pre.json yet")
        else:
            import_DB = json.load(json_file)
            # import_DB = json.loads(json_file.read())
            # for line in json_file:
            # import_DB.append(json.loads(line))
            # import_DB["games"].append(json.loads(line))
            # import_DB.append(json.loads(line))
            print(import_DB)
            input()

    # having issue with jsondecodeerror: extra data, s, end OR str object has no attribute read (load vs. loads)
    # seems like putting all into a "games" array doesn't help things

    # Make sure fresh for actual process once done testing
    import_DB.clear()
    export_DB.clear()

    # eventually try for functionality where we only update the games that have updated scores? or new games?

    with open(check_for_src("games.json")) as json_file:
        # first_char = json_file.read(1)
        # if not first_char:
        if (os.stat(check_for_src("games.json")).st_size == 0):
            print("Looks like we don't have anything in games.json yet")
        else:
            import_DB = json.load(json_file)
    print(import_DB)
    print(game_DB.items().__class__)
    input()

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

    # This is where the user sets whether they want to grab from the IGDB API or not
    #Set a series of flags on whether to pull certain attributes or not into the database?
    #Set specific functions for every potential attribute to grab?
    # Try to find ways to make IGDB pulling run in the background so I can work on other things while it's going
    igdb_check = False
    igdb_answer = None
    scratch_answer = False
    limit_answer = False
    limit_number = 0
    while (igdb_check == False):
        print("Would you like to grab additional game data from the IGDB API at this moment? Y or N")
        igdb_answer = input("Make your selection: ")
        if (igdb_answer == 'Y' or igdb_answer == 'Yes'):
            while True:
                print(
                    "Would you like to start from scratch? Or only deal with games that don't already have IGDB information?")
                print("1. Start from scratch")
                print("2. Only deal with games without IGDB info already")
                scratch_option = input()
                if (scratch_option == "1"):
                    scratch_answer = True
                    break
                elif (scratch_option == "2"):
                    scratch_answer = False
                    break
                else:
                    print("Please enter a valid response")
                    print()
                    continue
            while True:
                print(
                    "Would you like to set a limit on how many games to grab info for? This process can take a long time, so this can help get your foot in the door")
                print("1. Set a limit")
                print("2. Just try for all games")
                limit_option = input()
                if (limit_option == "1"):
                    limit_answer = True
                    while True:
                        print("Would you like to set the limit to? Please provide a valid number")
                        limit_set = input()
                        if (limit_set.isnumeric()):
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
            client_id = get_env_var('CLIENT_ID')
            client_secret = get_env_var('CLIENT_SECRET')
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
            from igdb.igdbapi_pb2 import ReleaseDateResult

            igdb_request = wrapper.api_request(
                'games.pb',  # Note the '.pb' suffix at the endpoint
                'fields name, rating; limit 5; offset 0;'
            )
            games_message = GameResult()
            games_message.ParseFromString(igdb_request)  # Fills the protobuf message object with the response
            games = games_message.games
            print(games)

            # Figure out if I can be more efficient with endpoints to make it take quicker? taking very long now
            print("Time to go looking around")
            time_speedup = 0;
            order_of_insert = 1
            # resets every time we start the process partway through? any workaround for this?
            # ^A feature I'm implementing to cut down how many games parsed through so that we can have an easier first attempt
            for game, details in itertools.islice(game_DB.items(), 0, limit_number):
                # if(scratch_answer == False and game in import_DB and details.igdb_found == True):
                if (scratch_answer == False and game in import_DB):
                    print("Hey, we already got this one!")
                    game_DB[game] = import_DB[game]
                    continue
                # Set time speedup back to 0 if want full and accurate database for all items
                # need to set value in both if and elif to work properly
                if (time_speedup < 0):
                    print("SKIPPING!!")
                    time_speedup += 1
                    continue
                elif (time_speedup == 0):
                    time_speedup = 0
                check_string = 'fields *; exclude age_ratings, aggregated_rating, aggregated_rating_count, alternative_names, '
                check_string += 'artworks, bundles, checksum, collection, collections, cover, created_at, expanded_games, '
                check_string += 'external_games, follows, franchises, game_localizations, '
                check_string += 'keywords, language_supports, player_perspectives, '
                check_string += 'rating, rating_count, release_dates, screenshots, similar_games, standalone_expansions, '
                check_string += 'storyline, tags, total_rating, total_rating_count, updated_at, videos, websites; '
                # Check if <> comes first, where we use ID instead of name, for titles hard to specify
                if (game.startswith('<')):
                    print(details)
                    print(game.strip())
                    # input("Turns out this is a special case!\n")
                    game_title = game.strip()
                    # pull the ID from the <> part of the string
                    check_string += 'where id = '
                    # pattern_match = r'<[0-9]+>'
                    pattern_match = r'[0-9]+'
                    substring = re.findall(pattern_match, game_title)
                    title_ID = substring[0]
                    # Try to use some info from the substring so we can grab the name of the game better for logging?
                    # consider string.replace() function?
                    removal = '<' + title_ID + '> '
                    # modified_title = game_title.strip(str(substring))
                    modified_title = game_title.strip(removal)
                    check_string += title_ID
                    # Maybe grab the name from IGDB here, to update the name before it gets sent to the cluster?
                    # Otherwise it might have <ID> in front of the name there?
                    # modified_DB[modified_title] = details
                    # input(modified_DB[modified_title])
                else:
                    check_string += 'where name = "'
                    check_string += game.strip()
                    check_string += '"'
                check_string += ' & (status = (0,2,3,4,5,8) | status = null)'
                check_string += '; '
                # if (limit_answer):
                # check_string += f'limit {limit_number}; '
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
                        # print(result)
                    # print(earliest_game.slug)
                    # print(earliest_game.url)
                    # print(earliest_game.id)
                    # print(earliest_game.platforms)
                    # print(earliest_release)
                    # Time to put the IGDB attributes into the game we are putting out to the cluster
                    game_DB[game].igdb_ID = earliest_game.id
                    game_DB[game].igdb_found = True
                    # game_DB[game].release_date = earliest_release
                    game_DB[game].release_date = earliest_release.isoformat()  # To make Json serializable?
                    # print("Time to go through platforms")
                    # Spin this while loop off into its own function eventually?
                    plat_counter = 0
                    # plat_counter not defined error?
                    main_plat = None
                    plat_name = None
                    list_plats = []
                    # REPLACE THIS WITH A REQUEST THAT LOOKS AT THE ID AND THEN CONSULTS PLATFORMS ENDPOINT?
                    while (plat_counter < len(earliest_game.platforms)):
                        # plat_next = plat_counter + 1
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
                        plat_name = platforms[0].name
                        if (plat_counter == 0):
                            main_plat = plat_name
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
                    # game_DB[game].main_platform = earliest_game.platforms[0]
                    earliest_plat_release = None
                    earliest_plat_date = datetime.datetime.now()
                    for release in earliest_game.release_dates:
                        print("Going through releases")
                        release_ID = None
                        sub_query = 'fields name; where id=' + str(release) + ';'
                        sub_request = wrapper.api_request(
                            'release_dates.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query
                        )
                        releases_message = ReleaseDateResult()
                        releases_message.ParseFromString(
                            sub_request)  # Fills the protobuf message object with the response
                        releases = releases_message.releasedates
                        curr_release = releases[0]
                        if earliest_plat_release == None or earliest_plat > curr_release.date:
                            earliest_plat_release = curr_release
                            earliest_plat_date = curr_release.date
                            main_plat = curr_release.platform
                    sub_query = 'fields name; where id=' + str(main_plat) + ';'
                    sub_request = wrapper.api_request(
                        'platforms.pb',  # Note the '.pb' suffix at the endpoint
                        sub_query
                    )
                    platforms_message = PlatformResult()
                    platforms_message.ParseFromString(
                        sub_request)  # Fills the protobuf message object with the response
                    platforms = platforms_message.platforms
                    # main_plat = platforms[0].name
                    game_DB[game].main_platform = main_plat  # Will this always pull best choice?
                    # ^Seriously consider revising this to pull the first format with the earliest release date
                    # Because platform ID's are overruling too much (ex. wii is an early ID so overrides earlier releases)
                    # game_DB[game].list_platforms = earliest_game.platforms
                    if (len(list_plats) > 0):
                        game_DB[game].list_platforms = list_plats  # Will only pull ID's for now, need to tackle later?
                    modes = earliest_game.game_modes
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
                            # print(new_modes)
                            mode_type = new_modes[0].name
                            game_DB[game].player_counts.append(mode_type)
                            # input(mode_type)
                        # game_DB[game].player_counts = modes # Changes approach but for the better?
                    # ^Also consider multiplayer_modes? (they use more of a boolean/integer approach?)
                    developers = earliest_game.involved_companies
                    # ^consider a check for developer boolean? porting? supporting?
                    # do we count publishers?
                    # consider more categories for game objects later like publishers
                    # input(developers)
                    # print(developers)
                    if (len(developers) > 0):
                        for dev in developers:
                            dev_name = None
                            # input(dev)
                            # FIX THE REST OF THIS!!! (involved company, company?)
                            # first query to look at involved companies
                            # sub_query = 'fields *;'
                            # sub_query_1 = 'fields *; where id=' + str(dev.id) + ' & developer=true;'
                            sub_query_1 = 'fields *; where id=' + str(dev.id) + ';'
                            sub_request_1 = wrapper.api_request(
                                'involved_companies.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query_1
                            )
                            inv_companies_message = InvolvedCompanyResult()
                            inv_companies_message.ParseFromString(
                                sub_request_1)  # Fills the protobuf message object with the response
                            inv_companies = inv_companies_message.involvedcompanies
                            # print(inv_companies)
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
                            # print(companies)
                            dev_name = companies[0].name
                            game_DB[game].list_companies.append(dev_name)
                            # if dev true: add to devs
                            # if pub true: add to pubs
                            # also consider supporting boolean in addition to developer and publisher? porting?
                            if (is_dev):
                                game_DB[game].list_developers.append(dev_name)
                            if (is_pub):
                                game_DB[game].list_publishers.append(dev_name)
                        # game_DB[game].list_developers = developers  # Will this grab the most definitive list?
                    # ADD GENRES
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
                            genres_message.ParseFromString(
                                sub_request)  # Fills the protobuf message object with the response
                            new_genres = genres_message.genres
                            genre_type = new_genres[0].name
                            game_DB[game].genres.append(genre_type)
                    # ADD THEMES
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
                    game_DB[game].order_inserted = order_of_insert
                elif (len(games) == 1):
                    try:
                        current_game = games[0]
                        try:
                            game_DB[game].igdb_ID = current_game.id
                        except IndexError as e:
                            print("Error:", e)
                            # print("Index", i, "is out of range")
                        game_DB[game].igdb_found = True
                        game_DB[game].release_date = current_game.first_release_date.ToDatetime().isoformat()
                        # ^To make JSON serializable?

                        # this version gave animal crossing: new horizons switch and n64
                        # current approach giving that game nothing for platforms?
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
                        # PASTED FROM ABOVE WITHOUT COMMENTS
                        plat_counter = 0
                        main_plat = None
                        plat_name = None
                        list_plats = []
                        while (plat_counter < len(current_game.platforms)):
                            plat_ID = current_game.platforms[plat_counter]
                            sub_query = 'fields name; where id=' + str(plat_ID.id) + ';'
                            sub_request = wrapper.api_request(
                                'platforms.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query
                            )
                            platforms_message = PlatformResult()
                            platforms_message.ParseFromString(
                                sub_request)  # Fills the protobuf message object with the response
                            platforms = platforms_message.platforms
                            plat_name = platforms[0].name
                            if (plat_counter == 0):
                                main_plat = plat_name
                            list_plats.append(plat_name)
                            plat_counter += 1
                        earliest_plat_release = None
                        earliest_plat_date = datetime.datetime.now()
                        for release in earliest_game.release_dates:
                            print("Going through releases")
                            release_ID = None
                            sub_query = 'fields name; where id=' + str(release) + ';'
                            sub_request = wrapper.api_request(
                                'release_dates.pb',  # Note the '.pb' suffix at the endpoint
                                sub_query
                            )
                            releases_message = ReleaseDateResult()
                            releases_message.ParseFromString(
                                sub_request)  # Fills the protobuf message object with the response
                            releases = releases_message.releasedates
                            curr_release = releases[0]
                            if earliest_plat_release == None or earliest_plat > curr_release.date:
                                earliest_plat_release = curr_release
                                earliest_plat_date = curr_release.date
                                main_plat = curr_release.platform
                        sub_query = 'fields name; where id=' + str(main_plat) + ';'
                        sub_request = wrapper.api_request(
                            'platforms.pb',  # Note the '.pb' suffix at the endpoint
                            sub_query
                        )
                        platforms_message = PlatformResult()
                        platforms_message.ParseFromString(
                            sub_request)  # Fills the protobuf message object with the response
                        platforms = platforms_message.platforms
                        game_DB[game].main_platform = main_plat
                        if (len(list_plats) > 0):
                            game_DB[game].list_platforms = list_plats

                        modes = current_game.game_modes
                        if (len(modes) > 0):
                            for mode in modes:
                                mode_type = None
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
                            # game_DB[game].player_counts = modes # Changes approach but for the better?
                        # ^Also consider multiplayer_modes? (they use more of a boolean/integer approach?)
                        developers = current_game.involved_companies
                        # print(developers)
                        if (len(developers) > 0):
                            for dev in developers:
                                dev_name = None
                                # FIX THE REST OF THIS!!! (involved company, company?)
                                # first query to look at involved companies
                                # sub_query = 'fields *;'
                                # sub_query_1 = 'fields *; where id=' + str(dev.id) + ' & developer=true;'
                                sub_query_1 = 'fields *; where id=' + str(dev.id) + ';'
                                sub_request_1 = wrapper.api_request(
                                    'involved_companies.pb',  # Note the '.pb' suffix at the endpoint
                                    sub_query_1
                                )
                                inv_companies_message = InvolvedCompanyResult()
                                inv_companies_message.ParseFromString(
                                    sub_request_1)  # Fills the protobuf message object with the response
                                inv_companies = inv_companies_message.involvedcompanies
                                # print(inv_companies)
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
                        # genre seems to be pulling in too many results right now, unrelated?
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
                                genres_message.ParseFromString(
                                    sub_request)  # Fills the protobuf message object with the response
                                new_genres = genres_message.genres
                                genre_type = new_genres[0].name
                                game_DB[game].genres.append(genre_type)
                        # ADD THEMES
                        # theme seems to be pulling in too many results right now, unrelated?
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
                        game_DB[game].order_inserted = order_of_insert
                    except Exception as e:
                        print("An error has occurred:", e)
                        # it starts hitting errors when it gets to some of the new games featured in metacritic user scores?
                else:
                    print("Not found with that name!")
                    input("Maybe you need to alter the title somehow?\n")
                order_of_insert += 1

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
        elif (igdb_answer == 'N' or igdb_answer == 'No'):
            print("Understood, skipping to next step.")
            igdb_check = True
        else:
            print("Answer not understood, try again.")
            print()

    print(game_DB.items().__class__)
    for game, details in itertools.islice(game_DB.items(), 0, 3):
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

    with open (check_for_src("games.json"), "w") as outfile:
        json.dump(export_DB, outfile)

    print("Games exported to games.json!")

    #Used code sample from Atlas on how to connect with Pymongo for assistance here
    #Connecting to env file to get private login data
    mon_connect = get_env_var('MONGO_URI')
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
            mongo_limit = int(input())
            break
        elif (mongo_option == '3'):
            break
        else:
            print("I'm sorry, I don't understand. Please enter valid input")
            continue
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
        export_dict = {}
        if (game.startswith('<')):
            #If I successfully improve how titles get put out to mongo cluster, make the IGDB ID the key I use there for ID
            print(game)
            pattern_match = r'[0-9]+'
            substring = re.findall(pattern_match, game)
            title_ID = substring[0]
            removal = '<' + title_ID + '> '
            modified_title = game.strip(removal)
            export_dict["Title"] = modified_title
        else:
            export_dict["Title"] = game
        export_dict["IGDB ID"] = details['igdb_ID']
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
        export_dict["Total Count"] = details['total_count']
        export_dict["Order Inserted"] = details['order_inserted']
        #export_dict = dict(game)
        #^need to expand and clarify more?
        #export_dict = dict('Title' = game, 'IGDB ID' = details.igdb_ID, 'Ranked Score' = details.ranked_score)
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

    # further sort by keys after sorted by values?

def main():
    #Basic solution to get testing functions to work for now, make a cleaner solution later?

    run_generator()

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
    file_ranked = open(check_for_src("reports/Sorted by Ranked.txt"),"w", encoding="utf-8")
    file_inclusion = open(check_for_src("reports/Sorted by Inclusion.txt"),"w", encoding="utf-8")
    file_average = open(check_for_src("reports/Sorted by Average.txt"),"w", encoding="utf-8")
    file_ranked_uncompleted = open(check_for_src("reports/Sorted by Ranked (Uncompleted).txt"), "w", encoding="utf-8")
    file_inclusion_uncompleted = open(check_for_src("reports/Sorted by Inclusion (Uncompleted).txt"),"w", encoding="utf-8")
    file_average_uncompleted = open(check_for_src("reports/Sorted by Average (Uncompleted).txt"),"w", encoding="utf-8")

    for game in games_pulled_ranked:
        entry = ""
        completed = game["Completed"]
        if (completed == True):
            entry += "[x]"
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
        output_lists = ', '.join(game['List of References'])
        sheet1.write(excel_count, 5, output_lists)
        sheet1.write(excel_count, 6, completion_status)
        #sheet1.write(excel_count, 5, game['Main Platform'].strip())
        sheet1.write(excel_count, 7, game['Main Platform'])
        #Create a loop to deal with printing the platforms in a comma approach
        """
        game_platforms = game['List of Platforms']
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
        sheet1.write(excel_count, 8, platforms_string)
        #sheet1.write(excel_count, 7, game['Release Date'].strip())
        #^Try to strip escape chars out earlier or the items themselves
        sheet1.write(excel_count, 9, game['Release Date'])
        players_string = ', '.join(game['Player Counts'])
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
    wb.save(check_for_src('reports/Sorted Database.xls'))

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

"Where we start the main function"
if __name__ == "__main__":
    main()