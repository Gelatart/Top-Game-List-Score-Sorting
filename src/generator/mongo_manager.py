from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .config import get_env_var
from .game_object import GameObject

class MongoManager:
    def __init__(self, uri=None, db_name="GameSorting", collection_name="games"):
        self.uri = uri or get_env_var("MONGO_URI")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_or_update_game(self, game: GameObject):
        game_dict = game.to_dict()
        self.collection.update_one(
            {"IGDB ID": game.igdb_ID},
            {"$set": game_dict},
            upsert=True
        )

    def get_all_games(self):
        return list(self.collection.find())

    def clear_collection(self):
        self.collection.delete_many({})

    def close(self):
        self.client.close()