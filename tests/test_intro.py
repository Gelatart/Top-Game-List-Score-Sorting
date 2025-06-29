from dataclasses import dataclass, field
import pytest
import os
from dotenv import load_dotenv
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from igdb.wrapper import IGDBWrapper

#import src.Generator #change this to from...import... when I start having real functions in generator
from src.Generator import mongo_connect
from src.Generator import check_for_src
from src.IGDB_Query import query_build_func

def test_non_class_test():
    #This one exists just so we can call it with :: from the command line and not have to worry about being part of a class
    assert("Test") == "Test"

class TestGenerator:

    load_dotenv()

    def test_mongo_connection(self):
        #Tests to make sure mongo connection works properly based on env details
        #Mongo connection doesn't seem to work on my netgear quite yet may need to configure

        #mon_connect = os.getenv('MONGO_URI')
        #mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
        #monDB = mon_client["GameSorting"]
        #assert mon_client.admin.command('ping')
        #print("Pinged your deployment. You successfully connected to MongoDB!")
        assert mongo_connect() == "Pinged your deployment. You successfully connected to MongoDB!"

    """
    def test_meant_to_fail(self):
        assert mongo_connect() == "Haha, this test is going to fail!"
    """

    """
    def check_for_src(potential_filename):
    cwd = os.getcwd()
    #input("We are currently in " + cwd)
    if_src = cwd[-3:]
    #input(if_src)
    if(if_src == "src"):
        potential_filename = "..\\" + potential_filename
    #input(potential_filename)
    return potential_filename
    """
    """
    FUNCTIONS IN CLASS APPROACH
    def test_src_text_found_from_root(self):
        #Tests to make sure function can find src in the name it is passed and adjust accordingly
        #Style that should be matching if running from root folder
        assert check_for_src("Generator.py") == "Generator.py"

    def test_src_text_found_from_src(self):
        #Tests to make sure function can find src in the name it is passed and adjust accordingly
        #Style that should be matching if running from src folder
        assert check_for_src("Generator.py") == "..\Generator.py"
    """

@pytest.mark.parametrize(
    #try a way of passing in the actual os.getcwd()?
    "query_text, resulting_request",
    [
        ("fields *; where name = 'Tetris';",wrapper.api_request(
        'games.pb',
        "fields *; where name = 'Tetris';"
        )),
        ("fields *; where name = 'Resident Evil';",wrapper.api_request(
        'games.pb',
        "fields *; where name = 'Resident Evil';"
        )),
    ],
)
def test_query_build_func(query_text):
    assert test_query_build_func(query_text) == resulting_request

#Referencing this tutorial: https://betterstack.com/community/guides/testing/pytest-guide/