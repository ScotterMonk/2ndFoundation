# User Query: API Provider Simplification

Create a plan based on this document: `.roo/docs/cascade-pre-plan-api-providers_new.md`

## Summary
Simplify API provider implementation by:
1) Unifying all providers under `BaseApiProvider`
2) Removing ALL HTML scraping functionality from IMDb
3) Standardizing authentication, error handling, and response patterns
4) IMDb should use ONLY API calls (RapidAPI)
5) All external APIs should be HTTP requests with proper authentication

## Constraints
CRITICAL:
- IMDB is used in this application. Keep active and fully operational.
- IMDB must use ONLY API calls. Remove all HTML scraping functionality from the application.
- TVDB and TMDB are not currently in use but may be used later:
    - Do not enable them.
    - Do not delete them.
- It is fine and preferred that TVDB and TMDB do not work.

## Key Files
- `utils/imdb_core.py` - Remove HTML scraping, migrate to BaseApiProvider
- `utils/api_provider_descriptors.py` - Fix header builder signature for IMDb
- `utils/api_provider_core.py` - BaseApiProvider class