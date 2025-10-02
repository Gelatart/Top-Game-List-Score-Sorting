import sqlite3

from .config import get_env_var
from .create_schema import create_schema
from .game_object import GameObject
#Use try, except, finally logic to deal with errors and close the connection?

class SQLManager:
    def __init__(self, db_path="data/games.db"):
        self.conn = sqlite3.connect(db_path)
        #Clear table at the start so we avoid any issues with unique constraints (should mongo do similar?)
        #Expand this to clear other tables later on so all is a blank slate?
        self.cursor = self.conn.cursor()
        #self.cursor.execute("DELETE FROM games")
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

    def build_where_clause(self, filters: dict) -> tuple[str, list]:
        """
        Build a WHERE clause with operators.
        filters = {
            "ranked_score": (">", 80),
            "main_platform": ("!=", "PC"),
            "release_date": (">=", "2010-01-01"),
            "title": ("LIKE", "%Mario%"),
            "main_platform": ("IN", ["PC", "Switch"])
        }
        """
        clauses = []
        params = []
        print(filters)
        print(type(filters))
        for col, (op, val) in filters.items():
            op = op.upper()
            print(val)
            print(type(val))
            #if op == "IN" and isinstance(val, (list, tuple)):
            if op == "IN":
                placeholders = ",".join(["?"] * len(val))
                clauses.append(f"{col} IN ({placeholders})")
                params.extend(val)
            elif op in ["=", "!=", ">", "<", ">=", "<="]:
                clauses.append(f"{col} {op} ?")
                params.append(val)
            else:
                raise ValueError(f"Unsupported operator: {op}")

        where_clause = "WHERE " + " AND ".join(clauses) if clauses else ""
        return where_clause, params

    def calculate_column_expression(self, expression, filters=None, limit=None):
        """
        Calculate an arithmetic expression across columns.

        Example:
            expression = "ranked_score + list_count"
            expression = "ranked_score * 1.5"
            expression = "(total_count - list_count) / 2"

        filters = { "main_platform": ("=", "PC") }
        """
        base_query = f"""
            SELECT g.id, g.title, g.igdb_id, {expression} AS result
            FROM games g
        """
        where_clause, params = self.build_where_clause(filters or {})
        limit_clause = f" LIMIT {limit}" if limit else ""

        query = f"{base_query} {where_clause} {limit_clause}"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def calculate_aggregate_expression(self, expression, filters=None):
        """
        Run an aggregate arithmetic expression.
        Example: "AVG(ranked_score)", "SUM(total_count)", "MAX(ranked_score) - MIN(ranked_score)"
        """
        base_query = f"SELECT {expression} AS result FROM games g"
        where_clause, params = self.build_where_clause(filters or {})

        query = f"{base_query} {where_clause}"
        self.cursor.execute(query, params)
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

    def insert_or_update_game_full_with_relations(self, game: GameObject):
        # 1. Insert/update game row
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

        #2. Get the game_id for foreign key linking
        #Use title pre-IGDB pass, igdb_id after enriching?
        self.cursor.execute("SELECT id FROM games WHERE igdb_id=? OR title=?", (game.igdb_ID, game.title))
        #game_id = self.cursor.fetchone()[0]
        row = self.cursor.fetchone()
        if row:
            game_id = row[0]
        else:
            raise ValueError(f"Could not find game in database after insert: {game.title}")

        # 3. Insert genres into normalized tables + link table
        for genre in game.genres:
            genre_id = self.get_or_create_id("genres", genre)
            self.cursor.execute("INSERT OR IGNORE INTO game_genres (game_id, genre_id) VALUES (?, ?)",
                                (game_id, genre_id))

        # 4. Insert platforms
        for platform in game.list_platforms:
            platform_id = self.get_or_create_id("platforms", platform)
            self.cursor.execute("INSERT OR IGNORE INTO game_platforms (game_id, platform_id) VALUES (?, ?)",
                                (game_id, platform_id))

        # 5. Insert themes
        #input(game.themes)
        for theme in game.themes:
            theme_id = self.get_or_create_id("themes", theme)
            self.cursor.execute("INSERT OR IGNORE INTO game_themes (game_id, theme_id) VALUES (?, ?)",
                                (game_id, theme_id))

        # 6. Player Modes (game modes like single-player or multiplayer)
        #input(game.player_counts)
        for mode in game.player_counts:
            mode_id = self.get_or_create_id("player_modes", mode)
            self.cursor.execute("INSERT OR IGNORE INTO game_player_modes (game_id, mode_id) VALUES (?, ?)", (game_id, mode_id))

         # 7. Developers
        for dev in game.list_developers:
            dev_id = self.get_or_create_id("developers", dev)
            self.cursor.execute("INSERT OR IGNORE INTO game_developers (game_id, developer_id) VALUES (?, ?)", (game_id, dev_id))

        # 8. Publishers
        for pub in game.list_publishers:
            pub_id = self.get_or_create_id("publishers", pub)
            self.cursor.execute("INSERT OR IGNORE INTO game_publishers (game_id, publisher_id) VALUES (?, ?)", (game_id, pub_id))

        # 9. Companies (other involved companies that don’t neatly fit as dev/pub)
        for comp in game.list_companies:
            comp_id = self.get_or_create_id("companies", comp)
            self.cursor.execute("INSERT OR IGNORE INTO game_companies (game_id, company_id) VALUES (?, ?)", (game_id, comp_id))

        # 10. Lists Referencing
        # If game.list_source is a single string, you could normalize it here
        #sources = game.list_source if isinstance(game.list_source, list) else [game.list_source]
        #for src in sources:
        for ref_list in game.lists_referencing:
            self.cursor.execute("""
                INSERT OR IGNORE INTO lists_referencing (game_id, source_file)
                VALUES (?, ?)
            """, (game_id, ref_list))

        #themes and game_themes, player_modes and game_player_modes not properly grabbing?

        #getattr(game, "themes", []) method instead of game.themes can guard against errors if a gameobject doesn't have a list for the attributes?
        #could be more normalized to have developers and publishers unified into companies with a role field instead of a separate Table?
        #IGDB structures it that way too?
        #ordering could be done by adding extra column to link table for "role" or "priority"?

        self.conn.commit()

    #make functions for inserting specific fields? have a base version needed and functions for all the others?

    def get_all_games(self):
        self.cursor.execute("SELECT * FROM games")
        return self.cursor.fetchall()

    #def get_all_full_game_info(self, limit=25):
    def get_all_full_game_info(self, filters=None, limit=None):
        """
        Return a denormalized view of ALL games, joining related tables into comma-separated lists (with GROUP_CONCAT for related fields).
        Make a version that is limited to `limit` rows by default.
        """
        base_query = """
        SELECT
            g.id, g.title, g.igdb_id, g.ranked_score, g.total_count, g.release_date,
            g.main_platform, g.list_source,
            GROUP_CONCAT(DISTINCT genres.name) AS genres,
            GROUP_CONCAT(DISTINCT themes.name) AS themes,
            GROUP_CONCAT(DISTINCT player_modes.name) AS player_modes,
            GROUP_CONCAT(DISTINCT platforms.name) AS platforms,
            GROUP_CONCAT(DISTINCT developers.name) AS developers,
            GROUP_CONCAT(DISTINCT publishers.name) AS publishers,
            GROUP_CONCAT(DISTINCT companies.name) AS companies,
            GROUP_CONCAT(DISTINCT lr.source_file) AS referenced_in
        FROM games g
        LEFT JOIN game_genres       gg   ON g.id = gg.game_id
        LEFT JOIN genres            ON gg.genre_id = genres.id
        LEFT JOIN game_themes       gt   ON g.id = gt.game_id
        LEFT JOIN themes            ON gt.theme_id = themes.id
        LEFT JOIN game_player_modes gpm  ON g.id = gpm.game_id
        LEFT JOIN player_modes      ON gpm.mode_id = player_modes.id
        LEFT JOIN game_platforms    gp   ON g.id = gp.game_id
        LEFT JOIN platforms         ON gp.platform_id = platforms.id
        LEFT JOIN game_developers   gd   ON g.id = gd.game_id
        LEFT JOIN developers        ON gd.developer_id = developers.id
        LEFT JOIN game_publishers   gpub ON g.id = gpub.game_id
        LEFT JOIN publishers        ON gpub.publisher_id = publishers.id
        LEFT JOIN game_companies    gc   ON g.id = gc.game_id
        LEFT JOIN companies         ON gc.company_id = companies.id
        LEFT JOIN lists_referencing lr   ON g.id = lr.game_id
        """
        where_clause, params = self.build_where_clause(filters or {})
        group_by = " GROUP BY g.id"
        limit_clause = f" LIMIT {limit}" if limit else ""
        #LIMIT ?
        #self.cursor.execute(query, (limit,))
        query = f"{base_query} {where_clause} {group_by} {limit_clause}"
        self.cursor.execute(query, params)
        print(query)
        return self.cursor.fetchall()

    def get_full_game_info_by_id(self, game_id):
        """
        Get full denormalized info for a single game by internal game_id.
        """
        query = """
        SELECT
            g.id,
            g.title,
            g.igdb_id,
            g.ranked_score,
            g.total_count,
            g.release_date,
            g.main_platform,
            g.list_source,
            GROUP_CONCAT(DISTINCT genres.name) AS genres,
            GROUP_CONCAT(DISTINCT themes.name) AS themes,
            GROUP_CONCAT(DISTINCT player_modes.name) AS player_modes,
            GROUP_CONCAT(DISTINCT platforms.name) AS platforms,
            GROUP_CONCAT(DISTINCT developers.name) AS developers,
            GROUP_CONCAT(DISTINCT publishers.name) AS publishers,
            GROUP_CONCAT(DISTINCT companies.name) AS companies,
            GROUP_CONCAT(DISTINCT lr.source_file) AS referenced_in
        FROM games g
        LEFT JOIN game_genres gg ON g.id = gg.game_id
        LEFT JOIN genres      ON gg.genre_id = genres.id
        LEFT JOIN game_themes gt ON g.id = gt.game_id
        LEFT JOIN themes      ON gt.theme_id = themes.id
        LEFT JOIN game_player_modes gpm ON g.id = gpm.game_id
        LEFT JOIN player_modes ON gpm.mode_id = player_modes.id
        LEFT JOIN game_platforms gp ON g.id = gp.game_id
        LEFT JOIN platforms    ON gp.platform_id = platforms.id
        LEFT JOIN game_developers gd ON g.id = gd.game_id
        LEFT JOIN developers   ON gd.developer_id = developers.id
        LEFT JOIN game_publishers gpub ON g.id = gpub.game_id
        LEFT JOIN publishers   ON gpub.publisher_id = publishers.id
        LEFT JOIN game_companies gc ON g.id = gc.game_id
        LEFT JOIN companies    ON gc.company_id = companies.id
        LEFT JOIN lists_referencing lr ON g.id = lr.game_id
        WHERE g.id = ?
        GROUP BY g.id
        """
        self.cursor.execute(query, (game_id,))
        print(query)
        return self.cursor.fetchone()

    def get_full_game_info_by_title(self, title):
        """
        Get full denormalized info for a single game by its title.
        """
        query = """
        SELECT g.id FROM games g WHERE g.title = ?
        """
        self.cursor.execute(query, (title,))
        row = self.cursor.fetchone()
        if row:
            print(query)
            return self.get_full_game_info_by_id(row[0])
        return None

    def get_full_game_info_by_igdb_id(self, igdb_id):
        """
        Get full denormalized info for a single game by its IGDB ID.
        """
        query = """
        SELECT g.id FROM games g WHERE g.igdb_id = ?
        """
        self.cursor.execute(query, (igdb_id,))
        row = self.cursor.fetchone()
        if row:
            print(query)
            return self.get_full_game_info_by_id(row[0])
        return None

    def get_custom_columns(self, columns, limit=20):
        """
        Fetch custom-selected columns from the games table.
        :param columns: list of column names to select
        :param limit: max rows to return
        """
        if not columns:
            raise ValueError("You must provide at least one column.")

        col_str = ", ".join(columns)
        query = f"SELECT {col_str} FROM games ORDER BY g.ranked_score DESC LIMIT ?"
        self.cursor.execute(query, (limit,))
        print(query)
        return self.cursor.fetchall()

    def get_custom_columns_with_joins(self, columns, filters=None, limit=20):
        """
        Dynamically build a SELECT query with optional joins if columns
        from related tables are requested (genres, themes, etc).
        :param columns: list of column names (e.g. ["title", "ranked_score", "genres.name"])
        :param limit: max rows
        """
        if not columns:
            raise ValueError("You must provide at least one column.")

        base_cols = []
        joins = []
        join_map = {
            "genres": ("game_genres", "genre_id", "genres"),
            "themes": ("game_themes", "theme_id", "themes"),
            "player_modes": ("game_player_modes", "mode_id", "player_modes"),
            "platforms": ("game_platforms", "platform_id", "platforms"),
            "developers": ("game_developers", "developer_id", "developers"),
            "publishers": ("game_publishers", "publisher_id", "publishers"),
            "companies": ("game_companies", "company_id", "companies"),
        }

        # Check each column
        for col in columns:
            if "." in col:  # e.g. "genres.name"
                table, field = col.split(".", 1)
                if table in join_map:
                    link_table, fk, ref_table = join_map[table]
                    join_stmt = f"""
                    LEFT JOIN {link_table} ON games.id = {link_table}.game_id
                    LEFT JOIN {ref_table} ON {link_table}.{fk} = {ref_table}.id
                    """
                    if join_stmt not in joins:
                        joins.append(join_stmt)
                    base_cols.append(f"{ref_table}.{field} AS {table}_{field}")
                else:
                    raise ValueError(f"Unknown related table: {table}")
            else:
                base_cols.append(f"games.{col}")

        col_str = ", ".join(base_cols)
        join_str = " ".join(joins)
        where_clause, params = self.build_where_clause(filters)
        limit_clause = f" LIMIT {limit}" if limit else ""
        query = f"""
        SELECT {col_str}
        FROM games
        {join_str}
        {where_clause}
        ORDER BY games.ranked_score DESC
        {limit_clause}
        """
        #replace limit ? with limit_clause
        #self.cursor.execute(query, (limit,))
        print(query)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_top_n_games(self, n=10, filters=None):
        """
        Example of ORDER BY + LIMIT
        """
        base_query = """
            SELECT title, igdb_id, ranked_score
            FROM games
        """
        where_clause, params = self.build_where_clause(filters or {})
        #limit_clause = f" LIMIT {n}" if n else ""
        #^Put this in
        query = f"{base_query} {where_clause} ORDER BY ranked_score DESC LIMIT ?"
        params.append(n)
        self.cursor.execute(query, params)
        print(query)
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
