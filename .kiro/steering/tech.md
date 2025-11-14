---
inclusion: always
---

---
inclusion: always
---

# Tech Stack

## Language & Environment

- **Python 3.9+** (originally 3.10.9)
- Virtual environment: `venv` or Conda
- Environment variables: `.env` file (python-dotenv)

## Dependencies

- **Database**: sqlite3 (built-in), pymongo
- **Data**: pandas, numpy
- **API**: igdb-api-v4, requests, protobuf
- **Export**: openpyxl, xlwt
- **Parsing**: beautifulsoup4
- **Utilities**: python-dateutil, pathlib

## Database

- **SQLite** (default): `data/games.db` - relational with foreign keys
- **MongoDB** (optional): Atlas cloud or local - denormalized documents
- **DatabaseInterface**: Abstraction layer for swapping implementations

## IGDB API

- Enriches metadata: platforms, release dates, genres, themes, companies
- Auth: Twitch Client ID + Secret in `.env` (IGDB_CLIENT_ID, IGDB_CLIENT_SECRET)
- Rate limit: ~4 req/sec with 0.25s delays
- Protocol: Protocol Buffers (`.pb` endpoints)
- Caching: Responses stored in `igdb_cache.json`

## Docker

- `docker-compose.yaml`: app, mongo, mongo-express (web UI)
- MongoDB: `mongodb://localhost:27017`
- Note: Atlas connections may require VPN to be disabled

## Common Commands

```bash
# Virtual environment activation
source venv/bin/activate  # macOS/Linux
deactivate                # Exit venv

# Conda environment (legacy)
conda activate GameListScore
conda deactivate

# Run main program
python main.py

# Run specific modules
python -m src.generator.generator
python -m src.print_reports
python -m src.drop

# Docker
docker-compose up
docker-compose down

# Testing
pytest tests/
```

## Code Style

- Use `pathlib.Path` for file paths (cross-platform)
- CLI-based interaction (no GUI)
- Dataclasses for data structures (`GameObject`)
- IGDB queries use Protocol Buffers (`.pb` endpoints)
- Type hints where applicable
- Module execution: `python -m src.module_name`
