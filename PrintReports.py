#Imports grabbed from generator.py I thought I might need
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv

print("Welcome to PrintReports!")

print("For now let's start with a test pull. Best games for the Wii!")

#Pulling from the mongo cluster seems not to work if we haven't done anything with mongo yet?
#When haven't run generator it seems not to work fully?

load_dotenv()

#Start connecting to Mongo cluster
mon_connect = os.getenv('MONGO_URI')
#print(mon_connect)
mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
#mon_client = pymongo.MongoClient(mon_connect)
mon_db = mon_client["GameSorting"]
try:
    mon_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
mon_col = mon_db["games"]
list_col = mon_db["lists"]

test_query = {"Main Platform": "Wii"}
#test_query = {"Main Platform": {"$exists": True}}
#test_query = {"Ranked Score": { "$gt": 2400 } }

print("Time to grab the games!")
#games_pulled = mon_db.mon_col.find().limit(15)
games_pulled = mon_col.find().limit(10)
#games_pulled = GameSorting.games.find().limit(10)
#games_pulled = mon_db.find().limit(15)
games_pulled = mon_col.find({},{"Title": 1, "Main Platform": 1}).limit(10)
games_pulled_query = mon_col.find(test_query, { "List of References": 0, "Total Count": 0}).limit(10)
games_pulled_ranked = mon_col.find(test_query).sort("Ranked Score", -1)
games_pulled_inclusion = mon_col.find(test_query).sort("Inclusion Score", -1)
games_pulled_average = mon_col.find(test_query).sort("Average Score", -1)

print(games_pulled_query)

"""
for game in games_pulled:
    print("Here is a game")
    print(game)
    if(game["Main Platform"] == "Wii"):
        print("We found one!")
        print(game)
    print()
"""

#input("Brief pause\n")

for game in games_pulled_query:
    print("Here is a game")
    print(game)
    #if(game["Main Platform"] == "Wii"):
    #    print("We found one!")
    #    print(game)
    print()

print("Now it's time for us to pick some options in generating a report")

answer_check_main = False
queries = []
while(answer_check_main == False):
    print()
    print("Which filter category would you like to add on to your report?")
    print("1. Platform Inclusion")
    print("2. Main Platform")
    print("3. Release Date")
    print("4. Completion Status")
    print("5. Title")
    print("6. Ranked Score")
    print("7. Inclusion Score")
    print("8. Average Score")
    print("9. Player Count")
    print("10. Developers")
    print("11. Miscellaneous")
    print("12. Finish and Generate Report")
    #consider franchise option when that data is pulled? other fields?

    filter_category = input("Make selection here: ")

    if(filter_category == '1'):
        print("You have selected 1. Platform Inclusion")
        print("Would you like to include single platforms, entire brands, or formats of platforms?")
        print("1. Single Platform")
        print("2. Brand of Platform")
        print("3. Format of Platform")
        platforms_option = input()
        if(platforms_option == '1'):
            print("Now we are going to list all of the options of platforms you can choose from")
            print("Note that the numbers are listed as so because they are the platform ID's listed in IGDB's API")
            input("Whenever you are ready, the platform options will be listed in full\n")
            print("3. Linux")
            print("4. N64")
            print("5. Wii")
            print("6. PC (Windows)")
            print("7. PS1")
            print("8. PS2")
            print("9. PS3")
            print("11. Xbox")
            print("12. X360")
            print("13. PC-DOS")
            print("14. Mac")
            print("15. C64 & C128")
            print("16. Amiga")
            print("18. NES")
            print("19. SNES")
            print("20. DS")
            print("21. GCN")
            print("22. GBC")
            print("Which platform would you like to include?")
            #have function to check if number just given was one of the valid options?
            if (plat_ID.id == 23):
                plat_name = "DC"
            elif (plat_ID.id == 24):
                plat_name = "GBA"
            elif (plat_ID.id == 25):
                plat_name = "Amstrad CPC"
            elif (plat_ID.id == 26):
                plat_name = "ZX Spectrum"
            elif (plat_ID.id == 27):
                plat_name = "MSX"
            elif (plat_ID.id == 29):
                plat_name = "GEN/MD"
            elif (plat_ID.id == 30):
                plat_name = "32X"
            elif (plat_ID.id == 32):
                plat_name = "SAT"
            elif (plat_ID.id == 33):
                plat_name = "GB"
            elif (plat_ID.id == 34):
                plat_name = "Android"
            elif (plat_ID.id == 35):
                plat_name = "Sega Game Gear"
            elif (plat_ID.id == 38):
                plat_name = "PSP"
            elif (plat_ID.id == 39):
                plat_name = "iOS"
            elif (plat_ID.id == 41):
                plat_name = "Wii U"
            elif (plat_ID.id == 46):
                plat_name = "Vita"
            elif (plat_ID.id == 48):
                plat_name = "PS4"
            elif (plat_ID.id == 49):
                plat_name = "XONE"
            elif (plat_ID.id == 52):
                plat_name = "Arcade"
            elif (plat_ID.id == 58):
                plat_name = "Super Famicom"
            elif (plat_ID.id == 59):
                plat_name = "2600"
            elif (plat_ID.id == 64):
                plat_name = "Sega Master System"
            elif (plat_ID.id == 75):
                plat_name = "Apple II"
            elif (plat_ID.id == 79):
                plat_name = "Neo Geo MVS"
            elif (plat_ID.id == 80):
                plat_name = "Neo Geo AES"
            elif (plat_ID.id == 88):
                plat_name = "Magnavox Odyssey"
            elif (plat_ID.id == 99):
                plat_name = "Famicom"
            elif (plat_ID.id == 130):
                plat_name = "Switch"
            elif (plat_ID.id == 137):
                plat_name = "New Nintendo 3DS"
            elif (plat_ID.id == 149):
                plat_name = "PC-98"
            elif (plat_ID.id == 169):
                plat_name = "Xbox Series"
            elif (plat_ID.id == 306):
                plat_name = "Satellaview"
            elif (plat_ID.id == 379):
                plat_name = "Game.com"
            #going to go off of IGDB ID's for now?
            #...
        print("Which brand of platform would you like to include?")
        print("1. Nintendo")
        print("2. Sony")
        print("3. Microsoft")
        print("4. Sega")
        print("5. Atari")
        #...
        print("Which format of platform would you like to include?")
        print("1. Console")
        print("2. Handheld")
        print("3. Computer")
        print("4. Arcade")
        #...
        print("Returning back to main menu")
    elif (filter_category == '2'):
        print("You have selected 2. Main Platform")
        print("Which platform would you like to be the main platform?")
        # ...
    elif (filter_category == '3'):
        print("You have selected 3. Release Date")
        print("Would you like to enter a specific date? Or specify a time range?")
        #...
        print("Type in the date you would like to filter for")
        #...
        print("Here are the time range options")
        print("1. Specific year")
        print("2. Specific decade")
        print("3. Before a date")
        print("4. After a date")
        print("5. In between two dates")
        print("6. 20th Century")
        print("7. 21st Century")
        #...
    elif (filter_category == '4'):
        print("You have selected 4. Completion Status")
        print("Would you like games you have completed? Or games you haven't completed?")
        #...
    elif (filter_category == '5'):
        print("You have selected 5. Title")
        print("Would you like to enter a filter string to use in filtering results?")
        #...
    elif (filter_category == '6'):
        print("You have selected 6. Ranked Score")
        print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
        #...
    elif (filter_category == '7'):
        print("You have selected 7. Inclusion Score")
        print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
        #...
    elif (filter_category == '8'):
        print("You have selected 8. Average Score")
        print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
        #...
    elif (filter_category == '9'):
        print("You have selected 9. Player Count")
        print("Would you like to select whether you want singleplayer or multiplayer?")
        print("Or select one-by-one which player counts you would like to include?")
        #...
    elif (filter_category == '10'):
        print("You have selected 10. Developers")
        print("Are you planning on selecting filters for developers or publishers right now?")
        print("For developers, are you looking for Main Developers, or just any company that worked on a game?")
        print("Which companies are you planning to filter for?")
        #...
    elif (filter_category == '11'):
        print("You have selected 11. Miscellaneous")
        print("This is for miscellaneous filter options that don't fit easily anywhere else")
        #...
    elif(filter_category == '12'):
        #answer_check_main = True
        print("Alright! Let's generate the report with the options selected!")
        custom_query = {}
        print("How would you like your report sorted?")
        print("1. By Ranked Score")
        print("2. By Inclusion Score")
        print("3. By Average Score")
        print("4. Alphabetical")
        print("5. Oldest First")
        print("6. Newest First")
        sort_type = input()
        if(sort_type == '1'):
            games_pulled = mon_col.find(custom_query).sort("Ranked Score", -1)
        elif (sort_type == '2'):
            games_pulled = mon_col.find(custom_query).sort("Inclusion Score", -1)
        elif (sort_type == '3'):
            games_pulled = mon_col.find(custom_query).sort("Average Score", -1)
        else:
            print("Sorry, I don't understand")
            #check again
        file_name = input("What would you like to name your file: ")
        #come up with a check if a particular file name already exists and whether they want to overwrite?
        file_name += "[CUSTOM GENERATION].txt"
        file_print = open(file_name, "w", encoding="utf-8")
        for game in games_pulled:
            # print(game)
            entry = ""
            completed = game["Completed"]
            if (completed == True):
                entry += "[x]"
            entry += game['Title'].strip()
            entry += " --> "
            entry += str(game['Ranked Score'])
            file_print.write(entry)
            file_print.write("\n")
        print("Your custom report has finished printing! Would you like to print more reports? Or quit the program")
        print("1. Print more reports")
        print("2. Quit the program")
        continue_check = input()
        if(continue_check == '1'):
            print("Alright, let's get back to the main printing menu!")
        elif(continue_check == '2'):
            answer_check_main = True
            print("Hope you enjoyed printing reports! See you later!")
        else:
            print("I'm sorry, I don't understand")
            #check again
    else:
        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")

#Close connection to open up socket (seemed to cause problems when running generator then trying printreports?)
mon_client.close()
#Close cursors too?
games_pulled.close()
games_pulled_query.close()
games_pulled_ranked.close()
games_pulled_average.close()
games_pulled_inclusion.close()

print("Successfully completed! Have a good day!")