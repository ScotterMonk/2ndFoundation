# User Query: External API Providers Simplification (BaseApiProvider)
Short plan name: 251022_api_unify
Project size: One Phase (small to medium project)
Autonomy level: High (rare direction)
Testing type: Use browser

Source request
<task>
Goal: Make a detailed plan to simplify (remove unnecessary complexity) one part of this application as shown below.

- "Complexity/simplification": use the rules in [simplification.md](.roo/docs/simplification.md)
- Use all resources you deem helpful, including but not limited to
    - `@/agents.md`
    - codebase_search
- IMDB is used in this application.
- TVDB and TMDB are not currently in use but may be used later.

## Cascade: External API Providers
Current State: 3 separate implementations (IMDb, TMDB, TVDB)
- Duplicate authentication logic
- Duplicate token caching (TVDB has 2 separate implementations)
- Duplicate error handling
- Duplicate request/response formatting

Insight: "All external APIs are HTTP requests with auth tokens"

Proposed Solution: Single BaseApiProvider class
- Unified token management (cache, refresh, expiry)
- Standard error handling patterns
- Common request/response formatting
- Configuration-driven endpoints

Cascade Eliminates:
- 6 duplicate authentication functions
- 4 duplicate token management functions
- Multiple error handling blocks
- 3 separate configuration patterns

Files Affected:
- [utils/api_tmdb/utils_tmdb_core.py](utils/api_tmdb/utils_tmdb_core.py)
- [utils/api_tvdb/tvdb_utils.py](utils/api_tvdb/tvdb_utils.py)
- [utils/api_tvdb/tvdb_extended.py](utils/api_tvdb/tvdb_extended.py)
- [utils/api_tvdb/tvdb_search.py](utils/api_tvdb/tvdb_search.py)
- [utils/imdb_core.py](utils/imdb_core.py)
</task>

Notes captured by planner-a
- Preserve core vs presentation separation per `@/agents.md`
- Config keys and endpoints in [config.py](config.py)
- Backward-compatible shims during migration