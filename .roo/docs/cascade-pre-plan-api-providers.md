# Make a plan to simplify one part of this application

CRITICAL to Keep in mind:
- IMDB is used in this application. Keep active and fully operational.
- IMDB must use ONLY API calls. Remove all HTML scraping functionality from the application.
- TVDB and TMDB are not currently in use but may be used later:
    - Do not enable them.
    - Do not delete them.
- It is fine and preferred that TVDB and TMDB do not work.

## Cascade: API Providers
**Current State**: 3 separate implementations (IMDb, TMDB, TVDB)
- Duplicate authentication logic
- Duplicate token caching (TVDB has 2 separate implementations)
- Duplicate error handling
- Duplicate request/response formatting
- IMDb uses mixed approach: RapidAPI for some data + HTML scraping for ratings

**Goal**: Unify all providers AND remove HTML scraping from IMDb
- IMDb should use ONLY API calls (RapidAPI)
- Remove all HTML scraping functionality (`imdb_rating_scrape()` and related code)
- All external APIs should be HTTP requests with proper authentication

**Proposed Solution**: Single `BaseApiProvider` class
- Unified token management (cache, refresh, expiry)
- Standard error handling patterns
- Common request/response formatting
- Configuration-driven endpoints

**Cascade Eliminates**:
- 6 duplicate authentication functions
- 4 duplicate token management functions
- Multiple error handling blocks
- 3 separate configuration patterns

**Files Affected**:
- `utils/imdb_core.py` (remove HTML scraping, migrate to BaseApiProvider)
- Any routes/utilities that call HTML scraping functions

Goal: Make a detailed plan to simplify (remove unnecessary complexity) one part of this application as shown below.
- "Complexity/simplification": use the rules in `@/.roo/docs/simplification.md`.
- Use all resources you deem helpful, including but not limited to
    - `.@/agents.md`
    - `codebase_search`
CRITICAL to Keep in mind:
- IMDB is used in this application. Keep active and fully operational.
- IMDB must use ONLY API calls. Remove all HTML scraping functionality from the application.
- TVDB and TMDB are not currently in use but may be used later:
    - Do not enable them.
    - Do not delete them.
- It is fine and preferred that TVDB and TMDB do not work.

