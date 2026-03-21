# Phase 1 Analysis: Refactoring Gap Report

## Overview

`generator.py` currently has two coexisting IGDB pipelines and two coexisting export/database pipelines. The new approach is largely complete and correct. The old approach is dead weight — but it contains a few edge cases and behaviors worth preserving before deletion.

---

## 1. IGDB Enrichment: Old vs New

### Old approach (lines ~240–560 in generator.py)
- Uses `IGDBWrapper` + Protocol Buffers (`.pb` endpoints)
- Manually constructs query strings with `fields *; exclude ...`
- Handles `<ID>` prefix by extracting ID with regex and querying `where id = <ID>`
- Has two branches: `len(games) > 1` and `len(games) == 1`
- The `len(games) > 1` branch is entirely gutted — all logic is replaced with `# REMOVING THIS PART` comments
- The `len(games) == 1` branch still has partial logic (platforms loop, but all other fields also marked `# REMOVING THIS PART`)
- Uses `import_DB` to skip already-enriched games when `scratch_answer == False` — but `import_DB` is always empty `{}`, so this never actually worked
- Rate limiting: manual `time.sleep()` not present in old section (only in new section)
- Pauses with `input()` when a game is not found ("Maybe you need to alter the title somehow?")

### New approach (`IGDB_Client.enrich_game_object()`)
- Uses `IGDBWrapper` with JSON endpoints (not `.pb`)
- Handles `<ID>` prefix correctly via `search_game_by_ID()`
- Handles title search via `search_game_by_title()` with unicode normalization
- Populates: `igdb_ID`, `igdb_found`, `release_date`, `release_dates` (full list), `list_platforms`, `genres`, `themes`, `player_counts`, `list_developers`, `list_publishers`, `list_companies`
- Caches by IGDB ID via `CacheManager`
- Rate limiting: `time.sleep(0.25)` in the new generator loop

### Coverage verdict
The new approach covers **all fields** the old approach ever populated. The old approach's `len(games) > 1` branch was already gutted. The new approach is strictly better.

### One behavior to preserve
The old approach paused on "not found" games with `input()`. The new approach silently skips them. This is actually better behavior for batch processing — no action needed, but worth noting.

---

## 2. Bugs Found in Current New Code

### Bug 1: `load_list` does not track `lists_referencing` for new games
```python
# In load_list():
if title not in game_DB:
    game_DB[title] = GameObject(title, ranked_score=score, total_count=total)
    # BUG: lists_referencing is never populated for first-seen games
else:
    game = game_DB[title]
    game.ranked_score += score
    game.total_count += total
    game.list_count += 1
    game.lists_referencing.append(filepath)  # only appended on subsequent appearances
```
The first time a game is seen, `filepath` is never added to `lists_referencing`. Every game's first list reference is silently dropped. The old code (`alt_generator.py`) correctly passed the filepath to the constructor.

### Bug 2: `file_count` is not mutated back to caller
```python
def load_list(files, file_count, game_DB, games_lists, type: ListType):
    for filepath in files:
        file_count += 1  # mutates local copy only — int is passed by value
```
`ranked_file_count`, `unranked_file_count`, `former_file_count` are always 0 when printed at the end. The counts printed are meaningless. Fix: return the count, or use a mutable container.

### Bug 3: `generate_sorted_reports` is called twice
```python
# In run_generator():
generate_sorted_reports(export_list)   # line ~780
# ... old export code ...
generate_sorted_reports(export_list)   # line ~810 — duplicate call
```
The sorted report files get written twice. Second call is redundant.

### Bug 4: `input(print(...))` at the end
```python
input(print(f"Successfully processed and stored {len(export_list)} games."))
```
`print()` returns `None`, so this calls `input(None)` which displays `None` as the prompt. Should be two separate statements.

### Bug 5: Old MongoDB section runs unconditionally after new DB section
After the new `db.insert_game()` loop and `db.close()`, there is:
```python
input("FROM THIS PART ONWARD CLEAR MONGO BITS, ONLY ATTEMPT MONGO CONNECTION IF WE INTEND SO")
```
This `input()` call blocks execution every single run, then the old MongoDB code below it references `mon_col` and `list_col` which are never defined in the new flow — this would crash if the `input()` were ever removed.

---

## 3. Database Operations: Old vs New

### Old approach (lines ~630–720)
- Manually constructs `export_dict` with hardcoded field names
- Calls `mon_col.insert_one(export_dict)` — but `mon_col` is never defined in the new flow
- Has prompts to clear the database and set a mongo limit
- Inserts game lists into a `list_col` collection

### New approach (`DatabaseInterface`)
- `insert_game()` → minimal insert (igdb_id, title, ranked_score, total_count)
- `insert_game_full()` → full insert via `insert_or_update_game_full_with_relations()` which handles all normalized tables: genres, themes, platforms, player_modes, developers, publishers, companies, lists_referencing, release_dates
- `clear_all()` / `clear_sql()` available but not called in the new flow (SQLManager auto-clears on init via `self.sql.clear_table()`)
- List tracking: `games_lists` is collected but never inserted into any database in the new flow

### Missing behavior to preserve
The old code inserted the list of source files into a MongoDB `lists` collection. The new `DatabaseInterface` has no equivalent. The `games_lists` list is populated but goes unused after the new flow. This is low priority (it was MongoDB-only) but worth noting.

---

## 4. Export: Old vs New

### Old approach
- `xlwt` workbook with columns: Title, IGDB ID, Ranked Score, Inclusion Score, Average Score, Lists Included On, Completed, Main Platform, List of Platforms, Release Date, Player Counts, Developers, Publishers, Companies, Genres, Themes
- Crossed-out style for completed games
- Saved as `.xls` (old format)
- Pulled data from MongoDB cursor (`games_pulled`)

### New approach (`exporter.py`)
- `export_to_excel()` uses `openpyxl`, saves as `.xlsx`
- Headers derived dynamically from `game.to_dict().keys()`
- No crossed-out style for completed games (minor visual regression)
- `export_to_json()` and `export_to_text()` also present
- `generate_sorted_reports()` writes 6 sorted `.txt` files (ranked, inclusion, average × completed/uncompleted)

### Coverage verdict
New approach covers all data fields. The only regression is the crossed-out Excel style for completed games — cosmetic, low priority.

### Note on `to_dict()`
`GameObject.to_dict()` joins all lists into comma-separated strings. This is fine for Excel/text export but means the dict loses list structure. The method also has a bug: it mutates `self.__dict__` in place (uses `result = self.__dict__` not a copy), which would corrupt the object if called more than once. Should use `result = dict(self.__dict__)`.

---

## 5. Imports: What's Unused in the New Flow

These imports at the top of `generator.py` are only needed by the old code:
- `import pymongo` — old mongo connect
- `from pymongo.mongo_client import MongoClient` — old mongo connect
- `from pymongo.server_api import ServerApi` — old mongo connect
- `import xlwt` / `from xlwt import Workbook` — old Excel export
- `import itertools` — only used in old `itertools.islice()` loop
- `import json` — used in old IGDB section (new approach uses `igdb_client.py`)
- `import requests` — used in old IGDB section (new approach uses `igdb_client.py`)

The `IGDBWrapper` import is missing from `generator.py` but referenced in the old section — it would crash if that section ran. The new approach correctly uses `IGDB_Client` from `igdb_client.py`.

---

## 6. `<ID>` Prefix Handling

Old approach: regex extracts ID, queries `where id = <ID>`, strips `<ID> ` from title for display.
New approach (`igdb_client.py`): same regex logic, calls `search_game_by_ID()`.

The new approach handles this correctly. One subtle difference: the old approach tried to strip the `<ID>` prefix from the title before storing in MongoDB. The new approach stores the raw title (with `<ID>` prefix) in the database. This is a minor cosmetic issue — the title in the DB will have `<1070> Super Mario World` instead of `Super Mario World`.

---

## 7. `modified_DB` — Declared, Never Used

```python
modified_DB = {}
```
Declared at the top of `run_generator()`, never written to or read from in the new flow. Was intended to hold renamed `<ID>` entries. Can be safely deleted.

---

## 8. `import_DB` — Declared, Never Used

```python
import_DB = {}
```
Declared mid-function with comment "eventually try for functionality where we only update games that have updated scores". Never populated. The old code checked `if game in import_DB` but since it's always empty, the check always fell through. Can be safely deleted.

---

## Summary: What the New Approach Is Missing or Has Wrong

| Issue | Severity | Action Needed |
|---|---|---|
| Bug: `lists_referencing` not set for first-seen games | High | Fix in `load_list()` |
| Bug: `file_count` not returned from `load_list()` | Low | Fix or remove the counts |
| Bug: `generate_sorted_reports()` called twice | Low | Remove duplicate call |
| Bug: `input(print(...))` at end | Low | Split into two lines |
| Bug: `to_dict()` mutates `self.__dict__` in place | Medium | Fix in `game_object.py` |
| Old IGDB section blocks with `input()` every run | Critical | Remove in Phase 2 |
| Old MongoDB section references undefined `mon_col` | Critical | Remove in Phase 2 |
| `<ID>` prefix not stripped from stored title | Low | Optional cleanup |
| `games_lists` collected but never stored to DB | Low | Optional: add to SQL schema |
| Crossed-out Excel style for completed games missing | Cosmetic | Optional in Phase 4 |
| Unused imports (pymongo, xlwt, itertools, etc.) | Low | Remove in Phase 5 |
| `modified_DB` and `import_DB` unused variables | Low | Remove in Phase 5 |

---

## What Is Safe to Delete (confirmed no unique functionality)

- Entire old IGDB section (lines ~240–560): all logic either gutted or superseded by `IGDB_Client`
- Entire old MongoDB export section (lines ~630–720): superseded by `DatabaseInterface`
- Old Excel generation (lines ~770–830): superseded by `exporter.py`
- `mongo_connect()` function: superseded by `MongoManager` / `DatabaseInterface`
- All `# REMOVING THIS PART` comment blocks
- `modified_DB`, `import_DB` variables
- `wb = Workbook()` / `sheet1` variables (old xlwt setup at top of `run_generator()`)
