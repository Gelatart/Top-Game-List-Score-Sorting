from dataclasses import dataclass, field
import pytest
import os
from dotenv import load_dotenv
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#import src.Generator #change this to from...import... when I start having real functions in generator
from src.Generator import mongo_connect

class TestGenerator:

    load_dotenv()

    def test_mongo_connection(self):
        #mon_connect = os.getenv('MONGO_URI')
        #mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
        #monDB = mon_client["GameSorting"]
        #assert mon_client.admin.command('ping')
        #print("Pinged your deployment. You successfully connected to MongoDB!")
        assert mongo_connect() == "Pinged your deployment. You successfully connected to MongoDB!"

#Referencing this tutorial: https://betterstack.com/community/guides/testing/pytest-guide/