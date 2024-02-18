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
file = open('var.env', 'r', encoding="utf-8")
fileContents = file.read()
print(fileContents)
file.close()
config = dotenv_values(".env")
print(config)
print(monConnect)
print(f"MonConnect:{monConnect}")
monClient = pymongo.MongoClient(monConnect)
monDB = monClient["GameSorting"]
try:
    monClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
monCol = monDB["games"]
monCol.drop()
print("Successfully dropped the games collection!")

"REFERENCES:"
"How to print file contents in Python: https://blog.finxter.com/how-to-print-the-content-of-a-txt-file-in-python/"
"Loading env as a dictionary: https://www.python-engineer.com/posts/dotenv-python/"