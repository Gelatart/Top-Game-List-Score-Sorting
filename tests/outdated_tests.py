import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#import igdb
from igdb.wrapper import IGDBWrapper
import requests

#import src.Generator #change this to from...import... when I start having real functions in generator
#from src.Generator import mongo_connect
#from src.Generator import check_for_src
#from src.IGDB_Query import query_build_func

#IGDB CREDENTIALS
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
post = f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
page = requests.post(post)  # gives access token we can use
print(page.text)
# wrapper = IGDBWrapper("YOUR_CLIENT_ID", "YOUR_APP_ACCESS_TOKEN")
received = json.loads(page.text)
access_token = received["access_token"]
print(access_token)
wrapper = IGDBWrapper(client_id, access_token)

class TestGenerator:

    load_dotenv()

    #Turn this into a mock test because of external logic
    #def test_mongo_connection(self):
        #Tests to make sure mongo connection works properly based on env details
        #Mongo connection doesn't seem to work on my netgear quite yet may need to configure

        #mon_connect = os.getenv('MONGO_URI')
        #mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
        #monDB = mon_client["GameSorting"]
        #assert mon_client.admin.command('ping')
        #print("Pinged your deployment. You successfully connected to MongoDB!")
        #assert mongo_connect() == "Pinged your deployment. You successfully connected to MongoDB!"

"""
igdb_request_1 = wrapper.api_request(
        'games.pb',
        "fields id, name; where name = 'Tetris';"
        )
igdb_request_2 = wrapper.api_request(
        'games.pb',
        "fields id, name; where name = 'Resident Evil';"
        )

@pytest.mark.parametrize(
    #try a way of passing in the actual os.getcwd()?
    "query_text, resulting_request",
    [
        ("fields id, name; where name = 'Tetris';", igdb_request_1),
        ("fields id, name; where name = 'Resident Evil';", igdb_request_2),
    ],
)
def test_query_build_func(query_text):
    assert test_query_build_func(query_text) == resulting_request

---
(These were in the TestGenerator class)

def test_meant_to_fail(self):
    assert mongo_connect() == "Haha, this test is going to fail!"

def check_for_src(potential_filename):
    cwd = os.getcwd()
    #input("We are currently in " + cwd)
    if_src = cwd[-3:]
    #input(if_src)
    if(if_src == "src"):
        potential_filename = "..\\" + potential_filename
    #input(potential_filename)
    return potential_filename

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