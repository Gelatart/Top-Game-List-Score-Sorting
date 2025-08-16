import sqlite3

#SQL_CLI seems to indicate the table is getting created but a lot of the fields are not populating properly

from .create_schema import create_schema
from .game_object import GameObject
#Use try, except, finally logic to deal with errors and close the connection?

class SQLManager:
    def __init__(self, db_path="games.db"):
        self.conn = sqlite3.connect(db_path)
        #Clear table at the start so we avoid any issues with unique constraints (should mongo do similar?)
        #Expand this to clear other tables later on so all is a blank slate?
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM games")
        create_schema(self.conn, db_path)
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
        ON CONFLICT(title) DO UPDATE SET
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
        ON CONFLICT(igdb_id) DO UPDATE SET
            igdb_id=excluded.igdb_id,
            title=excluded.title,
            ranked_score=excluded.ranked_score,
            list_source=excluded.list_source,
            total_count=excluded.total_count
        """, (
            game.igdb_ID,
            game.title,
            game.ranked_score,
            game.list_source,
            game.total_count
        ))
        self.conn.commit()

    def insert_or_update_game_full(self, game: GameObject):
        #right now only does the games table, expand this for the other tables too
        #ignore order_inserted for now because I don't know if we handle this or how we should
        #put function logic later for determining main_platform in terms of a tie? any way to determine best candidate?
        #make a function at some point that examines for suspect values in fields (ex: release dates on 1970)
        #print(game)
        self.cursor.execute("""
        INSERT INTO games (igdb_id, title, igdb_found, ranked_score, list_count, total_count, completed, release_date, main_platform, list_source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(igdb_id) DO UPDATE SET
            igdb_id=excluded.igdb_id,
            title=excluded.title,
            igdb_found = excluded.igdb_found,
            ranked_score=excluded.ranked_score,
            list_count=excluded.list_count,
            total_count=excluded.total_count,
            completed = excluded.completed,
            release_date = excluded.release_date,
            main_platform = excluded.main_platform,
            list_source=excluded.list_source
        """, (
            game.igdb_ID,
            game.title,
            game.igdb_found,
            game.ranked_score,
            game.list_count,
            game.total_count,
            game.completed,
            game.release_date,
            game.main_platform,
            game.list_source
        ))
        self.conn.commit()

    #make functions for inserting specific fields? have a base version needed and functions for all the others?

    def get_all_games(self):
        self.cursor.execute("SELECT * FROM games")
        return self.cursor.fetchall()

    def get_top_n_games(self, n=10):
        """
        Example of ORDER BY + LIMIT
        """
        self.cursor.execute("""
            SELECT title, igdb_id, ranked_score
            FROM games
            ORDER BY ranked_score DESC
            LIMIT ?
        """, (n,))
        return self.cursor.fetchall()

    def get_games_by_main_platform(self, platform_name):
        """
        Example of filtering results with WHERE
        """
        self.cursor.execute("""
            SELECT title, igdb_id, ranked_score, main_platform
            FROM games
            WHERE main_platform = ?
            ORDER BY ranked_score DESC
        """, (platform_name,))
        return self.cursor.fetchall()

    def get_games_with_developers(self):
        """
        Example of JOIN — assuming you have a 'developers' table
        """
        self.cursor.execute("""
            SELECT g.title, g.igdb_id, d.name AS developer
            FROM games g
            JOIN developers d ON g.developer_id = d.id
        """)
        return self.cursor.fetchall()

    def get_score_statistics(self):
        """
        Example of aggregation with GROUP BY
        """
        self.cursor.execute("""
            SELECT main_platform, COUNT(*) AS game_count, AVG(ranked_score) AS avg_score
            FROM games
            GROUP BY main_platform
        """)
        return self.cursor.fetchall()

    def union_example(self):
        #Seemingly not very helpful, just a random example I can build on?
        """
        Example of UNION — combine two queries
        """
        self.cursor.execute("""
            SELECT title FROM games WHERE ranked_score >= 90
            UNION
            SELECT title FROM games WHERE main_platform = 'PC'
        """)
        return self.cursor.fetchall()

    def clear_table(self):
        self.cursor.execute("DELETE FROM games")
        self.conn.commit()

    def close(self):
        self.conn.close()
