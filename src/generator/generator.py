# import required module
import json
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
import time
from typing import List
# Writing to an excel sheet using Python
import xlwt
from xlwt import Workbook
from pathlib import Path

import itertools

from .config import check_for_src, get_env_var
from .database_interface import DatabaseInterface
from .exporter import export_to_json, export_to_excel, export_to_text
from .file_loader import ListType, get_files_in_dir, read_game_list, read_attributed_games
from .game_object import GameObject
from .igdb_client import IGDB_Client

#Seems like new files I add might not be integrating yet into the general process? Make sure they do

def mongo_connect():
    #Replace the part where this originally happened later in the code with this function?
    mon_connect = get_env_var('MONGO_URI')
    mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
    monDB = mon_client["GameSorting"]
    #^Have this part happen before the function actually goes?
    connect_message = ""
    try:
        mon_client.admin.command('ping')
        connect_message = "Pinged your deployment. You successfully connected to MongoDB!"
        print(connect_message)
    except Exception as e:
        print(e)
        connect_message = e
    return connect_message

def load_list(files, file_count, game_DB, games_lists, type: ListType):
    """
    Load and process a directory of game lists into game_DB.
    Returns the updated file count.
    """
    for filepath in files:
        file_count += 1
        for title, score, total in read_game_list(filepath, type):
            if title not in game_DB:
                game_DB[title] = GameObject(title, ranked_score=score, total_count=total)
                game_DB[title].lists_referencing.append(filepath)  # track first appearance
            else:
                game = game_DB[title]
                game.ranked_score += score
                game.total_count += total
                game.list_count += 1
                game.lists_referencing.append(filepath)
            print(f"Score of {score}: {title}")
        games_lists.append(filepath)
    return file_count

def generate_sorted_reports(games: List[GameObject]):
    """Generate sorted text reports for ranked, inclusion, and average scores"""
    from .config import check_for_src
    

    # Sort games by different criteria
    games_by_ranked = sorted(games, key=lambda g: g.ranked_score, reverse=True)
    games_by_inclusion = sorted(games, key=lambda g: g.list_count, reverse=True)
    games_by_average = sorted(games, key=lambda g: g.ranked_score / g.list_count, reverse=True)
    
    # Generate ranked score report
    with open(check_for_src("reports/Sorted by Ranked.txt"), "w", encoding="utf-8") as f_ranked, \
         open(check_for_src("reports/Sorted by Ranked (Uncompleted).txt"), "w", encoding="utf-8") as f_ranked_uncompleted:
        
        for game in games_by_ranked:
            entry = ""
            if game.completed:
                entry += "[x]"
            entry += game.title.strip()
            if game.igdb_ID:
                entry += f" [IGDB ID: {game.igdb_ID}]"
            entry += f" --> {game.ranked_score}"
            
            f_ranked.write(entry + "\n")
            if not game.completed:
                f_ranked_uncompleted.write(entry + "\n")
    
    # Generate inclusion score report
    with open(check_for_src("reports/Sorted by Inclusion.txt"), "w", encoding="utf-8") as f_inclusion, \
         open(check_for_src("reports/Sorted by Inclusion (Uncompleted).txt"), "w", encoding="utf-8") as f_inclusion_uncompleted:
        
        for game in games_by_inclusion:
            entry = ""
            if game.completed:
                entry += "[x]"
            entry += game.title.strip()
            if game.igdb_ID:
                entry += f" [IGDB ID: {game.igdb_ID}]"
            entry += f" --> {game.list_count}"
            
            f_inclusion.write(entry + "\n")
            if not game.completed:
                f_inclusion_uncompleted.write(entry + "\n")
    
    # Generate average score report
    with open(check_for_src("reports/Sorted by Average.txt"), "w", encoding="utf-8") as f_average, \
         open(check_for_src("reports/Sorted by Average (Uncompleted).txt"), "w", encoding="utf-8") as f_average_uncompleted:
        
        for game in games_by_average:
            entry = ""
            if game.completed:
                entry += "[x]"
            entry += game.title.strip()
            if game.igdb_ID:
                entry += f" [IGDB ID: {game.igdb_ID}]"
            entry += f" --> {game.ranked_score / game.list_count}"
            
            f_average.write(entry + "\n")
            if not game.completed:
                f_average_uncompleted.write(entry + "\n")

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

    #file_path = Path("game_lists") / "Completions.txt"
    completed_titles = set(read_attributed_games(Path("game_lists") / "Completions.txt"))

    ranked_file_count = 0
    unranked_file_count = 0
    former_file_count = 0

    client = IGDB_Client()
    db = None

    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')

    # Step 1: Load and process ranked lists
    ranked_file_count = load_list(get_files_in_dir("game_lists/ranked"), ranked_file_count, game_DB, games_lists, ListType.RANKED)

    # Step 2: Load and process unranked lists
    unranked_file_count = load_list(get_files_in_dir("game_lists/unranked"), unranked_file_count, game_DB, games_lists, ListType.UNRANKED)

    # Step 3: Load and process former lists
    former_file_count = load_list(get_files_in_dir("game_lists/former"), former_file_count, game_DB, games_lists, ListType.FORMER)

    # Step 4: Mark completed games
    for title in completed_titles:
        if title in game_DB:
            game_DB[title].completed = True

    # Step 4.5: Mark seasonal games
    spring_titles = set(read_attributed_games(Path("game_lists") / "Spring.txt"))
    summer_titles = set(read_attributed_games(Path("game_lists") / "Summer.txt"))
    fall_titles = set(read_attributed_games(Path("game_lists") / "Fall-Halloween.txt"))
    winter_titles = set(read_attributed_games(Path("game_lists") / "Winter-Christmas.txt"))

    for title in spring_titles:
        if title in game_DB:
            game_DB[title].seasonal_spring = True

    for title in summer_titles:
        if title in game_DB:
            game_DB[title].seasonal_summer = True

    for title in fall_titles:
        if title in game_DB:
            game_DB[title].seasonal_fall_halloween = True

    for title in winter_titles:
        if title in game_DB:
            game_DB[title].seasonal_winter_christmas = True

    #JSON LOADING AND PULLING BEFORE IGDB CHECKING

    import_DB = {}

    # eventually try for functionality where we only update the games that have updated scores? or new games?

    # Step 5: Enrich with IGDB Data
    # IGDB_Client handles <ID> prefix, caching, unicode normalization, and all fields
    # (platforms, release_dates, genres, themes, game_modes, involved_companies)

    #pulling wrong data on some fields, might need to further develop?
    #Figure out how to derive a main_platform, perhaps by going through all of the release dates of all the platforms, and having some sort of way to break ties?
    full_answer = False
    while True:
        igdb_answer = input("Would you like to pull data from IGDB right now? Y or N: ").strip()
        if igdb_answer in ('Y', 'y', 'Yes', 'yes'):
            while True:
                #Add options to mix and match eventually
                #start with games table but later make sure all tables are getting all fields they need
                print("Would you like to store all potential data on games or just the minimum?")
                print("1. Just the minimum")
                print("2. All potential data")
                data_option = input("> ").strip()
                if data_option == "1":
                    full_answer = False
                    break
                elif data_option == "2":
                    full_answer = True
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            #could elaborate so limit only applies to games missing igdb data?
            limit_number = None  # defaults to no limit
            while True:
                print("Would you like to set a limit on how many games to grab info for?")
                print("1. Set a limit")
                print("2. No limit, try all games")
                limit_option = input("> ").strip()
                if limit_option == "1":
                    while True:
                        limit_set = input("Enter a positive number: ").strip()
                        if limit_set.isnumeric() and int(limit_set) > 0:
                            limit_number = int(limit_set)
                            break
                        else:
                            print("Please enter a valid positive number")
                    break
                elif limit_option == "2":
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            # Iterate with optional limit
            for i, game in enumerate(game_DB.values(), start=1):
                try:
                    client.enrich_game_object(game)
                    print(f"Processed {i}/{limit_number if limit_number else len(game_DB)}: {game.title}")
                    if limit_number and i >= limit_number:
                        break
                    time.sleep(0.25)  # ~4 requests per second, adjust as needed
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        print("Hit IGDB rate limit, waiting 10 seconds...")
                        time.sleep(10)
                    else:
                        raise
            break
        elif igdb_answer in ('N', 'n', 'No', 'no'):
            print("Understood, skipping IGDB enrichment.")
            break
        else:
            print("Please enter Y or N.")

    # Step 6: Save to database
    #Doing basic insert to mongo at this point, and then we can add other values later on? After IGDB pulling?
    #Have the user be able to set a flag if they want use_mongo at this point, so they don't have to deal with trying to connect?

    # See if we want to connect to Mongo cluster right now, so we can shut down that aspect if we don't want to deal with it
    db = None
    while True:
        #local_connect = True
        print("Would you like to connect to Mongo at this time or just local SQLite?")
        print("1. Connect to both")
        print("2. Only connect to SQLite")
        choice = input("> ").strip()
        if (choice == "1"):
            while True:
                print("Would you like to connect to the Atlas web instance or just local MongoDB?")
                print("1. Connect to Atlas")
                print("2. Connect to local MongoDB")
                local_choice = input("> ").strip()
                if(local_choice == "1"):
                    local_connect = False
                    break
                if (local_choice == "2"):
                    local_connect = True
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            print(local_connect)
            db = DatabaseInterface(use_mongo=True, use_sql=True, local_connect=local_connect)
            # First testing the mongo connection and notifying user
            # Try adding try, catch, except logic to mongo connection attempts?
            if not local_connect:
                input("About to attempt connection to Mongo, press ENTER when you are ready")
                mongo_connect()
            break
        elif (choice == "2"):
            db = DatabaseInterface(use_mongo=False, use_sql=True)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    print(full_answer)
    for i, game in enumerate(game_DB.values(), start=1):
        #enumerate or whatever so I can keep track of how many insertions are being done so progress is more clear on CLI
        #Use the pre-ID option in other cases? But here we should already have it?
        #Have the option to save to database before we bother to grab IGDB data? And then update with what we have gotten?
        #Give option to set limit on how many records to put out to databases?
        if(full_answer):
            db.insert_game_full(game)
        else:
            db.insert_game(game)
        if(db.sql):
            print(f"Inserting game {i} into SQLite")
        if(db.mongo):
            print(f"Inserting game {i} into MongoDB")
    db.close() #close later on? like when program concludes? or when user sets they want to close connections?
    #or just set database manager whenever we want to connect to do stuff again and don't leave open?

    print(f"Successfully processed {len(game_DB)} games.")

    # THIS IS THE OLD SETUP FOR THE MONGO DATABASE PROCESS, SEE ABOUT PULLING
    # WHAT I NEED AND REPLACING WHAT I DON'T

    input("FROM THIS PART ONWARD CLEAR MONGO BITS, ONLY ATTEMPT MONGO CONNECTION IF WE INTEND SO")

    #input("This is a test, program going to break for now. Goodbye!")
    #Do I need to close files at this point for writes? or do i even have anything open?
    #use with open in some cases to avoid needing to close?
    #exit()

    # Create index on title so can do partial title searching, don't mark as unique because some titles won't be
    """mon_col.create_index('Title')"""

    # INSERT ALL GAMES INTO DATABASE
    # Clear database to begin with?
    while True:
        print("Would you like to clear the database to start? Y or N")
        clear_option = input()
        if (clear_option == "Y" or clear_option == "y"):
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
        if (mongo_option == '1'):
            mongo_limit = limit_number
            break
        elif (mongo_option == '2'):
            print("Set your limit here")
            # add input verification
            mongo_limit = int(input())
            break
        elif (mongo_option == '3'):
            break
        else:
            print("I'm sorry, I don't understand. Please enter valid input")
            continue

    print("INSERTING INTO MONGODB!")
    for game, details in itertools.islice(game_DB.items(), 0, mongo_limit):
        print(details.__class__)
        # If they're all from scratch, details is a gameobject, otherwise it's a dict
        if (isinstance(details, GameObject)):
            print("This one's a game object!")
            details = json.loads(json.dumps(details.__dict__))
        # insertion = mon_col.insert_one(details)
        # insertion = mon_col.insert_one(game_DB[game])
        export_dict = {}
        if (game.startswith('<')):
            # If I successfully improve how titles get put out to mongo cluster, make the IGDB ID the key I use there for ID
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
        export_dict["Inclusion Score"] = details['list_count']
        average_score = details['ranked_score'] / details['total_count']
        export_dict["Average Score"] = average_score
        export_dict["List of References"] = details['lists_referencing']
        export_dict["Completed"] = details['completed']
        export_dict["List of Platforms"] = details['list_platforms']
        export_dict["Release Date"] = details['release_date']
        export_dict["Player Counts"] = details['player_counts']
        export_dict["Developers"] = details['list_developers']
        export_dict["Publishers"] = details['list_publishers']
        export_dict["Companies"] = details['list_companies']
        export_dict["Genres"] = details['genres']
        export_dict["Themes"] = details['themes']
        export_dict["Total Count"] = details['total_count']
        # export_dict = dict(game)
        # ^need to expand and clarify more?
        # export_dict = dict('Title' = game, 'IGDB ID' = details.igdb_ID, 'Ranked Score' = details.ranked_score)
        """insertion = mon_col.insert_one(export_dict)"""

    # insertion = mon_col.insert_many(export)
    print("TIME TO INSERT THE LISTS INTO MONGODB!")
    """
    for game_list in games_lists:
        # could keep track of what type of list it is, other variables?
        list_dict = dict(Title=game_list)
        print(list_dict)
        list_insert = list_col.insert_one(list_dict)
         # list_dict["Title"].append(list)
    """

    # after printed out everything to excel, then make three printed sorted lists?
     # each time, sort excel a certain way, then print out excel factors to list?

    # further sort by keys after sorted by values?

    # Files to mark additional personal statuses of games so far:
    # Completed

    # Prints total counts of lists used for each category
    print(f"Ranked Lists: {ranked_file_count}")
    print(f"Unranked Lists: {unranked_file_count}")
    print(f"Former Lists: {former_file_count}")

    print("LISTS USED IN PROCESS:")
    for game_list in games_lists:
        print(game_list)

    # Step 7: Export results
    # Add all of the specialized reports I was having before?
    export_list = list(game_DB.values())
    export_to_json(export_list, "reports/games.json")
    export_to_excel(export_list, "reports/games.xlsx")
    export_to_text(export_list, "reports/games.txt")
    
    # Generate sorted reports
    generate_sorted_reports(export_list)

    #OLD EXPORT PROCESS

    print()
    print("Time to grab the games from the database!")

    # Generate sorted reports
    generate_sorted_reports(export_list)

    # Writing to excel using new approach from MongoDB Atlas
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

    """for game in games_pulled:
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
        sheet1.write(excel_count, 7, game['Main Platform'])
        #Create a loop to deal with printing the platforms in a comma approach
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
        excel_count += 1"""
    wb.save(check_for_src('reports/Sorted Database.xls'))

    # Close connection to open up socket (seemed to cause problems when running generator then trying printreports?)
    """mon_client.close()"""
    # Close cursors too?
    """games_pulled.close()
    games_pulled_ranked.close()
    games_pulled_average.close()
    games_pulled_inclusion.close()"""

    #COMPLETION OF NEW PROCESS

    input(print(f"Successfully processed and stored {len(export_list)} games."))

def main():
    run_generator()

    print("Successfully completed! Have a good day!")

"Where we start the main function"
if __name__ == "__main__":
    main()

"""
OLD COMMENTS FOR FURTHER REVIEW (FROM OLD IGDB PROCESS):
# This is where the user sets whether they want to grab from the IGDB API or not
    # Set a series of flags on whether to pull certain attributes or not into the database?
    # Set specific functions for every potential attribute to grab?
    # Try to find ways to make IGDB pulling run in the background so I can work on other things while it's going

            # START SCRAPING FOR ATTRIBUTES
            # (Look into close-enough matches that can match when it’s not exact?)
            # (Have the option to replace data manually when database info isn’t good enough or is missing?)

#Stripping out <ID> to have a modified name (modified_DB?)

# Had & version_parent = null in the check_string before, but probably won't work in cases we do want port, might just want
                # more specificity in some cases
                # | category = 3  (attempted to insert this into the query)
                # Category is an enum, 3 means it's a bundle, is | the right way to do an or?
                # Exclude versions that aren't the parent
                # Exclude cancelled, unreleased, TBD versions?
                # Figure out how to deal with children versions? How to give points and pass on points to parent too?
                # Also dealing with compilation games? Add points to individual games? Create field to track subgames in a compilation?
                # check_string += ';'

#ADD PLATFORMS
# Originally went through all of the platforms for the earliest game and added them
                    # Set the first one to the main platform, might want better logic going forward for main_plat
                    #Support for platform_families?

#EARLIEST RELEASE
#DETERMINING EARLIEST RELEASE DATE OF EARLIEST GAME RELEASE
                    # REMOVING THIS PART
                    # Originally looped through them all, if none so far then accept, if find one that was earlier replace with that

#ADD MODES
# ^Also consider multiplayer_modes? (they use more of a boolean/integer approach?)

# ADD COMPANIES, DEVELOPERS PUBLISHERS
                    # ^consider a check for developer boolean? porting? supporting?
                    # do we count publishers?
                    # consider more categories for game objects later like publishers

# APPEND TO DEVELOPERS OR PUBLISHERS IF IS_DEV OR IS_PUB
                    # also consider supporting boolean in addition to developer and publisher? porting?

# When there is ID confusion, need to clarify ID when putting entries
            # Have a process that runs through when generating databases and pauses
            # when there are multiple options, so we can try to narrow down on that title
            # Use <> to contain ID number (from IGDB database)
            # Example: The ID we want to use for Super Mario World is 1070
            # retitle: a link to the past and other zelda games
            # ID for Final Fantasy VII: 427
            # investigate ways to test for what is the most parent version?
            # when multiple options to go with, for now go with the one that has
            # the most total_rating_count? earliest release date?

            # For now, Pokemon versions need to pick one over the other,for simplicity we go for the one that tends to be listed first
            # Pokémon Red Version seems to break the api request, probably the accented e
            # Doesn't get found with the title "Pokemon Red Version" either though
            # exit()
"""