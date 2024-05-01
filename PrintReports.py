#Imports grabbed from generator.py I thought I might need
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv

print("Welcome to PrintReports!")

print("For now let's start with a test pull. Best games for the PC!")

#Pulling from the mongo cluster seems not to work if we haven't done anything with mongo yet?
#When haven't run generator it seems not to work fully?

#Start connecting to Mongo cluster
mon_connect = os.getenv('MONGO_URI')
#print(mon_connect)
mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
mon_db = mon_client["GameSorting"]
try:
    mon_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
mon_col = mon_db["games"]
list_col = mon_db["lists"]

test_query = { "Main Platform": "PC (Windows)"}

print("Time to grab the games!")
#games_pulled = mon_db.mon_col.find().limit(15)
games_pulled = mon_col.find().limit(15)
games_pulled_query = mon_col.find(test_query)
games_pulled_ranked = mon_col.find(test_query).sort("Ranked Score", -1)
games_pulled_inclusion = mon_col.find(test_query).sort("Inclusion Score", -1)
games_pulled_average = mon_col.find(test_query).sort("Average Score", -1)

print(games_pulled_query)

for game in games_pulled:
    print("Here is a game")
    print(game)
    if(game["Main Platform"] == "PC (Windows)"):
        print("We found one!")
        print(game)
    print()

print("Now it's time for us to pick some options in generating a report")

#Close connection to open up socket (seemed to cause problems when running generator then trying printreports?)
mon_client.close()
#Close cursors too?
games_pulled.close()
games_pulled_query.close()
games_pulled_ranked.close()
games_pulled_average.close()
games_pulled_inclusion.close()

print("Successfully completed! Have a good day!")