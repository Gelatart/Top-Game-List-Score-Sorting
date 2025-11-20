# Requirements Document

## Introduction

This feature adds seasonal categorization to games in the aggregation system. Games can be tagged with one or more seasonal attributes (Spring, Summer, Fall/Halloween, Winter/Christmas) based on their thematic content, setting, or release timing. This allows for seasonal filtering and reporting of games, similar to how the existing Completions tracking works.

## Glossary

- **GameObject**: The core data structure representing a game with scores and metadata
- **Seasonal Attribute**: A categorical tag indicating a game's association with a specific season
- **Seasonal Text File**: A plain text file listing game titles for a specific season, similar to Completions.txt
- **Generator**: The main pipeline orchestrator that parses lists and creates GameObject instances
- **File Loader**: The module responsible for parsing text files from the game_lists directory

## Requirements

### Requirement 1

**User Story:** As a user, I want to categorize games by season so that I can filter and view games appropriate for different times of the year

#### Acceptance Criteria

1. THE GameObject SHALL include four boolean seasonal attributes: seasonal_spring, seasonal_summer, seasonal_fall_halloween, and seasonal_winter_christmas
2. WHEN a GameObject is created, THE GameObject SHALL initialize all seasonal attributes to False
3. THE GameObject SHALL allow multiple seasonal attributes to be set to True for a single game
4. THE seasonal attributes SHALL be independent boolean flags that can be set individually

### Requirement 2

**User Story:** As a user, I want to maintain seasonal game lists in text files so that I can easily add or remove games from seasonal categories

#### Acceptance Criteria

1. THE system SHALL support four seasonal text files in the game_lists directory: Spring.txt, Summer.txt, Fall-Halloween.txt, and Winter-Christmas.txt
2. WHEN a seasonal text file exists, THE File Loader SHALL parse the file using the same format as Completions.txt
3. THE seasonal text files SHALL support IGDB ID disambiguation using the `<ID>` prefix format
4. THE seasonal text files SHALL support one game title per line with optional whitespace

### Requirement 3

**User Story:** As a user, I want the generator to automatically assign seasonal attributes during processing so that I don't have to manually tag games in the database

#### Acceptance Criteria

1. WHEN the Generator processes game lists, THE Generator SHALL read all seasonal text files
2. WHEN a game title matches an entry in a seasonal text file, THE Generator SHALL set the corresponding seasonal boolean attribute to True
3. IF a game appears in multiple seasonal text files, THEN THE Generator SHALL set multiple seasonal boolean attributes to True
4. THE Generator SHALL perform seasonal matching after IGDB enrichment to ensure accurate title matching

### Requirement 4

**User Story:** As a user, I want seasonal data persisted in the database so that I can query and report on games by season

#### Acceptance Criteria

1. THE SQLite schema SHALL include four boolean columns in the games table: seasonal_spring, seasonal_summer, seasonal_fall_halloween, and seasonal_winter_christmas
2. THE MongoDB schema SHALL include four boolean fields in game documents: seasonal_spring, seasonal_summer, seasonal_fall_halloween, and seasonal_winter_christmas
3. WHEN saving a GameObject to SQLite, THE SQL Manager SHALL store each seasonal attribute as a boolean value (0 or 1)
4. WHEN saving a GameObject to MongoDB, THE Mongo Manager SHALL store each seasonal attribute as a boolean field
5. WHEN loading a GameObject from SQLite, THE SQL Manager SHALL convert boolean values (0 or 1) to Python boolean types

### Requirement 5

**User Story:** As a user, I want to export seasonal data in reports so that I can analyze games by seasonal categories

#### Acceptance Criteria

1. WHEN exporting to JSON, THE Exporter SHALL include all four seasonal attributes as boolean fields
2. WHEN exporting to Excel, THE Exporter SHALL include four separate boolean columns for each seasonal attribute
3. WHEN exporting to text, THE Exporter SHALL NOT include seasonal attributes in the output
4. THE Excel seasonal columns SHALL support filtering by True/False values for easy seasonal game discovery
