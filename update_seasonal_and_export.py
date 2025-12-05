#!/usr/bin/env python3
"""
Script to update seasonal attributes in the database and regenerate exports.
This is for testing task 6 of the seasonal-attributes spec.
"""

import sqlite3
from pathlib import Path
from src.generator.file_loader import read_attributed_games
from src.generator.sql_manager import SQLManager
from src.generator.exporter import export_to_json, export_to_excel, export_to_text

def update_seasonal_attributes():
    """Read seasonal files and update database with seasonal tags."""
    print("=" * 60)
    print("Updating Seasonal Attributes in Database")
    print("=" * 60)
    
    # Read seasonal files
    print("\nReading seasonal files...")
    spring_titles = set(read_attributed_games(Path("game_lists") / "Spring.txt"))
    summer_titles = set(read_attributed_games(Path("game_lists") / "Summer.txt"))
    fall_titles = set(read_attributed_games(Path("game_lists") / "Fall-Halloween.txt"))
    winter_titles = set(read_attributed_games(Path("game_lists") / "Winter-Christmas.txt"))
    
    print(f"  Spring: {len(spring_titles)} games")
    print(f"  Summer: {len(summer_titles)} games")
    print(f"  Fall/Halloween: {len(fall_titles)} games")
    print(f"  Winter/Christmas: {len(winter_titles)} games")
    
    # Connect to database
    print("\nConnecting to database...")
    conn = sqlite3.connect("data/games.db")
    cursor = conn.cursor()
    
    # Reset all seasonal flags first
    print("Resetting seasonal flags...")
    cursor.execute("""
        UPDATE games SET 
            seasonal_spring = 0,
            seasonal_summer = 0,
            seasonal_fall_halloween = 0,
            seasonal_winter_christmas = 0
    """)
    
    # Update seasonal flags
    update_count = 0
    
    print("\nUpdating seasonal flags...")
    for title in spring_titles:
        cursor.execute("UPDATE games SET seasonal_spring = 1 WHERE title = ?", (title,))
        if cursor.rowcount > 0:
            update_count += 1
    
    for title in summer_titles:
        cursor.execute("UPDATE games SET seasonal_summer = 1 WHERE title = ?", (title,))
        if cursor.rowcount > 0:
            update_count += 1
    
    for title in fall_titles:
        cursor.execute("UPDATE games SET seasonal_fall_halloween = 1 WHERE title = ?", (title,))
        if cursor.rowcount > 0:
            update_count += 1
    
    for title in winter_titles:
        cursor.execute("UPDATE games SET seasonal_winter_christmas = 1 WHERE title = ?", (title,))
        if cursor.rowcount > 0:
            update_count += 1
    
    conn.commit()
    
    # Verify updates
    cursor.execute("""
        SELECT COUNT(*) FROM games 
        WHERE seasonal_spring = 1 
           OR seasonal_summer = 1 
           OR seasonal_fall_halloween = 1 
           OR seasonal_winter_christmas = 1
    """)
    seasonal_game_count = cursor.fetchone()[0]
    
    print(f"✓ Updated {update_count} seasonal flags")
    print(f"✓ {seasonal_game_count} games now have seasonal attributes")
    
    conn.close()
    return seasonal_game_count

def export_from_database():
    """Export games from database to JSON, Excel, and text formats."""
    print("\n" + "=" * 60)
    print("Exporting Data")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect("data/games.db")
    cursor = conn.cursor()
    
    # Get all games with seasonal data
    cursor.execute("""
        SELECT 
            title, igdb_id, igdb_found, ranked_score, list_count, total_count,
            completed, release_date,
            seasonal_spring, seasonal_summer, seasonal_fall_halloween, seasonal_winter_christmas
        FROM games
        ORDER BY ranked_score DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\nFetched {len(rows)} games from database")
    
    # Convert to GameObject-like dicts for export
    from src.generator.game_object import GameObject
    
    games = []
    for row in rows:
        game = GameObject(
            title=row[0],
            ranked_score=row[3],
            total_count=row[5],
            igdb_ID=row[1],
            igdb_found=bool(row[2]),
            list_count=row[4],
            completed=bool(row[6]),
            release_date=row[7],
            seasonal_spring=bool(row[8]),
            seasonal_summer=bool(row[9]),
            seasonal_fall_halloween=bool(row[10]),
            seasonal_winter_christmas=bool(row[11])
        )
        games.append(game)
    
    # Export to all formats
    print("\nExporting to files...")
    export_to_json(games, "reports/games.json")
    print("  ✓ JSON: reports/games.json")
    
    export_to_excel(games, "reports/games.xlsx")
    print("  ✓ Excel: reports/games.xlsx")
    
    export_to_text(games, "reports/games.txt")
    print("  ✓ Text: reports/games.txt")
    
    # Count seasonal games
    seasonal_games = [g for g in games if any([
        g.seasonal_spring, g.seasonal_summer, 
        g.seasonal_fall_halloween, g.seasonal_winter_christmas
    ])]
    
    print(f"\n✓ Exported {len(games)} total games")
    print(f"✓ {len(seasonal_games)} games have seasonal attributes")
    
    return len(games), len(seasonal_games)

def main():
    """Main function to update seasonal data and export."""
    try:
        # Update seasonal attributes in database
        seasonal_count = update_seasonal_attributes()
        
        # Export from database
        total_games, seasonal_games = export_from_database()
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS")
        print("=" * 60)
        print(f"Database updated with seasonal attributes")
        print(f"Exports regenerated with seasonal data")
        print(f"Ready for verification testing")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
