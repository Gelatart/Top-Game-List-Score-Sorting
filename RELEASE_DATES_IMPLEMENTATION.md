# Release Dates Implementation

## Overview
This document describes the implementation of normalized release_dates support in the game aggregation system.

## Changes Made

### 1. Database Schema (`src/generator/create_schema.py`)
Already had the necessary tables:
- `release_dates` - stores individual release dates per game/platform/region
- `regions` - stores region names (Europe, North America, Japan, etc.)

### 2. Game Object (`src/generator/game_object.py`)
- Added `release_dates: list[dict]` field to store full release date information
- Kept `release_date: str` field for backward compatibility (stores earliest release)

### 3. IGDB Client (`src/generator/igdb_client.py`)
- Updated `parse_igdb_release_dates()` to parse IGDB release date data
- Modified IGDB queries to fetch: `release_dates.date, release_dates.platform.name, release_dates.region, release_dates.human`
- Updated `enrich_game_object()` to:
  - Parse all release dates from IGDB
  - Store them in `game.release_dates`
  - Calculate earliest release date for `game.release_date`

### 4. SQL Manager (`src/generator/sql_manager.py`)
- Added `get_or_create_region_id()` - maps IGDB region IDs to region names
- Added `get_platform_id_by_name()` - looks up platform IDs
- Added `get_release_dates_for_game()` - queries release dates with joins
- Updated `insert_or_update_game_full_with_relations()` to insert release dates into normalized table

## Data Flow

1. **IGDB API** returns release_dates array with:
   - `date` (unix timestamp)
   - `platform` (object with name)
   - `region` (IGDB region ID: 1-8)
   - `human` (human-readable string)

2. **IGDB Client** parses this into:
   ```python
   {
       "platform_name": "Nintendo Switch",
       "region_id": 2,  # North America
       "release_date": "2017-03-03",
       "human_readable": "Mar 03, 2017"
   }
   ```

3. **SQL Manager** inserts into database:
   - Creates/finds platform in `platforms` table
   - Creates/finds region in `regions` table
   - Inserts row into `release_dates` table with foreign keys

## IGDB Region IDs

| ID | Region |
|----|--------|
| 1  | Europe |
| 2  | North America |
| 3  | Australia |
| 4  | New Zealand |
| 5  | Japan |
| 6  | China |
| 7  | Asia |
| 8  | Worldwide |

## Usage Examples

### Query release dates for a game:
```python
db = DatabaseInterface(use_sql=True)
release_dates = db.sql.get_release_dates_for_game(game_id)
for date, platform, region, human in release_dates:
    print(f"{date} - {platform} ({region})")
```

### Access from game object:
```python
for rd in game.release_dates:
    print(f"{rd['release_date']} - {rd['platform_name']} - Region {rd['region_id']}")
```

## Testing

Run the test script:
```bash
python test_release_dates.py
```

This will:
1. Create a test game object
2. Fetch data from IGDB
3. Insert into SQLite
4. Query back the release dates

## Backward Compatibility

The `games.release_date` field is still populated with the earliest release date, so existing code that relies on this field will continue to work.

## Future Enhancements

- [ ] Add MongoDB support for release_dates
- [ ] Create views/reports that show games by region
- [ ] Add filtering by release date range in print_reports
- [ ] Cache platform lookups to reduce database queries
- [ ] Add support for release date status (announced, released, etc.)
