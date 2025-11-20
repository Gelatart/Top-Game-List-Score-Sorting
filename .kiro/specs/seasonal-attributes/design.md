# Design Document

## Overview

This design adds four independent boolean seasonal attributes to the GameObject class and integrates seasonal tagging throughout the data pipeline. Games can be tagged with one or more seasonal categories by maintaining text files similar to Completions.txt. The seasonal data flows through parsing, enrichment, database storage, and export phases.

## Architecture

The seasonal feature follows the existing pattern established by the `completed` attribute:

1. **Text File Storage**: Four seasonal text files in `game_lists/` directory
2. **Parsing Phase**: File loader reads seasonal files into sets
3. **Tagging Phase**: Generator marks GameObjects with seasonal flags after IGDB enrichment
4. **Persistence Phase**: Database managers store boolean values
5. **Export Phase**: Exporters include seasonal columns in output

## Components and Interfaces

### 1. GameObject (game_object.py)

Add four new boolean attributes to the GameObject dataclass:

```python
@dataclass
class GameObject:
    # ... existing attributes ...
    seasonal_spring: bool = False
    seasonal_summer: bool = False
    seasonal_fall_halloween: bool = False
    seasonal_winter_christmas: bool = False
```

These attributes:
- Default to `False` when a GameObject is created
- Are independent boolean flags (a game can have multiple set to `True`)
- Follow the same pattern as the existing `completed` attribute

### 2. File Loader (file_loader.py)

Update `read_attributed_games()` to handle missing files gracefully:

```python
def read_attributed_games(file_path: str) -> List[str]:
    """
    Return a list of game titles from a .txt file.
    This will start with Completions.txt, but could encompass other custom files with custom fields.
    Returns empty list if file doesn't exist.
    """
    full_path = check_for_src(file_path)
    if not os.path.exists(full_path):
        return []
    
    with open(full_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
```

**Design Decision**: Make `read_attributed_games()` handle missing files gracefully rather than creating a separate `read_seasonal_file_safe()` function. This:
- Benefits all optional attribute files (Completions.txt, seasonal files)
- Keeps the code DRY (Don't Repeat Yourself)
- Makes the generator code cleaner
- Prevents crashes if optional files are missing

Usage pattern in generator:
```python
spring_titles = set(read_attributed_games(Path("game_lists") / "Spring.txt"))
summer_titles = set(read_attributed_games(Path("game_lists") / "Summer.txt"))
fall_titles = set(read_attributed_games(Path("game_lists") / "Fall-Halloween.txt"))
winter_titles = set(read_attributed_games(Path("game_lists") / "Winter-Christmas.txt"))
```

### 3. Generator (generator.py)

Add seasonal tagging logic after the completion marking step (Step 4) and before IGDB enrichment:

```python
# Step 4: Mark completed games
for title in completed_titles:
    if title in game_DB:
        game_DB[title].completed = True

# Step 4.5: Mark seasonal games
spring_titles = set(read_attributed_games(Path("game_lists") / "Spring.txt"))
summer_titles = set(read_attributed_games(Path("game_lists") / "Summer.txt"))
fall_titles = set(read_attributed_games(Path("game_lists") / "Fall-Halloween.txt"))
winter_titles = set(read_attributed_games(Path("game_lists") / "Winter-Christmas.txt"))

for title in spring_titles:
    if title in game_DB:
        game_DB[title].seasonal_spring = True

for title in summer_titles:
    if title in game_DB:
        game_DB[title].seasonal_summer = True

for title in fall_titles:
    if title in game_DB:
        game_DB[title].seasonal_fall_halloween = True

for title in winter_titles:
    if title in game_DB:
        game_DB[title].seasonal_winter_christmas = True
```

**Design Decision**: Seasonal tagging happens before IGDB enrichment because:
- It only requires title matching, not IGDB data
- Follows the same pattern as completion marking
- Keeps the pipeline simple and predictable

### 4. SQL Manager (sql_manager.py)

#### Schema Changes (create_schema.py)

Add four boolean columns to the games table:

```sql
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
    seasonal_spring BOOLEAN DEFAULT 0,
    seasonal_summer BOOLEAN DEFAULT 0,
    seasonal_fall_halloween BOOLEAN DEFAULT 0,
    seasonal_winter_christmas BOOLEAN DEFAULT 0
);
```

#### Insert/Update Methods

Update all insert methods to include seasonal fields:

**insert_or_update_game_full():**
```python
self.cursor.execute("""
INSERT INTO games (igdb_id, title, igdb_found, ranked_score, list_count, total_count, completed, release_date,
                   seasonal_spring, seasonal_summer, seasonal_fall_halloween, seasonal_winter_christmas)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(igdb_id) DO UPDATE SET
    igdb_id=excluded.igdb_id,
    title=excluded.title,
    igdb_found = excluded.igdb_found,
    ranked_score=excluded.ranked_score,
    list_count=excluded.list_count,
    total_count=excluded.total_count,
    completed = excluded.completed,
    release_date = excluded.release_date,
    seasonal_spring = excluded.seasonal_spring,
    seasonal_summer = excluded.seasonal_summer,
    seasonal_fall_halloween = excluded.seasonal_fall_halloween,
    seasonal_winter_christmas = excluded.seasonal_winter_christmas
""", (
    game.igdb_ID,
    game.title,
    game.igdb_found,
    game.ranked_score,
    game.list_count,
    game.total_count,
    game.completed,
    game.release_date,
    game.seasonal_spring,
    game.seasonal_summer,
    game.seasonal_fall_halloween,
    game.seasonal_winter_christmas
))
```

**insert_or_update_game_full_with_relations():**
Same changes as above for the initial INSERT statement.

#### Query Methods

Update SELECT queries to include seasonal columns:

**get_all_full_game_info():**
```python
SELECT
    g.id, g.title, g.igdb_id, g.ranked_score, g.total_count, g.release_date,
    g.seasonal_spring, g.seasonal_summer, g.seasonal_fall_halloween, g.seasonal_winter_christmas,
    GROUP_CONCAT(DISTINCT genres.name) AS genres,
    ...
```

**get_full_game_info_by_id():**
Same SELECT clause changes as above.

**Design Decision**: Store as boolean (0/1) in SQLite rather than comma-separated strings because:
- Enables efficient filtering with WHERE clauses
- Matches the pattern used by `completed` attribute
- Supports Excel filtering requirements
- Simpler to query (e.g., `WHERE seasonal_spring = 1`)

### 5. MongoDB Manager (mongo_manager.py)

The existing `insert_or_update_game()` method uses `game.to_dict()` which automatically includes all GameObject attributes. No changes needed since the GameObject's `to_dict()` method will include the new seasonal fields.

MongoDB document structure:
```json
{
    "title": "Animal Crossing: New Horizons",
    "seasonal_spring": true,
    "seasonal_summer": true,
    "seasonal_fall_halloween": false,
    "seasonal_winter_christmas": false,
    ...
}
```

### 6. Exporter (exporter.py)

#### JSON Export

No changes needed. The `export_to_json()` function uses `game.to_dict()` which will automatically include seasonal attributes.

#### Excel Export

No changes needed. The `export_to_excel()` function dynamically reads headers from `game.to_dict().keys()` and will automatically include the four seasonal columns.

Excel output will have four boolean columns that support filtering:
- seasonal_spring
- seasonal_summer  
- seasonal_fall_halloween
- seasonal_winter_christmas

#### Text Export

No changes needed. The `export_to_text()` function only exports title, IGDB ID, and ranked score, intentionally excluding seasonal data per requirements.

## Data Models

### Seasonal Text Files

Location: `game_lists/Spring.txt`, `game_lists/Summer.txt`, `game_lists/Fall-Halloween.txt`, `game_lists/Winter-Christmas.txt`

Format (identical to Completions.txt):
```
Animal Crossing: New Horizons
<1070> Super Mario World
The Legend of Zelda: Breath of the Wild
```

- One game title per line
- Optional IGDB ID disambiguation using `<ID>` prefix
- UTF-8 encoding
- Empty lines ignored

### GameObject Structure

```python
@dataclass
class GameObject:
    title: str
    ranked_score: int
    total_count: int
    igdb_ID: Optional[int] = None
    igdb_found: bool = False
    list_count: int = 1
    lists_referencing: list[str] = field(default_factory=list)
    completed: bool = False
    seasonal_spring: bool = False
    seasonal_summer: bool = False
    seasonal_fall_halloween: bool = False
    seasonal_winter_christmas: bool = False
    # ... other existing attributes ...
```

### Database Schema

**SQLite:**
```sql
CREATE TABLE games (
    -- existing columns --
    seasonal_spring BOOLEAN DEFAULT 0,
    seasonal_summer BOOLEAN DEFAULT 0,
    seasonal_fall_halloween BOOLEAN DEFAULT 0,
    seasonal_winter_christmas BOOLEAN DEFAULT 0
);
```

**MongoDB:**
```json
{
    "seasonal_spring": false,
    "seasonal_summer": false,
    "seasonal_fall_halloween": false,
    "seasonal_winter_christmas": false
}
```

## Error Handling

### Missing Seasonal Files

The updated `read_attributed_games()` function handles missing files gracefully by returning an empty list. This means:
- If a seasonal file doesn't exist, no games will be tagged with that season
- No error or warning is raised
- The generator continues processing normally
- Same behavior applies to Completions.txt if it's missing

### Title Matching

- Uses exact string matching (case-sensitive)
- Supports IGDB ID disambiguation with `<ID>` prefix
- If a title in a seasonal file doesn't match any game in game_DB, it's silently skipped (same behavior as Completions.txt)

### Database Migration

For existing databases:
- SQLite: ALTER TABLE statements will add new columns with DEFAULT 0
- MongoDB: New fields will be added on next insert/update (schema-less)
- Existing records will have seasonal fields set to False/0

## Testing Strategy

### Unit Tests

1. **GameObject Tests** (test_game_object.py)
   - Verify seasonal attributes default to False
   - Verify multiple seasonal flags can be True simultaneously
   - Verify to_dict() includes seasonal attributes

2. **File Loader Tests** (test_file_loader.py)
   - Verify read_attributed_games() works with seasonal files
   - Test with IGDB ID disambiguation
   - Test with empty files

3. **SQL Manager Tests** (test_sql_manager.py)
   - Verify schema includes seasonal columns
   - Test insert with seasonal data
   - Test query methods return seasonal data
   - Test filtering by seasonal attributes

### Integration Tests

1. **End-to-End Pipeline**
   - Create test seasonal files
   - Run generator
   - Verify GameObjects have correct seasonal flags
   - Verify database contains seasonal data
   - Verify exports include seasonal columns

2. **Multiple Seasons**
   - Add same game to multiple seasonal files
   - Verify all corresponding flags are set to True

3. **Excel Export**
   - Verify four boolean columns appear
   - Verify columns can be filtered in Excel

## Implementation Notes

### File Naming Convention

- `Spring.txt` - Spring-themed games
- `Summer.txt` - Summer-themed games
- `Fall-Halloween.txt` - Fall and Halloween-themed games
- `Winter-Christmas.txt` - Winter and Christmas-themed games

**Design Decision**: Use descriptive filenames that clearly indicate the season. The hyphenated names (Fall-Halloween, Winter-Christmas) group related themes together.

### Attribute Naming Convention

- `seasonal_spring`
- `seasonal_summer`
- `seasonal_fall_halloween`
- `seasonal_winter_christmas`

**Design Decision**: Use `seasonal_` prefix to:
- Clearly indicate these are seasonal attributes
- Group them together in alphabetical listings
- Distinguish from other boolean attributes like `completed`
- Use underscores for Python naming convention

### Processing Order

1. Parse all game lists (ranked, unranked, former)
2. Mark completed games
3. **Mark seasonal games** ← New step
4. Enrich with IGDB data
5. Save to database
6. Export results

**Design Decision**: Seasonal marking happens early in the pipeline because:
- Only requires title matching (no IGDB data needed)
- Follows the same pattern as completion marking
- Ensures seasonal data is available for all subsequent operations

### Backward Compatibility

- Existing code that doesn't use seasonal attributes will continue to work
- GameObject's to_dict() automatically includes new attributes
- Database queries that don't filter by season will return all games
- Exports will include seasonal columns but can be ignored by existing consumers
