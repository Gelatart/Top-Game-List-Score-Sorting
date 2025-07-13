import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv

print("Welcome to Mongo-Query!")

#Load the env variables from .env
load_dotenv()

#implementing a mongo check now or later element like in printreports

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

while True:
    export_dict = {}
    print()
    print("What kind of Mongo querying would you like to do?")
    print("1. Write out a specific Mongo query")
    print("2. Build up a mongo query through command line options (Coming soon)")
    print("3. Quit the program")
    mongo_option = input()
    if(mongo_option == '1'):
        #Write out your full query
        while True:
            print("Alright! Please write out your query below by key and value!\n")
            full_query_key = input("Enter key: ")
            full_query_value = input("Enter value: ")
            export_dict[full_query_key] = full_query_value
            #games_pulled = mon_col.find(full_query) #.sort("Ranked Score", -1) <- Do we have to ask to add sorting, or can that be handled on its own?
            games_pulled = mon_col.find(export_dict)
            #Add in options for how we filter the data we grab?
            for game in games_pulled:
                print(game)
                print()
            while True:
                print("Would you like to keep using this mode? Or go back to the main menu?")
                print("1. Keep using this mode")
                print("2. Go back to the main menu")
                maintain_option = input()
                if(maintain_option == '1'):
                    print("Alright, keeping to this mode")
                    continue
                elif(maintain_option == '2'):
                    print("Alright, returning to the main menu")
                    break
                else:
                    print("I'm sorry, I don't understand. Please use valid input")
                    continue
    elif (mongo_option == '2'):
        # Build up a query through command line options
        print("Great!...Unfortunately we have not coded this part in yet, so you'll have to try it again later!")
        break
    elif (mongo_option == '3'):
        #Quit the program
        print("Alright, quitting the program")
        break
    else:
        print("I'm sorry, I don't understand your selection at this time")
        continue

#Close connection to open up socket
mon_client.close()

print("Successfully completed! Have a good day!")

"""
REFERENCES:
Adding user input into dictionary: https://www.geeksforgeeks.org/how-to-add-user-input-to-a-dictionary-in-python/#
"""