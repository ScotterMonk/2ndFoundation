# Plan: External API Providers Simplification (BaseApiProvider)
Short plan name: 251022_api_unify
Project size: One Phase (small to medium project)
Autonomy level: High (rare direction)
Testing type: Use browser

Background and problem
- Duplicate auth/token caching across TVDB and TMDB; separate IMDb implementation
- Evidence in `utils/api_tvdb/tvdb_utils.py`, `utils/api_tvdb/tvdb_extended.py`, `utils/api_tvdb/search_tvdb.py`, `utils/api_tmdb/utils_tmdb_core.py`, and `tvdb_api_test_report.md`
- Keep core vs presentation separation per `agents.md`
- Follow simplification principles in `.roo/docs/simplification.md`

Scope (in)
- Introduce a single core abstraction BaseApiProvider (no Flask imports) in `utils/api_provider_core.py`
- Hybrid approach: direct delegation from existing modules + provider descriptors (config + header builder + normalizers) passed to BaseApiProvider; no adapter classes in this phase
- Unify token management via a TokenCache (cache, refresh, expiry) across TVDB/TMDB; support no-token IMDb path. File-based by default under instance/api_tokens/{provider}.json with atomic write; option to swap to in-memory TTL for single-process
- Standardize HTTP request execution, error mapping, and request/response format hooks
- Configuration-driven endpoints and timeouts via `config.py` with sensible defaults if base URLs are currently hard-coded
- Maintain backward compatibility by keeping current module entry points and delegating to the base provider, emitting deprecation warnings for old auth/token helpers

Scope (out)
- No provider feature expansion beyond current capabilities
- No new data models or DB schema changes
- No switch to alternative API vendors in this phase

## Phase 1: Base provider consolidation and migration

Note: Tasks related to TVDB details route implementation and end-to-end browser testing for TVDB and TMDB were removed per user direction on 2025-10-22. The immediate priority is verifying IMDb functionality after refactoring.

### Task 1: Create BaseApiProvider class
Mode: /code-monkey
Action: Create `utils/api_provider_core.py` with BaseApiProvider class implementing unified HTTP request pipeline with urllib3 Retry (3 attempts, backoff_factor=0.5, retry on 429/500-504), standard error mapping returning envelope {'success', 'provider', 'status_code', 'error', 'endpoint', 'retried'}, and provider descriptor support (base_url, auth_strategy, header_builder, normalize callbacks).
Acceptance: BaseApiProvider class exists with execute_request method accepting provider descriptor, endpoint path, HTTP method, and optional params/data; returns standard envelope; no Flask imports.

### Task 2: Create TokenCache class
Mode: /code-monkey
Action: Create TokenCache class in `utils/api_provider_core.py` implementing file-based token storage under instance/api_tokens/{provider}.json with atomic write (temp file + rename), file locking for multi-process safety, token expiry checking, and auto-refresh callback support.
Acceptance: TokenCache class exists with get_token, save_token, and is_expired methods; handles Windows path normalization; uses os.replace for atomic writes; includes basic file locking via fcntl (Unix) or msvcrt (Windows).

### Task 3: Define TVDB provider descriptor
Mode: /code-monkey
Action: Create TVDB provider descriptor in `utils/api_tvdb/tvdb_utils.py` as dict or dataclass containing base_url from config.TVDB_BASE_URL, auth_strategy='bearer_token', token_endpoint='/login', header_builder function injecting Bearer token, and normalization callbacks (if needed).
Acceptance: TVDB_DESCRIPTOR defined with all required fields; header_builder accepts token and returns Authorization header; can be passed to BaseApiProvider.

### Task 4: Define TMDB provider descriptor
Mode: /code-monkey
Action: Create TMDB provider descriptor in `utils/api_tmdb/utils_tmdb_core.py` as dict or dataclass containing base_url from config.TMDB_API_BASE_URL, auth_strategy='static_token', header_builder function injecting read access token from config, and normalization callback to_tmdb_item.
Acceptance: TMDB_DESCRIPTOR defined with all required fields; header_builder uses config.TMDB_API_READ_ACCESS_TOKEN; can be passed to BaseApiProvider.

### Task 5: Define IMDb provider descriptor
Mode: /code-monkey
Action: Create IMDb provider descriptor in `utils/imdb_core.py` as dict or dataclass containing base_url inferred or from config, auth_strategy='api_key', header_builder function injecting API key as query param or header per IMDb API requirements, and normalization callback imdb_details_normalize.
Acceptance: IMDB_DESCRIPTOR defined with all required fields; header_builder uses config.IMDB_API_KEY; can be passed to BaseApiProvider.

### Task 6: Update config.py with API endpoint defaults
Mode: /code-monkey
Action: Add or verify config variables TVDB_BASE_URL (default 'https://api4.thetvdb.com/v4'), TVDB_TIMEOUT (default 15), TMDB_API_BASE_URL (if not present), IMDB_TIMEOUT (default 10) in `config.py` Config class; add inline comments documenting expected values.
Acceptance: All required config variables exist with sensible defaults; timeout values are integers; base URLs are strings.

### Task 7: Refactor get_tvdb_token_core to use TokenCache
Mode: /code-monkey
Action: Modify `get_tvdb_token_core` in `utils/api_tvdb/tvdb_utils.py` to use TokenCache instance for TVDB, implementing token retrieval, expiry check, auto-refresh via BaseApiProvider POST to /login endpoint using TVDB_DESCRIPTOR, and saving refreshed token; replace existing file-based caching logic.
Acceptance: get_tvdb_token_core uses TokenCache; token refresh uses BaseApiProvider; old caching code removed; function signature unchanged; returns valid TVDB token string.

### Task 8: Refactor get_tvdb_series_details_core to use BaseApiProvider
Mode: /code-monkey
Action: Modify `get_tvdb_series_details_core` in `utils/api_tvdb/tvdb_utils.py` to use BaseApiProvider.execute_request with TVDB_DESCRIPTOR, endpoint path f'/series/{tvdb_id}/extended', GET method, and token from get_tvdb_token_core; handle 401 by refreshing token and retrying; return data from standard envelope.
Acceptance: get_tvdb_series_details_core uses BaseApiProvider; no direct requests.get calls; handles 401 auto-refresh; returns series data dict; maintains existing error handling pattern.

### Task 9: Refactor get_tvdb_movie_details_core to use BaseApiProvider
Mode: /code-monkey
Action: Modify `get_tvdb_movie_details_core` in `utils/api_tvdb/tvdb_utils.py` to use BaseApiProvider.execute_request with TVDB_DESCRIPTOR, endpoint path f'/movies/{tvdb_id}/extended', GET method, and token from get_tvdb_token_core; handle 401 by refreshing token and retrying; return data from standard envelope.
Acceptance: get_tvdb_movie_details_core uses BaseApiProvider; no direct requests.get calls; handles 401 auto-refresh; returns movie data dict; maintains existing error handling pattern.

### Task 10: Refactor search_tvdb_core to use BaseApiProvider
Mode: /code-monkey
Action: Modify `search_tvdb_core` in `utils/api_tvdb/tvdb_utils.py` to use BaseApiProvider.execute_request with TVDB_DESCRIPTOR, endpoint path '/search', GET method, query params, and token from get_tvdb_token_core; handle 401 by refreshing token and retrying; return results from standard envelope.
Acceptance: search_tvdb_core uses BaseApiProvider; no direct requests.get calls; handles 401 auto-refresh; returns search results list; maintains existing error handling pattern.

### Task 11: Refactor authenticate function in tvdb_extended.py
Mode: /code-monkey
Action: Modify `authenticate` function in `utils/api_tvdb/tvdb_extended.py` to delegate to get_tvdb_token_core from tvdb_utils.py or use BaseApiProvider directly with TVDB_DESCRIPTOR for /login; remove duplicate token caching logic; add deprecation warning logging.
Acceptance: authenticate function delegates to centralized token management; duplicate code removed; deprecation warning emitted; function signature unchanged for backward compatibility.

### Task 12: Refactor get_valid_token in tvdb_extended.py
Mode: /code-monkey
Action: Modify `get_valid_token` in `utils/api_tvdb/tvdb_extended.py` to delegate to get_tvdb_token_core from tvdb_utils.py; remove duplicate token caching logic; add deprecation warning logging.
Acceptance: get_valid_token delegates to centralized token management; duplicate code removed; deprecation warning emitted; function signature unchanged.

### Task 13: Refactor functions in search_tvdb.py
Mode: /code-monkey
Action: Modify `authenticate` and `get_valid_token` in `utils/api_tvdb/search_tvdb.py` to delegate to get_tvdb_token_core from tvdb_utils.py; remove duplicate token caching logic; add deprecation warnings; update search_tvdb function to use BaseApiProvider with TVDB_DESCRIPTOR.
Acceptance: All TVDB functions in search_tvdb.py delegate to centralized implementations; duplicate code removed; deprecation warnings emitted; function signatures unchanged.

### Task 14: Refactor search_tmdb_core to use BaseApiProvider
Mode: /code-monkey
Action: Modify `search_tmdb_core` in `utils/api_tmdb/utils_tmdb_core.py` to use BaseApiProvider.execute_request with TMDB_DESCRIPTOR, endpoint path '/search/{media_type}', GET method, and query params; replace direct requests.get call; return results from standard envelope with to_tmdb_item normalization.
Acceptance: search_tmdb_core uses BaseApiProvider with TMDB_DESCRIPTOR; no direct requests.get calls; returns normalized search results list; error handling via standard envelope.

### Task 15: Refactor get_tmdb_details_core to use BaseApiProvider
Mode: /code-monkey
Action: Modify `get_tmdb_details_core` in `utils/api_tmdb/utils_tmdb_core.py` to use BaseApiProvider.execute_request with TMDB_DESCRIPTOR, endpoint path '/{media_type}/{tmdb_id}', GET method; replace direct requests.get call; return details from standard envelope with to_tmdb_item normalization.
Acceptance: get_tmdb_details_core uses BaseApiProvider with TMDB_DESCRIPTOR; no direct requests.get calls; returns normalized details dict; error handling via standard envelope.

### Task 16: Refactor imdb_api_get_details to use BaseApiProvider
Mode: /code-monkey
Action: Modify `imdb_api_get_details` in `utils/imdb_core.py` to use BaseApiProvider.execute_request with IMDB_DESCRIPTOR, appropriate endpoint path, GET method; replace direct requests.get call; return raw response data from standard envelope for existing normalization by imdb_details_normalize.
Acceptance: imdb_api_get_details uses BaseApiProvider with IMDB_DESCRIPTOR; no direct requests.get calls; returns response data dict; maintains compatibility with imdb_details_normalize.

### Task 17: Deprecate login_tvdb.py functions
Mode: /code-monkey
Action: Add deprecation warnings to all functions in `utils/api_tvdb/login_tvdb.py` directing users to use get_tvdb_token_core from tvdb_utils.py instead; add module-level docstring explaining deprecation and migration path.
Acceptance: All functions in login_tvdb.py emit deprecation warnings when called; module docstring explains migration; functions still work for backward compatibility.

### Task 18: Update config.py documentation
Mode: /task-simple
Action: Add or update comments in `config.py` documenting the purpose of TVDB_API_KEY, TVDB_BASE_URL, TVDB_TIMEOUT, TMDB_API_READ_ACCESS_TOKEN, TMDB_API_BASE_URL, IMDB_API_KEY, IMDB_TIMEOUT variables and their expected formats.
Acceptance: All API-related config variables have clear inline documentation; examples provided where helpful.

### Task 19: Create instance/api_tokens directory
Mode: /task-simple
Action: Create instance/api_tokens directory if it doesn't exist; add .gitignore entry to ignore *.json token files in this directory; add README.md explaining token cache storage for BaseApiProvider.
Acceptance: instance/api_tokens directory exists; .gitignore properly configured; README.md documents token cache location and format.

### Task 20: Create TVDB admin utility for presentation layer
Mode: /code-monkey
Action: Create `routes/utils_admin_tvdb.py` following the pattern of `routes/utils_admin_api.py` with function `tvdb_search_util()` that accepts request args (query, genre_id, sort, direction, page, per_page), calls `search_tvdb_core` from `utils/api_tvdb/tvdb_utils.py` via BaseApiProvider, processes results, and returns standardized dict with success, results list, pagination object, search_query, and any errors for template rendering.
Acceptance: utils_admin_tvdb.py exists with tvdb_search_util function; delegates to search_tvdb_core; returns dict compatible with route_helpers pattern; no Flask imports in core files; includes proper error handling.

### Task 21: Add TVDB search route to admin blueprint
Mode: /front-end
Action: Add GET route `/admin/tvdb_search` to `routes/admin.py` that calls `tvdb_search_util()` from `routes/utils_admin_tvdb.py` and renders `templates/admin/tvdb_search.html` with returned data using `handle_util_result` or `handle_simple_util_result` pattern; ensure route has `@login_required` and `@admin_required` decorators; import tvdb_search_util at top of file.
Acceptance: Route `/admin/tvdb_search` exists in admin.py; calls tvdb_search_util; renders tvdb_search.html template; follows existing route pattern for admin utilities; proper authentication decorators applied.

### Task 22: Verify IMDb integration remains functional
Mode: /tester
Action: Use MCP Puppeteer or create test script in `temp/` to verify IMDb API calls via BaseApiProvider return expected data structure; test imdb_api_get_details with known IMDb ID; validate imdb_details_normalize still processes response correctly.
Acceptance: IMDb API calls work via BaseApiProvider; responses match expected format; normalization functions process data correctly; no errors in test execution.

### Task 23: Document new provider pattern in agents.md
Mode: /task-simple
Action: Add section to `agents.md` documenting the BaseApiProvider pattern, provider descriptor structure, TokenCache usage, and how to add new API providers following this pattern; include code examples.
Acceptance: agents.md updated with comprehensive BaseApiProvider documentation; includes example descriptor definition; explains when to use core vs presentation separation with providers.

Objectives (from high-level plan)
- Single token management layer with per-provider strategy:
  - TVDB: bearer via /login; cached with expiry; auto-refresh on 401
  - TMDB: static read access token from config; header injection
  - IMDb: API key only; no token flow
- Standard HTTP pipeline with urllib3 Retry (default: 3 attempts; backoff_factor=0.5; retry on 429, 500-504)
- Provider descriptors define base_url, auth strategy, header builder, and normalization callbacks
- Standard response envelope: {'success': bool, 'provider': str, 'status_code': int|None, 'error': str|None, 'endpoint': str, 'retried': int|bool}
- Configuration-driven endpoints and timeouts via `config.py`
- Backward compatibility via thin shims with deprecation warnings

Deliverables (artifacts from tasks)
- `utils/api_provider_core.py` with BaseApiProvider and TokenCache classes
- Provider descriptors in tvdb_utils.py, utils_tmdb_core.py, imdb_core.py
- Updated TVDB modules delegating to BaseApiProvider
- Updated TMDB module delegating to BaseApiProvider
- Updated IMDb module delegating to BaseApiProvider
- Updated `config.py` with documented API configuration
- Deprecation warnings in duplicate auth/token helpers
- instance/api_tokens directory for token storage
- Updated `agents.md` documentation

Acceptance criteria
- Duplicate authentication functions eliminated (target: 6) and token management functions eliminated (target: 4)
- Token caching unified to TokenCache; 401 auto-refresh verified with forced-expiry test
- Standard response envelope returned from all providers; wrappers work via delegation
- All wrappers use provider descriptors with BaseApiProvider
- IMDb functionality verified end-to-end after refactoring
- No Flask imports in core; config-driven endpoints/timeouts honored with defaults
- Manual verification complete for IMDb integration

Risks and mitigations
- Token storage consistency on multi-process: file-based cache with atomic write (temp + rename) and file lock
- Provider rate limits: urllib3 Retry with backoff for idempotent GET
- Backward compatibility drift: shims with deprecation warnings and stable signatures
- Windows paths: normalize cache paths to avoid separator issues
- Future evolution: descriptors create seam for adapter classes later

Affected files
- `utils/api_tmdb/utils_tmdb_core.py`
- `utils/api_tvdb/tvdb_utils.py`
- `utils/api_tvdb/tvdb_extended.py`
- `utils/api_tvdb/search_tvdb.py`
- `utils/api_tvdb/login_tvdb.py`
- `utils/imdb_core.py`
- `config.py`
- `utils/api_provider_core.py` (new)
- `routes/utils_admin_tvdb.py` (new)
- `routes/admin.py`
- `templates/admin/tvdb_search.html`
- instance/api_tokens/ (new directory)
- `agents.md`

Non-functional constraints
- Keep core modules free of Flask imports
- Follow naming convention {domain}_{specific}
- Add Created/Modified attribution comments per `.roo/rules/01-general.md`