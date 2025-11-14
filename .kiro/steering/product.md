---
inclusion: always
---

---
inclusion: always
---

# Product Overview

Video game list aggregation and scoring system that processes curated "best games" lists from publications, websites, and user rankings to generate aggregate acclaim scores.

## Core Workflow

1. Parse text files from `game_lists/` (ranked/unranked/former)
2. Calculate scores based on list type and position
3. Enrich with IGDB API metadata (platforms, release dates, genres, themes, companies)
4. Store in SQLite (default) or MongoDB
5. Export reports (Excel, JSON, text)

## Scoring Rules

- **Ranked**: Top entry = N points (N = list size), decrementing by 1 per position
- **Unranked**: Each game = average score ((N+1)/2 points)
- **Former**: Reduced weight for discontinued/outdated lists

## Key Concepts

- **GameObject**: Core data structure representing a game with scores and metadata
- **Inclusion Score**: Count of how many lists mention a game
- **Ranked Score**: Sum of position-based points from ranked lists
- **Average Score**: Combined metric for overall ranking
- **IGDB Enrichment**: External API adds platform info, release dates, genres, themes, involved companies
- **Caching**: IGDB responses cached to minimize API calls and respect rate limits
