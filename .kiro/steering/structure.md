---
inclusion: always
---

---
inclusion: always
---

# Project Structure

## Entry Points

- **main.py**: CLI menu hub for all operations

## Core Modules (`src/generator/`)

- **generator.py**: Main pipeline orchestrator - parses lists, calculates scores, enriches data, saves to DB
- **game_object.py**: `GameObject` dataclass - core data structure with scores and metadata
- **file_loader.py**: Parses text files from `game_lists/` (ranked/unranked/former)
- **igdb_client.py**: IGDB API client with rate limiting (~4 req/sec)
- **cache_manager.py**: IGDB response caching (JSON file-based)
- **database_interface.py**: Abstraction layer for SQLite/MongoDB
- **sql_manager.py**: SQLite operations and schema
- **mongo_manager.py**: MongoDB operations
- **exporter.py**: Export to JSON, Excel, text
- **config.py**: Environment variables and path utilities
- **create_schema.py**: Database schema definitions

## Utility Scripts (`src/`)

- **alt_generator.py**: Incremental generator (only processes new lists)
- **print_reports.py**: Generate custom reports from database
- **print_reports_listings.py**: Keeps track of lists of CLI options for print_reports
- **Drop.py**: Database cleanup utility
- **quick_math.py**: Personal hours tracking (unrelated to main project)
- **IGDB_Query.py**: CLI tool for testing IGDB API queries
- **mongo_query.py**: CLI tool for testing MongoDB queries
- **sql_cli.py**: SQLite command-line interface
- **sql_manager_cli.py**: SQLite management CLI

## Data Organization

### `game_lists/`
- **ranked/**: Position-based scoring (1st place = N points, last = 1 point)
- **unranked/**: Equal weight scoring (all entries = average points)
- **former/**: Discontinued lists (reduced weight)
- **Completions.txt**: Personal completion tracking

### `data/`
- **games.db**: SQLite database (default storage)

### `reports/`

- Generated output files (Excel, JSON, text)
- Sorted databases by various criteria

## Configuration

- **.env**: API keys, database URIs (not in repo)
- **.env.example**: Template for required environment variables
- **requirements.txt**: Python dependencies
- **docker-compose.yaml**: Container orchestration

## Testing (`tests/`)

- Unit tests for core modules
- Test files follow `test_*.py` naming convention
- Uses pytest framework

## Special Naming Conventions

- **`<ID>` prefix in lists**: IGDB ID disambiguation (e.g., `<1070> Super Mario World`)
- Use when title matching is ambiguous

## Architecture Patterns

- **DatabaseInterface**: Unified API for SQLite/MongoDB - swap implementations without changing business logic
- **GameObject**: Single source of truth for game data structure
- **Caching**: IGDB responses cached in `igdb_cache.json` to minimize API calls
- **Path handling**: Use `pathlib.Path` for cross-platform compatibility; `config.check_for_src()` adjusts relative paths
