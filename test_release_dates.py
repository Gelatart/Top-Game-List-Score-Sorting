#!/usr/bin/env python3
"""
Quick test script to verify release_dates implementation
"""

from src.generator.game_object import GameObject
from src.generator.igdb_client import IGDB_Client
from src.generator.database_interface import DatabaseInterface

def test_release_dates():
    print("Testing release_dates implementation...")
    
    # Create a test game object
    game = GameObject(
        title="The Legend of Zelda: Breath of the Wild",
        ranked_score=100,
        total_count=100
    )
    
    print(f"\n1. Created game object: {game.title}")
    print(f"   Initial release_date: {game.release_date}")
    print(f"   Initial release_dates: {game.release_dates}")
    
    # Test IGDB enrichment
    print("\n2. Fetching data from IGDB...")
    client = IGDB_Client()
    client.enrich_game_object(game)
    
    print(f"   IGDB ID: {game.igdb_ID}")
    print(f"   Main release_date: {game.release_date}")
    print(f"   Number of release dates: {len(game.release_dates)}")
    
    if game.release_dates:
        print("\n   Release dates details:")
        for i, rd in enumerate(game.release_dates[:5], 1):  # Show first 5
            print(f"     {i}. Platform: {rd.get('platform_name', 'N/A')}")
            print(f"        Region: {rd.get('region_id', 'N/A')}")
            print(f"        Date: {rd.get('release_date', 'N/A')}")
            print(f"        Human: {rd.get('human_readable', 'N/A')}")
    
    # Test database insertion
    print("\n3. Testing database insertion...")
    db = DatabaseInterface(use_mongo=False, use_sql=True)
    db.insert_game_full(game)
    
    print("   ✓ Game inserted into SQLite")
    
    # Query back the release dates
    print("\n4. Querying release_dates from database...")
    db.sql.cursor.execute("""
        SELECT rd.release_date, p.name as platform, r.name as region, rd.human_readable
        FROM release_dates rd
        LEFT JOIN platforms p ON rd.platform_id = p.id
        LEFT JOIN regions r ON rd.region_id = r.id
        WHERE rd.game_id = (SELECT id FROM games WHERE igdb_id = ?)
        LIMIT 5
    """, (game.igdb_ID,))
    
    results = db.sql.cursor.fetchall()
    if results:
        print(f"   Found {len(results)} release dates in database:")
        for date, platform, region, human in results:
            print(f"     - {date} | {platform or 'N/A'} | {region or 'N/A'} | {human or 'N/A'}")
    else:
        print("   No release dates found in database")
    
    db.close()
    print("\n✓ Test completed successfully!")

if __name__ == "__main__":
    test_release_dates()
