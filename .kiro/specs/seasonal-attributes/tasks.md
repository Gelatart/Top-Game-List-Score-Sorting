# Implementation Plan

- [x] 1. Update GameObject with seasonal attributes
  - Add four boolean attributes: seasonal_spring, seasonal_summer, seasonal_fall_halloween, seasonal_winter_christmas
  - Set default values to False for all seasonal attributes
  - Verify to_dict() method includes seasonal attributes automatically
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 2. Update file_loader to handle missing files gracefully
  - Modify read_attributed_games() to check if file exists before opening
  - Return empty list if file doesn't exist
  - Import os module if not already imported
  - _Requirements: 2.2, 2.3, 2.4_

- [ ] 3. Update database schema for seasonal attributes
  - [ ] 3.1 Update create_schema.py to add seasonal columns to games table
    - Add seasonal_spring BOOLEAN DEFAULT 0
    - Add seasonal_summer BOOLEAN DEFAULT 0
    - Add seasonal_fall_halloween BOOLEAN DEFAULT 0
    - Add seasonal_winter_christmas BOOLEAN DEFAULT 0
    - _Requirements: 4.1, 4.3_

  - [ ] 3.2 Update sql_manager.py insert methods
    - Modify insert_or_update_game_full() to include seasonal fields in INSERT and UPDATE
    - Modify insert_or_update_game_full_with_relations() to include seasonal fields
    - Add seasonal parameters to SQL query tuples
    - _Requirements: 4.3, 4.5_

  - [ ] 3.3 Update sql_manager.py query methods
    - Modify get_all_full_game_info() SELECT to include seasonal columns
    - Modify get_full_game_info_by_id() SELECT to include seasonal columns
    - Ensure seasonal data is returned in query results
    - _Requirements: 4.5_

- [ ] 4. Update generator to read and apply seasonal tags
  - [ ] 4.1 Read seasonal text files after completion marking
    - Read Spring.txt using read_attributed_games()
    - Read Summer.txt using read_attributed_games()
    - Read Fall-Halloween.txt using read_attributed_games()
    - Read Winter-Christmas.txt using read_attributed_games()
    - Convert each to a set for efficient lookup
    - _Requirements: 2.1, 3.1_

  - [ ] 4.2 Apply seasonal tags to GameObjects
    - Loop through spring_titles and set seasonal_spring = True
    - Loop through summer_titles and set seasonal_summer = True
    - Loop through fall_titles and set seasonal_fall_halloween = True
    - Loop through winter_titles and set seasonal_winter_christmas = True
    - Place this logic after completion marking (Step 4) and before IGDB enrichment (Step 5)
    - _Requirements: 3.2, 3.3, 3.4_

- [ ] 5. Create sample seasonal text files
  - Create game_lists/Spring.txt with sample spring-themed games
  - Create game_lists/Summer.txt with sample summer-themed games
  - Create game_lists/Fall-Halloween.txt with sample fall/halloween-themed games
  - Create game_lists/Winter-Christmas.txt with sample winter/christmas-themed games
  - Use same format as Completions.txt (one game per line)
  - _Requirements: 2.1, 2.2_

- [ ] 6. Verify exports include seasonal data
  - Run generator with seasonal files
  - Check that JSON export includes seasonal boolean fields
  - Check that Excel export includes four seasonal columns
  - Verify text export does NOT include seasonal data
  - Test Excel filtering on seasonal columns
  - _Requirements: 5.1, 5.2, 5.3, 5.4_
