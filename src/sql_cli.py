import sqlite3

#Give an option to use SQL manager rather than directly write commands?

def run_sql_cli(db_path="games.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"Connected to {db_path}")
    print("Type SQL commands and press Enter. Type 'exit' to quit.")

    while True:
        cmd = input("SQL> ")
        if cmd.strip().lower() in ("exit", "quit"):
            break
        try:
            cursor.execute(cmd)
            if cmd.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            else:
                conn.commit()
                print("Query executed successfully.")
        except Exception as e:
            print(f"Error: {e}")

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    run_sql_cli()