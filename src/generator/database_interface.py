import os

from .mongo_manager import MongoManager
from .sql_manager import SQLManager
from .game_object import GameObject

class DatabaseInterface:
    def __init__(self, use_mongo=False, use_sql=True, local_connect=True):
        """
        Initialize database managers based on env vars or flags.
        """
        self.use_sql = use_sql
        self.use_mongo = use_mongo
        self.local_connect = local_connect

        #self.mongo = MongoManager() if use_mongo else None #should it be self.use_mongo?
        #self.sql = SQLManager() if use_sql else None

        self.sql = None
        self.mongo = None

        """
        If you run with docker-compose up using the config ChatGPT drafted, your container will have:
            SQLITE_PATH=/app/data/games.db
            MONGO_URI=mongodb://mongo:27017/top_game_db    
        DatabaseInterface will detect those and connect properly.
        If you run locally without Docker, it just falls back to defaults (games.db in project root, and MongoAtlas?).
        """

        # SQLite setup
        if self.use_sql:
            sqlite_path = os.getenv("SQLITE_PATH", "data/games.db")
            os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
            self.sql = SQLManager(sqlite_path)
            self.sql.clear_table() #Figure out if I always need this?

        #MongoDB setup
        if self.use_mongo:
            if self.local_connect:
                mongo_uri = "mongodb://localhost:27017/top_game_db"
            else:
                mongo_uri = os.getenv("MONGO_URI")
                if not mongo_uri:
                    print("⚠️ No Atlas URI found in environment. Please set MONGO_URI in your .env file.")
            #mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/top_game_db")
            self.mongo = MongoManager(uri=mongo_uri)

    def insert_game_pre_ID(self, game: GameObject):
        """
        Insert game with minimal data (before IGDB enrichment).
        """
        if self.mongo:
            #see if want mongo to update to this pre and post IGDB ID logic?
            self.mongo.insert_or_update_game(game)
        if self.sql:
            self.sql.insert_or_update_game_pre_ID(game)

    def insert_game(self, game: GameObject):
        if self.mongo:
            self.mongo.insert_or_update_game(game)
        if self.sql:
            self.sql.insert_or_update_game(game)

    def insert_game_full(self, game: GameObject):
        """
        Insert full enriched game data.
        """
        if self.mongo:
            #have mongo have a split between full and minimum? unnecessary?
            self.mongo.insert_or_update_game(game)
            #print("Inserting game into MongoDB")
        if self.sql:
            #self.sql.insert_or_update_game_full(game)
            self.sql.insert_or_update_game_full_with_relations(game)
            #print("Inserting game into SQLite")

    def get_all_games(self):
        """
        TRY THIS?
        results = []
        if self.sql:
            results.extend(self.sql.get_all_games())
        if self.mongo:
            results.extend(self.mongo.get_all_games())
        return results
        """
        #split into mongo and sql functions so don't return both at same time?
        mongo_games = self.mongo.get_all_games() if self.mongo else []
        sql_games = self.sql.get_all_games() if self.sql else []
        return mongo_games, sql_games

    def clear_sql(self):
        self.sql.clear_table()

    def clear_all(self):
        if self.mongo:
            self.mongo.clear_collection()
        if self.sql:
            self.sql.clear_table()

    def close(self):
        if self.mongo:
            self.mongo.close()
        if self.sql:
            self.sql.close()
