import argparse
import sys
from tabulate import tabulate
from generator.game_object import GameObject
from generator.sql_manager import SQLManager

#Create an input interface where I can write out commands and keep running them

#Do we have the options to selectively build out AND/OR conditions?
#Does like support matching with single characters with _?
#Provide support for DISTINCT functionality?
#Provide support for ORDER BY functionality?
#Make sure all commands allow for limits where that makes sense?
#Provide support for OFFSET functionality?
#Make sure we support different join types?
#-Already done inner join? Because equivalent to standard join?
#Add support for left join, right join, full join

COMMANDS = [
    ("Show all games (basic)", "list_games"),
    ("Show all games (full joined info)", "list_games_full"),
    ("Show a game's full info (by ID)", "show_game_id"),
    ("Show a game's full info (by Title)", "show_game_title"),
    ("Show a game's full info (by IGDB ID)", "show_game_igdb"),
    ("Custom SELECT (choose columns)", "custom_columns"),
    ("Custom SELECT (choose columns) (with joins)", "custom_columns_joins"),
    ("Select a group of columns as aliases", "alias_columns"),
    ("Select columns from any table and have joins automatically determined", "auto_columns"),
    ("Preset queries (genres, themes, platforms, etc.)", "preset_queries"),
    ("Insert/Update game (pre-ID)", "insert_preid"),
    ("Insert/Update game (with IGDB ID)", "insert_id"),
    ("Get top N games by ranked score", "top_games"),
    ("Get games by main platform", "games_by_platform"),
    ("Get games with developers", "games_with_developers"),
    ("Show score statistics grouped by platform", "score_stats"),
    ("Calculate arithmetic expression across columns (per row)s", "build_arithmetic"),
    ("Calculate aggregate expression (AVG, SUM, etc.)", "build_aggregate"),
    ("Run UNION example query", "union_example"),
    ("Clear all games", "clear"),
    ("Run a custom SQL query", "run_sql"),
]

def get_filters_from_user():
    """
    Interactive filter builder for WHERE clauses.
    Returns dict like:
    {"ranked_score": (">", 80), "title": ("LIKE", "%Mario%"), "platform": ("IN", ["PC", "Switch"])}
    """
    filters = {}
    print("\nAdd filters? (y/n)")
    if input("> ").strip().lower() != "y":
        return filters

    while True:
        col = input("Column name (or 'done'): ").strip()
        #Put in ability for it to interpret columns simply like "player_modes" and not having to indicate the table it's from?
        #Add functionality for joins to be pulled in if the column calls for it?
        if col.lower() == "done":
            break
        op = input("Operator (=, !=, >, <, >=, <= ) for basics\nOperator (LIKE, IN, BETWEEN, IS NULL) for advanced (NOT toggle comes later): ").strip().upper()
        #Keep to the more basic ones for now, have like and such be separate? actually include the new ones?
        #val = input("Value (for IN, separate with commas): ").strip()
        if op == "LIKE":
            #LOOK AT LIKE FUNCTION I SET UP BEFORE
            not_toggle = input("Use NOT LIKE instead? (y/n): ").strip().lower()
            if not_toggle == "y":
                op = "NOT LIKE"

            val = input("Enter pattern (use % as wildcard, e.g. %Mario%): ").strip()
            #CONSIDER: ci = input("Case-insensitive? (y/n): ").strip().lower() == "y"
            #limit handled elsewhere?
            filters[col] = (op, val)
        elif op == "IN":
            not_toggle = input("Use NOT IN instead? (y/n): ").strip().lower()
            if not_toggle == "y":
                op = "NOT IN"

            raw = input("Enter comma-separated values: ").strip()
            vals = [v.strip() for v in raw.split(",")]
            filters[col] = (op, vals)
        elif op == "BETWEEN":
            not_toggle = input("Use NOT BETWEEN instead? (y/n): ").strip().lower()
            if not_toggle == "y":
                op = "NOT BETWEEN"

            start = input("Start value: ").strip()
            end = input("End value: ").strip()
            #val = (start, end)
            filters[col] = (op, (start, end))
        elif op == "IS NULL":
            not_toggle = input("Use NOT NULL  instead? (y/n): ").strip().lower()
            if not_toggle == "y":
                op = "IS NOT NULL"

            filters[col] = (op, None)
        else:
            val = input("Value: ").strip()
            if val.isdigit():
                # If numeric, convert to int
                val = int(val)
            filters[col] = (op, val)
        #filters[col] = (op, val)

    return filters
def build_arithmetic_expression():
    """
    Interactive builder for arithmetic expressions.
    """
    print("\n=== Arithmetic Expression Builder ===")
    print("You can build expressions like: ranked_score + list_count")
    print("Available operators: +, -, *, /")
    print("Type 'done' when finished.\n")

    #Add better support for aggregate expression building? Spin off separate similar function for that?

    tokens = []
    while True:
        token = input("Enter column name, number, or operator (+ - * /): ").strip()
        if token.lower() == "done":
            break
        tokens.append(token)

    expression = " ".join(tokens)
    print(f"\nFinal expression: {expression}")
    return expression


def main():
    parser = argparse.ArgumentParser(
        description="Command line interface for interacting with the SQL Manager."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Basic Commands ---
    # Get all games
    subparsers.add_parser("list_games", help="List all games in the database")

    subparsers.add_parser("list_games_full", help="List all games in the database and all of their data from all tables")
    subparsers.add_parser("show_game_id", help="Get full denormalized info for a single game by internal game_id")
    subparsers.add_parser("show_game_title", help="Get full denormalized info for a single game by its title")
    subparsers.add_parser("show_game_igdb", help="Get full denormalized info for a single game by its IGDB ID")
    subparsers.add_parser("custom_columns", help="Fetch custom-selected columns from the games table")
    subparsers.add_parser("custom_columns_joins", help="Dynamically build a SELECT query with optional joins if columns from related tables are requested (genres, themes, etc)")
    subparsers.add_parser("alias_columns", help="Fetch custom-selected columns from the games table, with user-selected aliases")
    subparsers.add_parser("auto_columns",help="Automatically build SELECT query with JOINs based on requested columns.")
    #PUT IN THE REST OF THE NEW FUNCTIONS HERE!!!
    #...

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

    #Build arithmetic expressions
    subparsers.add_parser("build_arithmetic", help="Calculate arithmetic expression across columns (per row)")

    # Build aggregate expressions
    subparsers.add_parser("build_aggregate", help="Calculate aggregate expression (AVG, SUM, etc.)")

    # Run a UNION example
    subparsers.add_parser("union_example", help="Run UNION example query")

    # Clear the table
    subparsers.add_parser("clear", help="Clear all games from the database")

    # Run a freeform SQL query
    query_parser = subparsers.add_parser("run_sql", help="Run a custom SQL query")
    query_parser.add_argument("sql", help="SQL query string to execute")

    preset_parser = subparsers.add_parser("preset_queries", help="Preset queries (genres, themes, platforms, etc.)")
    # ^preset_parser = subparsers.add_parser...
    preset_parser.add_argument("filters", help="Filters for WHERE clause, format: column,operator,value")

    # --- Insert/Update Commands ---
    insert_preid_parser = subparsers.add_parser("insert_preid", help="Insert/Update a game (before IGDB ID)")
    insert_preid_parser.add_argument("title", help="Game title")
    insert_preid_parser.add_argument("ranked_score", type=int, help="Ranked score")
    insert_preid_parser.add_argument("total_count", type=int, help="Total count")

    insert_id_parser = subparsers.add_parser("insert_id", help="Insert/Update a game with IGDB ID")
    insert_id_parser.add_argument("igdb_id", type=int, help="IGDB ID")
    insert_id_parser.add_argument("title", help="Game title")
    insert_id_parser.add_argument("ranked_score", type=int, help="Ranked score")
    insert_id_parser.add_argument("total_count", type=int, help="Total count")

    args = parser.parse_args()

    db = SQLManager("data/games.db")
    #input("Test")
    #print(db.db_path)

    # Make SQLite rows behave like dicts
    db.conn.row_factory = sqlite3.Row
    db.cursor = db.conn.cursor()

    # if a command is passed on the command line, run once and exit
    if args.command:
        run_command(db, args.command, args)
        db.close()
        return
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
        if command == "list_games":
            args.limit = input("Enter limit (optional): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else None
        elif command == "list_games_full":
            args.limit = input("Limit results? (leave blank for no limit): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else None
            args.filters = get_filters_from_user()
        elif command == "show_game_id":
            args.id = int(input("Enter game_id: "))
        elif command == "show_game_title":
            args.title = input("Enter title: ")
        elif command == "show_game_igdb":
            args.igdb_id = input("Enter IGDB ID: ")
        elif command == "custom_columns":
            args.cols = input("Enter column names separated by commas: ").strip().split(",")
            args.cols = [c.strip() for c in args.cols if c.strip()]
            args.limit = input("Limit results (default 20): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else 20
        elif command == "custom_columns_joins":
            args.cols = input("Enter column names (comma-separated, e.g. title, ranked_score, genres.name): ").strip().split(",")
            args.cols = [c.strip() for c in args.cols if c.strip()]
            args.limit = input("Limit results (default 20): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else 20
        elif command == "alias_columns":
            args.cols = input("Enter columns (comma-separated): ").strip().split(",")
            args.cols = [c.strip() for c in args.cols]

            alias_choice = input("Do you want aliases? (y/n): ").strip().lower()
            args.aliases = None
            if alias_choice == "y":
                args.aliases = input("Enter aliases (comma-separated): ").strip().split(",")
                args.aliases = [a.strip() for a in args.aliases]

            args.joins = []
            add_joins = input("Do you want to add JOINs? (y/n): ").strip().lower()
            while add_joins == "y":
                table = input("Enter join table: ").strip()
                condition = input(f"Enter join condition (e.g., games.id = {table}.game_id): ").strip()
                args.joins.append((table, condition))
                add_joins = input("Add another JOIN? (y/n): ").strip().lower()

            args.limit = input("Enter limit (optional): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else None
        elif command == "auto_columns":
            args.cols = input("Enter columns (comma-separated): ").strip().split(",")
            args.cols = [c.strip() for c in args.cols]

            args.limit = input("Enter limit (optional): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else None
        elif command == "preset_queries":
            print("Choose a preset query:")
            print("1. Games with genres")
            print("2. Games with themes")
            print("3. Games with platforms")
            print("4. Games with developers")
            print("5. Games with publishers")
            print("6. Games with companies")
            preset = input("> ").strip()

            presets_map = {
                "1": ["title", "ranked_score", "genres.name"],
                "2": ["title", "ranked_score", "themes.name"],
                "3": ["title", "ranked_score",  "platforms.name"],
                "4": ["title", "ranked_score",  "developers.name"],
                "5": ["title", "ranked_score",  "publishers.name"],
                "6": ["title", "ranked_score",  "companies.name"],
            }

            if preset not in presets_map:
                print("Invalid choice.")
            else:
                args.cols = presets_map[preset]
                print(f"Do you want to add filters? (y/n)")
                filter_choice = input("> ").strip().lower()

                if filter_choice == "y":
                    args.filters = get_filters_from_user()
                    print(args.filters)

                args.limit = input("Limit results (default 20): ").strip()
                args.limit = int(args.limit) if args.limit.isdigit() else 20
        elif command == "top_games":
            args.n = int(input("How many top games?: "))
            args.filters = get_filters_from_user()
        elif command == "games_by_platform":
            args.platform = input("Enter platform: ")
        elif command == "games_with_developers":
            args.limit = input("Limit results (default 20): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else 20
        elif command == "build_arithmetic":
            args.expression = build_arithmetic_expression()
            args.filters = get_filters_from_user()
            args.limit = input("Limit results (default 20): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else None
        elif command == "build_aggregate":
            args.expression = build_arithmetic_expression()
            args.filters = get_filters_from_user()
            args.limit = input("Limit results (default 20): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else None
        elif command == "union_example":
            args.limit = input("Limit results (default 20): ").strip()
            args.limit = int(args.limit) if args.limit.isdigit() else 20
        elif command == "run_sql":
            args.sql = input("Enter SQL query: ")
        elif command == "insert_preid":
            args.title = input("Title: ")
            args.ranked_score = int(input("Ranked score: "))
            args.total_count = int(input("Total count: "))
        elif command == "insert_full":
            args.igdb_id = int(input("IGDB ID: "))
            args.title = input("Title: ")
            args.ranked_score = int(input("Ranked score: "))
            args.total_count = int(input("Total count: "))

        run_command(db, command, args)

def run_command(db, command, args):
    if command == "list_games":
        print_rows(db.get_all_games(args.limit), db.cursor)

    #make a version of this that actually does take a limit, in between all and one
    elif command == "list_games_full":
        #Seems this can take a real long time except if more filtered down?
        #Might end up hanging?
        #Provide a way to show progress to user, whether it is making progress or just getting stuck
        print_rows(db.get_all_full_game_info(filters=args.filters,limit=args.limit), db.cursor)

    elif command == "show_game_id":
        print_rows(db.get_full_game_info_by_id(args.id), db.cursor)

    elif command == "show_game_title":
        print_rows(db.get_full_game_info_by_title(args.title), db.cursor)

    elif command == "show_game_igdb":
        print_rows(db.get_full_game_info_by_igdb_id(args.igdb_id), db.cursor)

    elif command == "custom_columns":
        print_rows(db.get_custom_columns(args.cols, args.limit), db.cursor)

    elif command == "custom_columns_joins":
        try:
            print(f"Selected columns: {args.cols}")
            print_rows(db.get_custom_columns_with_joins(args.cols, args.filters, args.limit), db.cursor)
        except Exception as e:
            print(f"Error: {e}")

    elif command == "alias_columns":
        print_rows(db.alias_select(args.cols, args.aliases, args.joins, args.limit), db.cursor)

    elif command == "auto_columns":
        print_rows(db.auto_custom_select(args.cols, args.limit), db.cursor)

    elif command == "preset_queries":
        print(f"Preset query results for {args.cols}:")
        filters = getattr(args, "filters", None) or {}
        print_rows(db.get_custom_columns_with_joins(args.cols, filters, args.limit), db.cursor)

    elif command == "insert_preid":
        game = GameObject(
            title=args.title,
            ranked_score=args.ranked_score,
            total_count=args.total_count
        )
        db.insert_or_update_game_pre_ID(game)
        print(f"Inserted/Updated game (pre-ID): {args.title}")

    elif command == "insert_id":
        game = GameObject(
            igdb_ID=args.igdb_id,
            title=args.title,
            ranked_score=args.ranked_score,
            total_count=args.total_count
        )
        db.insert_or_update_game(game)
        print(f"Inserted/Updated game (IGDB-ID): {args.title}")

    elif command == "top_games":
        print_rows(db.get_top_n_games(args.n, args.filters), db.cursor)

    #WE WILL WANT TO FIX THIS COMMAND TO GO WITH MORE DERIVED LOGIC RATHER THAN JUST HAVING FIELD FOR IT
    elif command == "games_by_platform":
        print_rows(db.get_games_by_main_platform(args.platform), db.cursor)

    elif command == "games_with_developers":
        print_rows(db.get_games_with_developers(args.limit), db.cursor)

    elif command == "score_stats":
        print_rows(db.get_score_statistics(), db.cursor)

    elif command == "build_arithmetic":
        print_rows(db.calculate_column_expression(args.expression,filters=args.filters,limit=args.limit), db.cursor)

    elif command == "build_aggregate":
        result = db.calculate_aggregate_expression(args.expression,filters=args.filters,limit=args.limit)
        print("Aggregate result:", result)

    elif command == "union_example":
        print_rows(db.union_example(args.limit), db.cursor)

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

    #insert_or_update_game_full?
    #insert_or_update_game_full_with_relations?

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