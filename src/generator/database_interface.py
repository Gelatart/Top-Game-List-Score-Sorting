from .mongo_manager import MongoManager
from .sql_manager import SQLManager
from .game_object import GameObject

class DatabaseInterface:
    def __init__(self, use_mongo=False, use_sql=True):
        self.mongo = MongoManager() if use_mongo else None
        self.sql = SQLManager() if use_sql else None
        if use_sql:
            self.sql.clear_table()

    def insert_game_pre_ID(self, game: GameObject):
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
        if self.mongo:
            #have mongo have a split between full and minimum? unnecessary?
            self.mongo.insert_or_update_game(game)
            print("Inserting game into MongoDB")
        if self.sql:
            #self.sql.insert_or_update_game_full(game)
            self.sql.insert_or_update_game_full_with_relations(game)
            print("Inserting game into SQLite")

    def get_all_games(self):
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
