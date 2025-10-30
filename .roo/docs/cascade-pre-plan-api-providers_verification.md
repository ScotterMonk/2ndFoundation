Verification of each plan element and necessary updates

Summary
- A unified provider layer already exists via [`BaseApiProvider()`](utils/api_provider_core.py:13) and [`TokenCache()`](utils/api_provider_core.py:100).
- TVDB and TMDB largely use that layer through lazy descriptors (token cache and header builders) defined in [`get_tvdb_descriptor()`](utils/api_provider_descriptors.py:67) and [`get_tmdb_descriptor()`](utils/api_provider_descriptors.py:89).
- IMDb is active and operational but still uses direct requests to RapidAPI and HTML scraping; it instantiates a provider but does not use it consistently. See provider instantiation at [`imdb_provider = BaseApiProvider(IMDB_DESCRIPTOR)`](utils/imdb_core.py:38), while calls flow through [`imdb_api_search_title()`](utils/imdb_core.py:129) and [`imdb_api_get_details()`](utils/imdb_core.py:215), each using requests directly.
- CRITICAL: IMDb must use ONLY API calls. All HTML scraping functionality (including [`imdb_rating_scrape()`](utils/imdb_core.py:391)) must be removed from the application.
- The "Files Affected: utils/imdb_core.py" pointer is valid; however, changes may also be required in [`get_imdb_descriptor()`](utils/api_provider_descriptors.py:111) to align header-builder signatures if you adopt the base provider for IMDb calls.

Verification details

1) Current State: “3 separate implementations (IMDb, TMDB, TVDB)”
- Accurate in a limited sense, but TVDB and TMDB already route through the shared provider.
    - TVDB: Descriptor and token cache are centralized; downstream utilities use the provider and header override:
        - Token cache usage: [`get_tvdb_token_core()`](utils/api_tvdb/tvdb_utils.py:21) and header override usage in [`get_tvdb_series_details_core()`](utils/api_tvdb/tvdb_utils.py:67) and [`get_tvdb_movie_details_core()`](utils/api_tvdb/tvdb_utils.py:95).
        - Descriptor + cache: [`get_tvdb_descriptor()`](utils/api_provider_descriptors.py:67).
    - TMDB: Uses static token via descriptor and provider-based GET; examples of provider usage appear in [`utils/api_tmdb/utils_tmdb_core.py`](utils/api_tmdb/utils_tmdb_core.py).
- IMDb: A provider is instantiated but not leveraged; functionality uses RapidAPI directly, plus rating scraping:
    - Provider instantiation: [`imdb_provider = BaseApiProvider(IMDB_DESCRIPTOR)`](utils/imdb_core.py:38)
    - Requests via RapidAPI: [`imdb_api_search_title()`](utils/imdb_core.py:129), [`imdb_api_get_details()`](utils/imdb_core.py:215)
    - HTML scraping for ratings: [`imdb_rating_scrape()`](utils/imdb_core.py:391) - MUST BE REMOVED

2) Duplicate authentication logic
- Partially accurate; the primary code paths for TVDB/TMDB now standardize auth via descriptors:
    - TVDB token refresh is centralized in [`_refresh_tvdb_token()`](utils/api_provider_descriptors.py:17) and cached via [`TokenCache()`](utils/api_provider_core.py:100).
    - TMDB uses a static read token injected by [`get_tmdb_descriptor()`](utils/api_provider_descriptors.py:89).
- IMDb still authenticates ad hoc with RapidAPI keys in functions like [`imdb_api_search_title()`](utils/imdb_core.py:129) and [`imdb_api_get_details()`](utils/imdb_core.py:215), not the provider abstraction.
- Legacy/auxiliary TVDB scripts likely still contain standalone auth flows (as indicated by authenticate/save_token patterns referenced in redundancy reports), but the main TVDB utility path uses the shared cache. Consider these auxiliary scripts out-of-scope unless you intend to consolidate scripts too.

3) Duplicate token caching (TVDB has 2 separate implementations)
- Outdated in mainline flow: TVDB’s active utility path uses the centralized [`TokenCache()`](utils/api_provider_core.py:100) via [`get_tvdb_descriptor()`](utils/api_provider_descriptors.py:67).
- There are older patterns (authenticate + save_token) present in auxiliary code referenced by the redundancy analysis, but they are not on the primary path used by the new descriptors. If you intend to reduce the repository footprint, you can archive/remove duplicate script-level auth logic later, without enabling TVDB.

4) Duplicate error handling
- Largely resolved for TVDB/TMDB through [`BaseApiProvider.get()`](utils/api_provider_core.py:48) which returns a standardized response dict and retries on transient failures.
- Persisting for IMDb: error handling is bespoke in functions using requests directly (eg, [`imdb_api_search_title()`](utils/imdb_core.py:129), [`imdb_api_get_details()`](utils/imdb_core.py:215), and the HTML scraping path).

5) Duplicate request/response formatting
- A normalization hook is modeled in descriptors (normalization_callbacks), but not fully leveraged. Each provider normalizes in its own utils; IMDb has rich normalization functions like [`imdb_details_normalize()`](utils/imdb_core.py:246) and inline normalization in [`imdb_search_for_media_core()`](utils/imdb_core.py:868).
- This duplication is acceptable if formats differ by provider; attempting to abstract normalization prematurely can overfit. Keep as-is unless strong convergence exists.

6) Insight: "All external APIs are HTTP requests with auth tokens"
- Needs correction for implementation:
    - IMDb ratings currently rely on HTML scraping: [`imdb_rating_scrape()`](utils/imdb_core.py:391) - THIS MUST BE REMOVED
    - IMDb API usage is key-based (RapidAPI), not a bearer token
    - After removing HTML scraping, IMDb should use ONLY RapidAPI calls
- Updated approach: "All external APIs are HTTP requests with proper authentication; TVDB/TMDB use bearer tokens, IMDb uses API keys via RapidAPI. HTML scraping is not allowed."

7) Proposed Solution: "Single BaseApiProvider class"
- Already implemented and in use for TVDB/TMDB: [`BaseApiProvider()`](utils/api_provider_core.py:13).
- Must be fully adopted by IMDb for all functionality. Remove all HTML scraping - IMDb should use ONLY API calls through the provider.

8) Cascade Eliminates counts (6 duplicate auth functions, 4 duplicate token mgmt functions, etc.)
- Counts are outdated given the new provider core and descriptors; actual remaining duplication is primarily:
    - IMDb’s direct RapidAPI calls and function-local error handling.
    - Auxiliary TVDB scripts with bespoke auth, not on the primary path.
- Recommendation: Recalculate duplication using the existing redundancy artifacts (eg, `redundancy_analysis_report.md`, `redundancy_analysis_detailed.json`) after IMDb adoption to report accurate post-change deltas.

9) Files Affected: “utils/imdb_core.py”
- Correct, but incomplete. To adopt the provider for IMDb you will also need to adjust the IMDb descriptor or provider usage:
    - The IMDb descriptor’s header_builder signature currently expects an argument (api_key) in [`get_imdb_descriptor()`](utils/api_provider_descriptors.py:111), while [`BaseApiProvider.get()`](utils/api_provider_core.py:48) calls `header_builder()` with no arguments by default. This mismatch will require one of:
        - Option A: Change `header_builder` for IMDb to a zero-arg lambda that reads from config/env internally; or
        - Option B: Always pass `headers_override` when calling `.get()` for IMDb so signature mismatches are avoided.
- Additional references that call IMDb core:
    - Consumer imports: [`routes/utils_user_media.py`](routes/utils_user_media.py:27)
    - Keep TMDB/TVDB code untouched (not enabled), but you may update comments and docs.

Updated, precise plan (minimal, safe, and aligned with constraints)
Scope constraints upheld:
- Keep IMDb active and fully operational using ONLY API calls.
- Remove all HTML scraping functionality from the application.
- Do not enable TVDB or TMDB; do not delete them.

Actions:
1) IMDb descriptor header builder alignment
- Action: Update [`get_imdb_descriptor()`](utils/api_provider_descriptors.py:111) so `header_builder` is zero-arg and internally resolves the API key from `current_app.config` (or env) to produce {'x-api-key': key}. This makes it compatible with [`BaseApiProvider.get()`](utils/api_provider_core.py:48) default header flow without passing headers_override.

2) IMDb search/details migration to BaseApiProvider
- Action: In [`utils/imdb_core.py`](utils/imdb_core.py), refactor [`imdb_api_search_title()`](utils/imdb_core.py:129) and [`imdb_api_get_details()`](utils/imdb_core.py:215) to use [`imdb_provider.get`](utils/imdb_core.py:38) with IMDb's base_url and provider-standard error handling. Preserve existing query parameter shapes and normalization via [`imdb_item_normalize()`](utils/imdb_core.py:59) and [`imdb_details_normalize()`](utils/imdb_core.py:246).

3) Remove HTML scraping functionality
- Action: REMOVE [`imdb_rating_scrape()`](utils/imdb_core.py:391) and all related HTML scraping code from [`utils/imdb_core.py`](utils/imdb_core.py).
- Action: Find and remove all calls to HTML scraping functions throughout the application.
- Action: If rating data is needed, obtain it through the RapidAPI instead (verify API provides rating data).

4) Standardized error paths for IMDb
- Action: Replace function-local try/except request blocks with centralized response checking:
    - If `response['success']` is False, propagate a standardized error dict or raise a ValueError with a consistent message, aligning with how TMDB/TVDB callers check provider responses.

5) Leave TVDB/TMDB code paths untouched (no enablement)
- Action: No functional changes to [`utils/api_tvdb/tvdb_utils.py`](utils/api_tvdb/tvdb_utils.py) or [`utils/api_tmdb/utils_tmdb_core.py`](utils/api_tmdb/utils_tmdb_core.py).
- Optional docs-only cleanup: Confirm README/comments no longer claim duplicate caches; point them to [`TokenCache()`](utils/api_provider_core.py:100).

6) Post-change verification
- Action: Run the IMDb-facing tests to confirm no regressions:
    - `tests/test_imdb_search.py`, routes that import IMDb core like [`routes/utils_user_media.py`](routes/utils_user_media.py:27).
- Action: Re-run redundancy metrics to update the “Cascade Eliminates” numbers in `redundancy_analysis_report.md`.

Risk/impact notes
- Header builder signature: essential to fix before switching IMDb calls to the provider; otherwise you'll get a TypeError due to a zero-arg call in [`BaseApiProvider.get()`](utils/api_provider_core.py:61).
- Removing HTML scraping: Verify RapidAPI provides all needed data (especially ratings). If ratings are unavailable via API, discuss alternative approaches with user.
- TVDB/TMDB remain dormant; no functional enablement occurs.

Revised assessment of the original plan's claims
- Single BaseApiProvider viability: Accurate (already present).
- IMDb auth unification: Needed and safe with the header-builder alignment.
- Remove HTML scraping: CRITICAL requirement - all HTML scraping must be removed, IMDb should use ONLY API calls.
- "All APIs use auth tokens": Updated to "All APIs use proper authentication (bearer tokens or API keys); no HTML scraping allowed".
- "Cascade Eliminates" counts: Outdated; recompute after IMDb migration and scraping removal.
- "Files Affected": At least `utils/imdb_core.py` and `utils/api_provider_descriptors.py`, plus any files that call HTML scraping functions. Do not modify TMDB/TVDB logic except comments/docs if desired.

This verifies the plan and provides a corrected update path that keeps IMDb fully operational using ONLY API calls, removes all HTML scraping, and does not enable or delete TVDB/TMDB.