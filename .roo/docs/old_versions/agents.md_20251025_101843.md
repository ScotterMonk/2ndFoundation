# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Environment
Windows 11, VS Code, Powershell.

## Run Commands
- Never use Linux commands in terminal.
- Start app: `python app.py` (not `flask run`)
- Activate venv: `.\activate.ps1`

## Critical Non-Standard Patterns

### Architecture: Core vs Presentation Separation
- `utils/*_core.py` - stateless business logic (no Flask context)
- `routes/utils_*_*.py` - Flask-aware presentation utilities
- Routes delegate to presentation utils, which call core functions
- This separation is MANDATORY - never mix Flask imports into `*_core.py` files

### Database
- PostgreSQL ONLY - never SQLite (even for dev/test)
- DB instance imported from `utils/database.py` not created in `app.py`
- Database scripts: Write to `temp/` folder and run, never paste multi-line scripts in terminal
- TestingConfig intentionally has `WTF_CSRF_ENABLED = False`

### Route Helpers Pattern
- `utils/route_helpers.py` provides standardized response handling
- Always use `handle_util_result()`, `handle_simple_util_result()`, or `handle_delete_result()`
- These handle success/error states, flash messages, and redirects consistently

### Media File Processing Pipeline
- Location: `utils/media_core.py`
- Core entities: CoreResult schema, CoreError taxonomy, MediaFileConfig dataclass
- Handler: MediaFileHandler orchestrates validate_pipeline, transform_pipeline, storage_pipeline
- Presentation pattern: Routes build MediaFileConfig from `config.py`, call handler from presentation utilities
- Legacy adapters in `utils/media.py` are deprecated - prefer direct handler usage
- Routes must translate CoreResult via `utils/route_helpers.py`
- Storage: {upload_folder}/{media_type_code}/{user_id}/, thumbnails at {upload_folder}/../thumbnails/
- Filename format: {user_id}_{timestamp}_{secure_original_name}
- Atomic writes: write to .tmp then rename; cleanup on error
- Idempotent deletes using Path.unlink(missing_ok=True)

### Browser Testing (web automation / browsing)
- `browser_action`

#### Preconditions
- Ensure the target web app/server is running before navigating (for localhost tasks).
- If it is not running, start it first.
- Safety when browsing:
    - Do not include secrets in screenshots or console logs.

#### Available Actions
Each action automatically returns: screenshot + console logs + page status
- `launch`: Start browser session at URL
- `click`: Click at specific x,y pixel coordinates  
- `type`: Type text into currently focused element
- `scroll_down`: Scroll down one page height
- `scroll_up`: Scroll up one page height
- `close`: End browser session

#### Important Workflow Rules
- Must start with `launch` and end with `close`
- Only ONE action per message
- While browser session is open (between `launch` and `close`), no other tools can be used
- Close the browser before running commands, editing files, or using other tools
- Coordinates are viewport-relative (not page-relative)
- Must target visible elements within current viewport
- Console logs are automatically included in each response - no separate retrieval needed

#### Authentication Strategy
PREFERRED: Login via querystring when safe and allowed:
http://localhost:5000/auth/login?email=[credentials]&password=[credentials]
- If any bug arises (including failed login with existing users), prepare a WTS package and delegate to `/debug`.
- After fix returns, retest the same flows.

#### Token Optimization
- Screenshot quality: 45-60% for text-based testing (default: 70%).
- Viewport size: Small Desktop (900×600) or Mobile (360×640) recommended.
- Disable browser tool in settings when not actively testing.

### Documentation
- Backups: `.roo/docs/old_versions/[file name without extension]_[timestamp]_[extension]`
- Logs and completed plans: `.roo/docs/plans_completed/`
- DB schema changes logged in `.roo/docs/pgdb_changes.md`

## External API Provider Framework

### BaseApiProvider
- `utils/api_provider_core.py` contains centralized `BaseApiProvider` class for all external API interactions
- Stateless design with no Flask context dependencies - suitable for use in `*_core.py` files
- Use this class instead of creating separate HTTP client code for each API

### Provider Descriptors
- `utils/api_provider_descriptors.py` defines configuration descriptors for all external APIs
- New API providers should be configured by adding a `DESCRIPTOR` dictionary in this file
- Descriptor-based approach is the standard - avoid creating separate utility files for each new API
- Supports multiple auth strategies: bearer tokens, API keys, static tokens
- Includes `TokenCache` class for automatic token refresh and caching

### Configuration
- All API-related settings (keys, URLs, timeouts) centralized in `config.py`
- API credentials and configuration sourced from `.env` file
- Current providers configured: TVDB, TMDB, IMDB