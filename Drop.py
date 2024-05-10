#NEEDED IMPORTS?
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#import dotenv
from dotenv import load_dotenv
from dotenv import dotenv_values

#DROPPING PROCESS BEGINS
load_dotenv()
monConnect = os.getenv('MONGO_URI')
#file = open('var.env', 'r', encoding="utf-8")
file = open('.env', 'r', encoding="utf-8")
fileContents = file.read()
print(fileContents)
file.close()
#config = dotenv_values(".env")
print(f"MonConnect:{monConnect}")
monClient = pymongo.MongoClient(monConnect, server_api=ServerApi('1'))
monDB = monClient["GameSorting"]
try:
    monClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Uh-oh!")
    print(e)
mon_col = monDB["games"]
listCol = monDB["lists"]
mon_col.drop()
listCol.drop()
print("Successfully dropped the games collection!")
print("Successfully dropped the lists collection!")

"REFERENCES:"
"How to print file contents in Python: https://blog.finxter.com/how-to-print-the-content-of-a-txt-file-in-python/"
"Loading env as a dictionary: https://www.python-engineer.com/posts/dotenv-python/"
"Working off of just .env: https://www.reddit.com/r/learnpython/comments/qw6msy/cant_see_my_environment_variable_when_using/"