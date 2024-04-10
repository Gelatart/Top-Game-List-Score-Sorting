#Imports grabbed from generator.py I thought I might need
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv

print("Welcome to PrintReports!")

print("For now let's start with a test pull. Best games for the N64!")

#Start connecting to Mongo cluster
mon_connect = os.getenv('MONGO_URI')
#print(mon_connect)
mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
monDB = mon_client["GameSorting"]
try:
    mon_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
mon_col = monDB["games"]
list_col = monDB["lists"]

test_query = { "Main Platform": "N64"}

print("Time to grab the games!")
games_pulled = mon_col.find(test_query)
games_pulled_ranked = mon_col.find(test_query).sort("Ranked Score", -1)
games_pulled_inclusion = mon_col.find(test_query).sort("Inclusion Score", -1)
games_pulled_average = mon_col.find(test_query).sort("Average Score", -1)

for game in games_pulled:
    print("We found one!")
    print(game)

print("Successfully completed! Have a good day!")