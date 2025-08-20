import argparse
from generator.sql_manager import SQLManager

#Create an input interface where I can write out commands and keep running them

def main():
    parser = argparse.ArgumentParser(
        description="Command line interface for interacting with the SQL Manager."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Commands ---
    # Get all games
    subparsers.add_parser("get_all_games", help="List all games in the database")

    # Get top N games
    top_parser = subparsers.add_parser("top_games", help="Get top N games by ranked score")
    top_parser.add_argument("n", type=int, help="Number of top games to retrieve")

    # Get games filtered by platform
    platform_parser = subparsers.add_parser("games_by_platform", help="Get games for a specific platform")
    platform_parser.add_argument("platform", help="Platform name (e.g., 'PC')")

    # Get score statistics
    subparsers.add_parser("score_stats", help="Show score statistics grouped by platform")

    # Run a UNION example
    subparsers.add_parser("union_example", help="Run UNION example query")

    # Clear the table
    subparsers.add_parser("clear", help="Clear all games from the database")

    args = parser.parse_args()

    db = SQLManager("games.db")

    if args.command == "get_all_games":
        results = db.get_all_games()
        for row in results:
            print(row)

    elif args.command == "top_games":
        results = db.get_top_n_games(args.n)
        for row in results:
            print(row)

    elif args.command == "games_by_platform":
        results = db.get_games_by_main_platform(args.platform)
        for row in results:
            print(row)

    elif args.command == "score_stats":
        results = db.get_score_statistics()
        for row in results:
            print(row)

    elif args.command == "union_example":
        results = db.union_example()
        for row in results:
            print(row)

    elif args.command == "clear":
        confirm = input("Are you sure you want to clear all games? (y/n): ")
        if confirm.lower() == "y":
            db.clear_table()
            print("All games cleared.")

    else:
        parser.print_help()

    db.close()

if __name__ == "__main__":
    main()
