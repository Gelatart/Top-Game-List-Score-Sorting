import sqlite3

def create_schema(db_path="games.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # === Main Game Table ===
    cursor.execute("""
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
    )
    """)

    # === List File References ===
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lists_referencing (
        game_id INTEGER,
        source_file TEXT,
        FOREIGN KEY (game_id) REFERENCES games(id)
    )
    """)
    #Any other fields needed? How do I indicate which files list what games?

    # === Normalized Text Tables ===
    for table in ["genres", "themes", "player_modes", "platforms", "developers", "publishers", "companies"]:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

    # === Link Tables ===
    link_tables = {
        "game_genres": "genre_id",
        "game_themes": "theme_id",
        "game_player_modes": "mode_id",
        "game_platforms": "platform_id",
        "game_developers": "developer_id",
        "game_publishers": "publisher_id",
        "game_companies": "company_id"
    }

    for table, ref_id in link_tables.items():
        base = table.replace("game_", "").rstrip("s")  # genre, platform, etc.
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            game_id INTEGER,
            {ref_id} INTEGER,
            FOREIGN KEY (game_id) REFERENCES games(id),
            FOREIGN KEY ({ref_id}) REFERENCES {base}s(id)
        )
        """)

    conn.commit()
    conn.close()
    print("Database schema created.")

# Optional direct run
if __name__ == "__main__":
    create_schema()
