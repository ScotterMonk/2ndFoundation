# IMDb Core Consolidation Plan

## Overview
Consolidate redundant IMDb functionality between `utils/imdb_core.py` and `utils/api_imdb/utils_imdb_core.py` by establishing `utils/imdb_core.py` as the single source of truth and deprecating the duplicate module.

## Background
Analysis revealed significant code duplication between two IMDb core modules:
- `utils/imdb_core.py` - Comprehensive feature set with full API integration
- `utils/api_imdb/utils_imdb_core.py` - Subset of functionality with duplicate implementations

## Recommendation
Keep `utils/imdb_core.py` as the primary module and convert `utils/api_imdb/utils_imdb_core.py` to a deprecation shim layer that forwards calls to the main module.

## Phases and Tasks

### Phase 1: Preparation
1) Backup current implementations
   - Copy both files to `.roo/docs/old_versions/` with timestamp

2) Update import references
   - Modify `utils/media_core.py` to import from `utils.imdb_core` instead of `utils.api_imdb.utils_imdb_core`
   - Verify no other files import from the deprecated module

### Phase 2: Create Deprecation Shim
3) Convert `utils/api_imdb/utils_imdb_core.py` to shim layer
   - Replace all function implementations with deprecation warnings
   - Forward calls to corresponding functions in `utils.imdb_core`
   - Follow existing pattern used in `utils/api_imdb/utils_imdb.py`

4) Update function name mappings
   - Map `normalize_imdb_id` → `imdb_id_normalize`
   - Map `to_imdb_item` → `imdb_item_normalize`
   - Map `fetch_imdb_details_core` → `imdb_details_fetch_core`
   - Map `search_imdb_for_media_core` → `imdb_search_for_media_core`
   - Map `get_imdb_rating_value` → `imdb_rating_scrape`

### Phase 3: Testing and Validation
5) Test import changes
   - Verify `utils/media_core.py` functions correctly with new imports
   - Check that all IMDb functionality works as expected

6) Validate deprecation warnings
   - Confirm deprecation warnings appear when using old module
   - Verify functionality still works through the shim layer

## Acceptance Criteria
- All code consolidated into single module (`utils/imdb_core.py`)
- No functional regressions in IMDb operations
- Deprecation warnings properly displayed for old module usage
- All import references updated to use primary module
- Backup files created in `.roo/docs/old_versions/`

## Integration Points
- `utils/media_core.py` - Primary consumer of IMDb functionality
- `utils/api_imdb/utils_imdb.py` - Existing deprecation pattern to follow
- `utils/deprecation.py` - Deprecation warning utilities

## Testing Strategy
- Verify IMDb search functionality works after consolidation
- Test media import operations that depend on IMDb data
- Confirm deprecation warnings appear without breaking functionality
- Validate that all existing routes using IMDb features continue to work

## Implementation Notes
- Function signatures remain the same to maintain compatibility
- Deprecation shim ensures backward compatibility during transition
- Following established project pattern for deprecation (see `utils/api_imdb/utils_imdb.py`)
- All core functionality preserved in `utils/imdb_core.py`