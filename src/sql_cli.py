import sqlite3

#Give an option to use SQL manager rather than directly write commands?

def run_sql_cli(db_path="games.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"Connected to {db_path}")
    print("Type SQL commands and press Enter. Type 'exit' or 'quit' to quit.")

    while True:
        query = input("SQL> ").strip()
        if query.lower() in ("exit", "quit"):
            break
        try:
            cursor.execute(query)
            if query.lower().startswith("select"):
                rows = cursor.fetchall()
                #Get column names
                col_names = [desc[0] for desc in cursor.description]
                print(" | ".join(col_names))
                print("-" * (len(" | ".join(col_names))))
                for row in rows:
                    #print(row)
                    print(" | ".join(str(val) if val is not None else "NULL" for val in row))
            else:
                conn.commit()
                print("Query executed successfully.")
        except Exception as e:
            print(f"Error: {e}")

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    run_sql_cli()