import sqlite3

from .create_schema import create_schema
from .game_object import GameObject
#Use try, except, finally logic to deal with errors and close the connection?

class SQLManager:
    def __init__(self, db_path="games.db"):
        create_schema(db_path)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        #self._create_table()

    #Have a first pass to grab from IGDB just ID's for all of the games and create a basic table off that
    #Then the optional second pass to grab the rest of the attributes we will need
    #Have a function to temporarily create IGDB ID's before the IGDB pass? Just autoincrementing?
    #Have a bool flag that shows if id's are temp or real?
    def _create_table(self):
        #id INTEGER PRIMARY KEY AUTOINCREMENT,
        #title TEXT UNIQUE,
        #Changing it so id is the primary key that we autoincrement
        #but I might want to try to use igdb_ID as the primary key later when we have it?
        #keep new id as the primary key for simplicity's sake and not having to spend time on IGDB until we need it
        #maybe make igdb_id a secondary key?
        #keep IGDB ID <> in part of title at start
        #have later function to go through and look for games with that, and update title, but keep unique ID?
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            igdb_found BOOLEAN,
            igdb_id INTEGER UNIQUE,
            ranked_score INTEGER,
            list_count INTEGER,
            total_count INTEGER,
            completed BOOLEAN,
            release_date TEXT,
            main_platform TEXT,
            list_source TEXT,
            order_inserted INTEGER
        );
        """)
        #Make release_date a datetime value instead?
        #Do I actually want an order_inserted value? Is it useful?
        self.conn.commit()

    def get_or_create_id(self, table, name):
        self.cursor.execute(f"INSERT OR IGNORE INTO {table}(name) VALUES (?)", (name,))
        self.cursor.execute(f"SELECT id FROM {table} WHERE name=?", (name,))
        return self.cursor.fetchone()[0]

    def insert_or_update_game_pre_ID(self, game: GameObject):
        self.cursor.execute("""
        INSERT INTO games (title, ranked_score, list_source, total_count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            ranked_score=excluded.ranked_score,
            list_source=excluded.list_source,
            total_count=excluded.total_count
        """, (
            game.title,
            game.ranked_score,
            game.list_source,
            game.total_count
        ))
        self.conn.commit()

    def insert_or_update_game(self, game: GameObject):
        self.cursor.execute("""
        INSERT INTO games (igdb_id, title, ranked_score, list_source, total_count)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            igdb_id=excluded.igdb_id,
            title=excluded.title,
            ranked_score=excluded.ranked_score,
            list_source=excluded.list_count,
            total_count=excluded.total_count
        """, (
            game.igdb_ID,
            game.title,
            game.ranked_score,
            game.list_source,
            game.total_count
        ))
        self.conn.commit()

    #make functions for inserting specific fields? have a base version needed and functions for all the others?

    def get_all_games(self):
        self.cursor.execute("SELECT * FROM games")
        return self.cursor.fetchall()

    def clear_table(self):
        self.cursor.execute("DELETE FROM games")
        self.conn.commit()

    def close(self):
        self.conn.close()
