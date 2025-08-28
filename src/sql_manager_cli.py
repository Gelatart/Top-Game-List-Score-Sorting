import argparse
from tabulate import tabulate
from generator.game_object import GameObject
from generator.sql_manager import SQLManager

#Create an input interface where I can write out commands and keep running them

COMMANDS = [
    ("List all games", "list_games"),
    ("Get top N games by ranked score", "top_games"),
    ("Get games by platform", "games_by_platform"),
    ("Get games with developers", "games_with_developers"),
    ("Show score statistics grouped by platform", "score_stats"),
    ("Run UNION example query", "union_example"),
    ("Clear all games", "clear"),
    ("Run a custom SQL query", "run_sql"),
    ("Insert/Update game (pre-ID)", "insert_preid"),
    ("Insert/Update game (with IGDB ID)", "insert_id"),
    ("Show full denormalized game info", "full_game_info"),
]

def main():
    parser = argparse.ArgumentParser(
        description="Command line interface for interacting with the SQL Manager."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Basic Commands ---
    # Get all games
    subparsers.add_parser("list_games", help="List all games in the database")

    # Get top N games
    top_parser = subparsers.add_parser("top_games", help="Get top N games by ranked score")
    top_parser.add_argument("n", type=int, help="Number of top games to retrieve")

    # Get games filtered by platform
    platform_parser = subparsers.add_parser("games_by_platform", help="Get games for a specific platform")
    platform_parser.add_argument("platform", help="Platform name (e.g., 'PC')")

    # Get games with developers (JOIN)
    subparsers.add_parser("games_with_developers", help="Get games with developers (JOIN example)")

    # Get score statistics (GROUP BY / aggregation)
    subparsers.add_parser("score_stats", help="Show score statistics grouped by platform")

    # Run a UNION example
    subparsers.add_parser("union_example", help="Run UNION example query")

    # Clear the table
    subparsers.add_parser("clear", help="Clear all games from the database")

    # Run a freeform SQL query
    query_parser = subparsers.add_parser("run_sql", help="Run a custom SQL query")
    query_parser.add_argument("sql", help="SQL query string to execute")

    # --- Insert/Update Commands ---
    insert_preid_parser = subparsers.add_parser("insert_preid", help="Insert/Update a game (before IGDB ID)")
    insert_preid_parser.add_argument("title", help="Game title")
    insert_preid_parser.add_argument("ranked_score", type=int, help="Ranked score")
    insert_preid_parser.add_argument("list_source", help="Source file")
    insert_preid_parser.add_argument("total_count", type=int, help="Total count")

    insert_id_parser = subparsers.add_parser("insert_id", help="Insert/Update a game with IGDB ID")
    insert_id_parser.add_argument("igdb_id", type=int, help="IGDB ID")
    insert_id_parser.add_argument("title", help="Game title")
    insert_id_parser.add_argument("ranked_score", type=int, help="Ranked score")
    insert_id_parser.add_argument("list_source", help="Source file")
    insert_id_parser.add_argument("total_count", type=int, help="Total count")

    args = parser.parse_args()

    db = SQLManager("games.db")

    # Make SQLite rows behave like dicts
    db.conn.row_factory = sqlite3.Row
    db.cursor = db.conn.cursor()

    if args.command:
        run_command(db, args.command, args)
    else:
        """
        #Return to this as an alternate option? Choose if want to type out or do numbered entries
        # Interactive mode (REPL)
        print("Entering interactive mode. Type 'help' for commands, 'exit' to quit.")
        while True:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit"]:
                    break
                if user_input.lower() == "help":
                    parser.print_help()
                    continue

                # Parse user input into arguments
                args = parser.parse_args(user_input.split())
                run_command(db, args.command, args)

            except SystemExit:
                # argparse throws this when parsing fails
                print("Invalid command. Type 'help' to see available commands.")
            except Exception as e:
                print(f"Error: {e}")
        """
        interactive_menu(db)

    db.close()

def interactive_menu(db):
    # Interactive numbered menu
    print("=== SQL Manager Interactive CLI ===")
    while True:
        print("\nSelect an option:")
        for i, (desc, _) in enumerate(COMMANDS, 1):
            print(f"{i}. {desc}")
        print("0. Exit")

        choice = input("> ").strip()
        if not choice.isdigit():
            print("Please enter a number.")
            continue

        choice = int(choice)
        if choice == 0:
            break
        if not (1 <= choice <= len(COMMANDS)):
            print("Invalid choice.")
            continue

        desc, command = COMMANDS[choice - 1]
        args = argparse.Namespace(command=command)

        # Ask for arguments interactively
        if command == "top_games":
            args.n = int(input("Enter N: "))
        elif command == "games_by_platform":
            args.platform = input("Enter platform: ")
        elif command == "run_sql":
            args.sql = input("Enter SQL query: ")
        elif command == "insert_preid":
            args.title = input("Title: ")
            args.ranked_score = int(input("Ranked score: "))
            args.list_source = input("List source: ")
            args.total_count = int(input("Total count: "))
        elif command == "insert_full":
            args.igdb_id = int(input("IGDB ID: "))
            args.title = input("Title: ")
            args.ranked_score = int(input("Ranked score: "))
            args.list_source = input("List source: ")
            args.total_count = int(input("Total count: "))

        run_command(db, command, args)

def run_command(db, command, args):
    if command == "list_games":
        print_rows(db.get_all_games(), db.cursor)

    elif command == "top_games":
        print_rows(db.get_top_n_games(args.n), db.cursor)

    elif command == "games_by_platform":
        print_rows(db.get_games_by_main_platform(args.platform), db.cursor)

    elif command == "games_with_developers":
        print_rows(db.get_games_with_developers(), db.cursor)

    elif command == "score_stats":
        print_rows(db.get_score_statistics(), db.cursor)

    elif command == "union_example":
        print_rows(db.union_example(), db.cursor)

    elif command == "clear":
        confirm = input("Are you sure you want to clear all games? (y/n): ")
        if confirm.lower() == "y":
            db.clear_table()
            print("All games cleared.")

    elif command == "run_sql":
        try:
            db.cursor.execute(args.sql)
            #seems like this breaks right now after the select statement?
            #db.cursor.execute(args)
            print_rows(db.cursor.fetchall(), db.cursor)
        except Exception as e:
            print(f"SQL error: {e}")

    #get_or_create_id?

    elif command == "insert_preid":
        game = GameObject(
            title=args.title,
            ranked_score=args.ranked_score,
            list_source=args.list_source,
            total_count=args.total_count
        )
        db.insert_or_update_game_pre_ID(game)
        print(f"Inserted/Updated game (pre-ID): {args.title}")

    elif command == "insert_id":
        game = GameObject(
            igdb_ID=args.igdb_id,
            title=args.title,
            ranked_score=args.ranked_score,
            list_source=args.list_source,
            total_count=args.total_count
        )
        db.insert_or_update_game(game)
        print(f"Inserted/Updated game (IGDB-ID): {args.title}")

    #insert_or_update_game_full?
    #insert_or_update_game_full_with_relations?

    elif command == "full_game_info":
        #Currently this prints pretty ugly, with a lot of space at the end, and a bunch of dashes at the end, look into fixing?
        if hasattr(args, "game_id") and args.game_id:
            print_rows(db.get_full_game_info(game_id=args.game_id), db.cursor)
        else:
            #Let user set their own limit?
            print_rows(db.get_full_game_info(limit=5), db.cursor)

    else:
        print(f"Unknown command: {command}")

def print_rows(rows, cursor):
    if not rows:
        print("No results.")
        return
    # If using row_factory, rows are sqlite3.Row objects
    if isinstance(rows[0], sqlite3.Row):
        headers = rows[0].keys()
        data = [tuple(r) for r in rows]
    else:
        headers = [desc[0] for desc in cursor.description]
        data = rows
    print(tabulate(data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    import sqlite3
    main()