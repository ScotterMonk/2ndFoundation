# Plan: Rename imdb_core_utils.py to utils_imdb_core.py and refactor

## Overview
Rename the file `utils/api_imdb/imdb_core_utils.py` to `utils/api_imdb/utils_imdb_core.py` and update all references to follow the established naming convention pattern of `{domain}_{specific}`.

## Phases and Tasks

### Phase 1: Pre-work and Analysis
- [x] Search for existing patterns and dependencies
- [x] Read the current file to understand its content
- [ ] Create backup of original file

### Phase 2: File Renaming
- [ ] Rename the file from `imdb_core_utils.py` to `utils_imdb_core.py`

### Phase 3: Update Import Statements
- [ ] Update import in `utils/api_imdb/__init__.py`
- [ ] Update import in `utils/media_core.py`
- [ ] Update any other files that import from the old file path

### Phase 4: Code Refactoring (if needed)
- [ ] Review function names to ensure they follow naming conventions
- [ ] Review variable names to ensure they follow naming conventions
- [ ] Make any necessary code adjustments

### Phase 5: Verification
- [ ] Verify all imports are working correctly
- [ ] Confirm no syntax errors in the renamed file

## Integration Points
- `utils/api_imdb/__init__.py` - imports functions from this file
- `utils/media_core.py` - imports functions from this file
- Any other files that may import from this module

## Acceptance Criteria
- File is successfully renamed to `utils_imdb_core.py`
- All import statements are updated to reference the new file name
- Code follows established naming conventions
- No syntax errors in the renamed file
- All dependent modules can still import the required functions

## Notes
- Following naming convention pattern: `{specific}_{domain}` -> `{domain}_{specific}`
- No testing required as specified by user
- Autonomy level: High (rare direction)
- Testing type: No testing