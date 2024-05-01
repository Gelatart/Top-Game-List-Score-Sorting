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
games_pulled_query = mon_col.find(test_query, { "List of References": 0}).limit(10)
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

    filter_category = input("Make selection here: ")

    if(filter_category == '1'):
        print("You have selected 1. Platform Inclusion")
        print("Would you like to include single platforms, entire brands, or formats of platforms?")
        print("1. Single Platform")
        print("2. Brand of Platform")
        print("3. Format of Platform")
        print("Which platform would you like to include?")
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
    elif(filter_category == '12'):
        answer_check_main = True
        print("Alright! Let's generate the report with the options selected!")
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