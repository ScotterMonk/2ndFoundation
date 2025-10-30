# API Provider Simplification Pre-Plan

CRITICAL Constraints:
- IMDB is used in this application. Keep active and fully operational.
- IMDB must use ONLY API calls. Remove all HTML scraping functionality from the application.
- TVDB and TMDB are not currently in use but may be used later:
    - Do not enable them.
    - Do not delete them.
- It is fine and preferred that TVDB and TMDB do not work.

## Current State Analysis

### Provider Implementation Status
- A unified provider layer already exists via `utils/api_provider_core.py`:
    - `BaseApiProvider()` class
    - `TokenCache()` class
- TVDB and TMDB largely use this layer through lazy descriptors defined in `utils/api_provider_descriptors.py`:
    - `get_tvdb_descriptor()`
    - `get_tmdb_descriptor()`
- IMDb is active and operational but uses mixed approach:
    - Provider instantiated at `imdb_provider = BaseApiProvider(IMDB_DESCRIPTOR)` in `utils/imdb_core.py`
    - Direct RapidAPI requests via `imdb_api_search_title()` and `imdb_api_get_details()`
    - HTML scraping for ratings via `imdb_rating_scrape()` - MUST BE REMOVED

### Duplicate Patterns Identified
- Duplicate authentication logic
- Duplicate token caching (TVDB has 2 separate implementations)
- Duplicate error handling
- Duplicate request/response formatting
- IMDb uses mixed approach: RapidAPI for some data + HTML scraping for ratings

## Goals

Primary objectives for this simplification:
1) Unify all providers under `BaseApiProvider`
2) Remove ALL HTML scraping functionality from IMDb
3) Standardize authentication, error handling, and response patterns
4) IMDb should use ONLY API calls (RapidAPI)
5) All external APIs should be HTTP requests with proper authentication

Updated insight: "All external APIs are HTTP requests with proper authentication; TVDB/TMDB use bearer tokens, IMDb uses API keys via RapidAPI. HTML scraping is not allowed."

## Verification Details

### Current Implementation Analysis

1) Provider Usage
- TVDB: Descriptor and token cache are centralized; downstream utilities use provider and header override:
    - Token cache: `get_tvdb_token_core()` in `utils/api_tvdb/tvdb_utils.py`
    - Header override: `get_tvdb_series_details_core()` and `get_tvdb_movie_details_core()`
    - Descriptor + cache: `get_tvdb_descriptor()` in `utils/api_provider_descriptors.py`
- TMDB: Uses static token via descriptor and provider-based GET
    - Examples: `utils/api_tmdb/utils_tmdb_core.py`
- IMDb: Provider instantiated but not leveraged
    - Provider: `imdb_provider = BaseApiProvider(IMDB_DESCRIPTOR)` in `utils/imdb_core.py`
    - Direct requests: `imdb_api_search_title()`, `imdb_api_get_details()`
    - HTML scraping: `imdb_rating_scrape()` - MUST BE REMOVED

2) Authentication Logic
- TVDB/TMDB: Now standardize auth via descriptors
    - TVDB token refresh: `_refresh_tvdb_token()` cached via `TokenCache()`
    - TMDB: Static read token injected by `get_tmdb_descriptor()`
- IMDb: Still authenticates ad hoc with RapidAPI keys in search/details functions

3) Token Caching
- Mainline flow: TVDB uses centralized `TokenCache()` via `get_tvdb_descriptor()`
- Legacy/auxiliary TVDB scripts may contain standalone auth flows but are not on primary path

4) Error Handling
- TVDB/TMDB: Largely resolved through `BaseApiProvider.get()` which returns standardized response dict and retries on transient failures
- IMDb: Bespoke error handling in functions using requests directly

5) Request/Response Formatting
- Normalization hook modeled in descriptors (normalization_callbacks) but not fully leveraged
- Each provider normalizes in its own utils
- IMDb has rich normalization: `imdb_details_normalize()`, inline normalization in `imdb_search_for_media_core()`
- Keep as-is unless strong convergence exists

6) Header Builder Signature Issue
- IMDb descriptor's header_builder expects an argument (api_key) in `get_imdb_descriptor()`
- `BaseApiProvider.get()` calls `header_builder()` with no arguments by default
- This mismatch requires resolution before migration

## Action Plan

### 1) IMDb descriptor header builder alignment
Action: Update `get_imdb_descriptor()` in `utils/api_provider_descriptors.py` so `header_builder` is zero-arg and internally resolves the API key from `current_app.config` (or env) to produce {'x-api-key': key}. This makes it compatible with `BaseApiProvider.get()` default header flow without passing headers_override.

### 2) IMDb search/details migration to BaseApiProvider
Action: In `utils/imdb_core.py`, refactor `imdb_api_search_title()` and `imdb_api_get_details()` to use `imdb_provider.get` with IMDb's base_url and provider-standard error handling. Preserve existing query parameter shapes and normalization via `imdb_item_normalize()` and `imdb_details_normalize()`.

### 3) Remove HTML scraping functionality
Action: REMOVE `imdb_rating_scrape()` and all related HTML scraping code from `utils/imdb_core.py`.
Action: Find and remove all calls to HTML scraping functions throughout the application.
Action: If rating data is needed, obtain it through the RapidAPI instead (verify API provides rating data).

### 4) Standardized error paths for IMDb
Action: Replace function-local try/except request blocks with centralized response checking:
- If `response['success']` is False, propagate a standardized error dict or raise a ValueError with a consistent message, aligning with how TMDB/TVDB callers check provider responses.

### 5) Leave TVDB/TMDB code paths untouched (no enablement)
Action: No functional changes to `utils/api_tvdb/tvdb_utils.py` or `utils/api_tmdb/utils_tmdb_core.py`.
Optional docs-only cleanup: Confirm README/comments no longer claim duplicate caches; point them to `TokenCache()`.

### 6) Post-change verification
Action: Run the IMDb-facing tests to confirm no regressions:
- `tests/test_imdb_search.py`, routes that import IMDb core like `routes/utils_user_media.py`
Action: Re-run redundancy metrics to update the "Cascade Eliminates" numbers in `redundancy_analysis_report.md`.

## Files Affected

Primary:
- `utils/imdb_core.py` - Remove HTML scraping, migrate to BaseApiProvider
- `utils/api_provider_descriptors.py` - Fix header builder signature for IMDb

Secondary:
- Any routes/utilities that call HTML scraping functions
- Consumer imports: `routes/utils_user_media.py`

Do not modify:
- `utils/api_tvdb/tvdb_utils.py` - TVDB remains dormant
- `utils/api_tmdb/utils_tmdb_core.py` - TMDB remains dormant

## Risk/Impact Notes

Critical risks to address:
- Header builder signature: Essential to fix before switching IMDb calls to the provider; otherwise TypeError will occur due to zero-arg call in `BaseApiProvider.get()`
- Removing HTML scraping: Verify RapidAPI provides all needed data (especially ratings). If ratings are unavailable via API, discuss alternative approaches with user before proceeding.
- TVDB/TMDB remain dormant; no functional enablement occurs

## Expected Outcomes

Cascade eliminates:
- IMDb's direct RapidAPI calls and function-local error handling
- All HTML scraping functionality
- Duplicate authentication patterns
- Bespoke error handling blocks

Note: Original "Cascade Eliminates" counts (6 duplicate auth functions, 4 duplicate token mgmt functions) are outdated given the new provider core and descriptors. Recalculate duplication using existing redundancy artifacts after IMDb migration and scraping removal.

## Planning Instructions

Goal: Make a detailed plan to simplify (remove unnecessary complexity) one part of this application as shown above.
- "Complexity/simplification": use the rules in `@/.roo/docs/simplification.md`
- Use all resources deemed helpful, including but not limited to:
    - `@/agents.md`
    - `codebase_search`

This pre-plan provides a corrected update path that keeps IMDb fully operational using ONLY API calls, removes all HTML scraping, and does not enable or delete TVDB/TMDB.