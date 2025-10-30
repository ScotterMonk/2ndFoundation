# API Provider Simplification Plan

## Objective
Simplify API provider implementation by unifying all providers under `BaseApiProvider`, removing HTML scraping from IMDb, and standardizing authentication and error handling patterns.

## Critical Constraints
- IMDB is used in this application. Keep active and fully operational.
- IMDB must use ONLY API calls. Move all HTML scraping functionality to `.roo/docs/unused_for_now/` (archive) folder and remove references to that HTML scraping code.
- TVDB and TMDB are not currently in use but may be used later:
    - Do not enable them.
    - Do not delete them.
    - Move the functionality to `.roo/docs/unused_for_now/` (archive) folder.
- It is fine and preferred that TVDB and TMDB do not work.

## Current State
Based on codebase search:
- Unified provider layer exists via `utils/api_provider_core.py`:
    - `BaseApiProvider()` class
    - `TokenCache()` class
- TVDB and TMDB largely use this layer through `utils/api_provider_descriptors.py`
- IMDb is active but uses mixed approach:
    - Provider instantiated at `imdb_provider = BaseApiProvider(IMDB_DESCRIPTOR)` in `utils/imdb_core.py`
    - Direct RapidAPI requests via `imdb_api_search_title()` and `imdb_api_get_details()`
    - HTML scraping for ratings via `imdb_rating_scrape()` - MUST BE MOVED and deREFERENCED.

## Key Files
Primary:
- `utils/imdb_core.py` - IMDb implementation (1129 lines)
- `utils/api_provider_descriptors.py` - Provider descriptors
- `utils/api_provider_core.py` - BaseApiProvider class

Secondary:
- Routes/utilities that call HTML scraping functions
- Consumer imports: `routes/utils_user_media.py`

## High-Level Phases

### Phase 1: Fix IMDb Descriptor Header Builder
Objective: Resolve header builder signature mismatch to enable BaseApiProvider usage.
Context: IMDb descriptor's header_builder expects an argument (api_key) but `BaseApiProvider.get()` calls `header_builder()` with no arguments by default.

Tasks:
- Task 1.1: Modify `get_imdb_descriptor()` header_builder in `utils/api_provider_descriptors.py` from `lambda api_key: {'x-api-key': api_key}` to zero-arg lambda that resolves API key internally via `current_app.config['IMDB_API_KEY']` and returns `{'x-api-key': key}`.
    Mode hint: /code-monkey
    Integration: Aligns IMDb descriptor with TVDB/TMDB pattern; enables `BaseApiProvider.get()` to work without headers_override.
    Reference pattern: See `get_tvdb_descriptor()` line 75 uses `lambda token:` (single arg from cache), but IMDb should use `lambda: {'x-api-key': current_app.config['IMDB_API_KEY']}` (zero-arg, internal resolution).
    Acceptance: `get_imdb_descriptor()['header_builder']()` returns dict with the expected API key header when called with no arguments; descriptor access does not require Flask app context at module import (evaluated at call-time only).

### Phase 2: Migrate IMDb Functions to BaseApiProvider
Objective: Refactor IMDb search/details functions to use `imdb_provider.get()` instead of direct requests.
Context: Currently `imdb_api_search_title()` and `imdb_api_get_details()` use direct `requests.get()`.

Tasks:
- Task 2.1: Refactor `imdb_api_search_title()` in `utils/imdb_core.py` to replace direct `requests.get()` with `imdb_provider.get(endpoint, params=params)` using existing `imdb_provider` instance and RapidAPI search endpoint `/title/auto-complete`.
    Mode hint: /code-monkey
    Integration: Use provider's standardized GET method; preserve existing `params` dict shape and `imdb_item_normalize()` for results.
    Reference pattern: See `utils/api_tvdb/tvdb_utils.py` lines 67-92 for `tvdb_provider.get()` usage with endpoint and checking `response['success']`.
    Acceptance: Function returns same data structure; uses `imdb_provider.get()`; no direct `requests.get()` calls remain in this function.

- Task 2.2: Refactor `imdb_api_get_details()` in `utils/imdb_core.py` to replace direct `requests.get()` with `imdb_provider.get(endpoint)` using RapidAPI details endpoint pattern `/api/imdb/{imdb_id}`.
    Mode hint: /code-monkey
    Integration: Use provider's standardized GET; preserve `imdb_details_normalize()` for response formatting.
    Reference pattern: TVDB details calls in `utils/api_tvdb/tvdb_utils.py` show provider.get() with f-string endpoints.
    Acceptance: Function returns same normalized details structure; uses `imdb_provider.get()`; no direct `requests.get()` calls remain.

### Phase 3: Move HTML Scraping Functionality
Objective: Remove all HTML scraping code from IMDb implementation and save the code to `.roo/docs/unused_for_now/` with appropriate file name(s); remove all references across codebase and tests.
Context: `imdb_rating_scrape()` function and related HTML parsing must be removed.

Tasks:
- Task 3.1: Create archive file `.roo/docs/unused_for_now/imdb_html_scraping.md` containing extracted code from `imdb_rating_scrape()` and `_extract_rating_from_obj()` functions with brief header explaining these were removed in favor of API-only approach.
    Mode hint: /task-simple
    Integration: Preserves code for historical reference.
    Acceptance: Archive file exists with scraped function bodies and explanatory header; uses markdown code blocks.

- Task 3.2: Remove `imdb_rating_scrape()` function definition from `utils/imdb_core.py`.
    Mode hint: /code-monkey
    Integration: Eliminates HTML scraping implementation.
    Acceptance: Function no longer exists in `utils/imdb_core.py`; file remains syntactically valid.

- Task 3.3: Remove `_extract_rating_from_obj()` helper function from `utils/imdb_core.py`.
    Mode hint: /task-simple
    Integration: Removes HTML parsing helper.
    Acceptance: Function no longer exists in file.

- Task 3.4: Refactor `imdb_rating_core()` in `utils/imdb_core.py` to call `imdb_api_get_details(imdb_id)` instead of `imdb_rating_scrape(imdb_id)`, extract rating from API response data, and map to return dict keys `rating`, `rating_0_10`, `rating_0_100` (setting to `None` if unavailable).
    Mode hint: /code-monkey
    Integration: Converts ratings to API-only; maintains same response shape.
    Reference: Check RapidAPI response structure for rating field location.
    Acceptance: Function calls `imdb_api_get_details()`, extracts rating, returns dict with same keys; no scraping calls.

- Task 3.5: Remove `from utils.imdb_core import imdb_rating_scrape` import statement from `tests/test_imdb_search.py`.
    Mode hint: /task-simple
    Integration: Derferences scraping in tests.
    Acceptance: Import line removed; test file imports remain valid.

- Task 3.6: Update any test functions in `tests/test_imdb_search.py` that call `imdb_rating_scrape()` to instead test `imdb_rating_core()` API-based flow.
    Mode hint: /code-monkey
    Integration: Tests verify API-only rating functionality.
    Acceptance: No calls to `imdb_rating_scrape()` in test files; `imdb_rating_core()` is tested.

### Phase 4: Standardize Error Handling
Objective: Replace function-local error handling with centralized provider response checking.
Context: IMDb functions have bespoke error handling; should align with TVDB/TMDB pattern.

Tasks:
- Task 4.1: Refactor error handling in `imdb_api_search_title()` and `imdb_api_get_details()` in `utils/imdb_core.py` to remove local try/except blocks around `requests` calls and instead check `response['success']` from `imdb_provider.get()`, raising `ValueError` with error message if `False`.
    Mode hint: /code-monkey
    Integration: Aligns error handling with BaseApiProvider pattern.
    Reference pattern: `utils/api_tvdb/tvdb_utils.py` line 88: `if not response['success']: raise ConnectionError(...)`.
    Acceptance: Functions use `if not response['success']` checks; no try/except around provider.get() calls; raise clear errors.

- Task 4.2: Update `imdb_rating_core()` error handling in `utils/imdb_core.py` to check API response success and propagate error dict with `success: False, error: <message>` keys instead of raising exceptions for missing ratings.
    Mode hint: /code-monkey
    Integration: Provides graceful failure for unavailable ratings.
    Acceptance: Function returns error dict when API fails; maintains consistent response structure.

### Phase 5: Verification and Testing
Objective: Ensure IMDb functionality works correctly using only API calls.

Tasks:
- Task 5.1: Run pytest on `tests/test_imdb_search.py` to verify all IMDb tests pass with API-only implementation.
    Mode hint: /tester
    Integration: Validates IMDb search/details/rating functionality via pytest.
    Command: `pytest tests/test_imdb_search.py -v`
    Acceptance: All tests pass; no import errors; no references to scraping functions.

- Task 5.2: Verify IMDb integration in routes by running pytest on relevant route test files covering `routes/utils_user_imdb.py`, `routes/utils_user_media.py`, `routes/utils_admin_api.py` IMDb functionality.
    Mode hint: /tester
    Integration: Ensures route-level IMDb calls work correctly.
    Command: `pytest tests/ -k "imdb" -v`
    Acceptance: Route tests pass; IMDb provider integration works through routes.

- Task 5.3: Perform codebase-wide search for any remaining references to `imdb_rating_scrape` or `_extract_rating_from_obj` to confirm complete removal.
    Mode hint: /task-simple
    Integration: Final verification of scraping removal.
    Use: `codebase_search` or `search_files` with pattern `imdb_rating_scrape|_extract_rating_from_obj`.
    Acceptance: No matches found in codebase except archive file.

- Task 5.4: Manually test IMDb search and details retrieval via Python console to verify provider-based calls return expected data structure (execute within Flask app context: `from app import app; with app.app_context(): ...`).
    Mode hint: /tester
    Integration: Smoke test of core IMDb API functions under app context.
    Test: Import and call `imdb_api_search_title()`, `imdb_api_get_details()`, `imdb_rating_core()` with sample IMDb IDs inside an app_context.
    Acceptance: Functions execute successfully without "working outside of application context" errors; return expected dict structures; use `imdb_provider.get()` internally and do not produce HTTP 401 due to missing headers.

- Task 5.5: Validate IMDb RapidAPI header names and host by executing `imdb_provider.get('/title/auto-complete', params={'q':'inception'})` within app context and confirming authentication succeeds.
    Mode hint: /tester
    Integration: Confirms `header_builder` produces correct header keys/values for the configured base URL.
    Acceptance: Response indicates `success: True` (HTTP 200) rather than 401/403; if authentication fails, record observed header requirements and open a follow-up fix task.

### Phase 6: Safe Archive of Dormant TVDB/TMDB Code
Objective: Move dormant TVDB/TMDB auxiliary code to archive without breaking imports or runtime.
Context: User prefers TVDB/TMDB to remain non-functional and preserved. Some modules (eg, admin utilities) may import TVDB/TMDB helpers at import time.

Tasks:
- Task 6.1: Use `search_files` to identify all Python files in `utils/api_tvdb/` and `utils/api_tmdb/` directories and create list of which are CLI scripts vs imported modules.
    Mode hint: /task-simple
    Integration: Maps TVDB/TMDB code structure for safe archiving.
    Method: List files, check for `if __name__ == "__main__"` patterns indicating standalone scripts.
    Acceptance: List created identifying standalone scripts (eg, `search_tvdb.py`, `prowlarr-search.py`) vs core modules.

- Task 6.2: Create archive directories `.roo/docs/unused_for_now/tvdb/` and `.roo/docs/unused_for_now/tmdb/` and move non-imported auxiliary files (CLI scripts, READMEs) from `utils/api_tvdb/` and `utils/api_tmdb/` into respective archive folders.
    Mode hint: /task-simple
    Integration: Preserves auxiliary code while keeping core modules intact.
    Files to move: Standalone scripts, `README.md`, `.env` files not needed for import.
    Acceptance: Archive directories exist with moved files; core imported modules remain in `utils/api_tvdb/` and `utils/api_tmdb/`.

- Task 6.3: Add deprecation comment block at top of remaining TVDB/TMDB core module files in `utils/api_tvdb/` and `utils/api_tmdb/` stating "DORMANT: This module is not actively supported. Preserved for potential future use. Do not enable without review."
    Mode hint: /task-simple
    Integration: Documents dormant status clearly.
    Acceptance: Comment blocks added to top of retained `.py` files in both TVDB/TMDB directories.

- Task 6.4: Test application startup by running `python app.py` to verify no `ImportError` exceptions occur related to TVDB/TMDB modules.
    Mode hint: /tester
    Integration: Confirms app starts successfully with archived structure.
    Command: `python app.py` (check for clean startup without TVDB/TMDB import errors).
    Acceptance: App starts without errors; no ImportError mentioning TVDB or TMDB.

- Task 6.5: Create index file `.roo/docs/unused_for_now/api_archive_index.md` documenting what was archived from TVDB/TMDB and why.
    Mode hint: /task-simple
    Integration: Provides context for archived code.
    Content: List of archived files, date, reason (dormant APIs, preserved for future use).
    Acceptance: Index file exists with clear documentation of archived items.