# Tester Mode - Non-Obvious Patterns

This file provides guidance to agents when working with code in this repository.

## Test Database (CRITICAL)
- PostgreSQL ONLY - never SQLite (even for dev/test)
- Tests use live PostgreSQL database, not a separate test DB
- TestingConfig intentionally has `WTF_CSRF_ENABLED = False`

## Test Scripts
- Database scripts: Write to `temp/` folder and run, never paste multi-line scripts in terminal
- When creating a script to "check the database", write a temp .py file in `temp/` folder and run it

## Browser Testing (web automation / browsing)
- `browser_action`

### Preconditions
- Ensure the target web app/server is running before navigating (for localhost tasks).
- If it is not running, start it first.

### Available Actions
Each action automatically returns: screenshot + console logs + page status

- `launch`: Start browser session at URL
- `click`: Click at specific x,y pixel coordinates  
- `type`: Type text into currently focused element
- `scroll_down`: Scroll down one page height
- `scroll_up`: Scroll up one page height
- `close`: End browser session

### Important Workflow Rules
- Must start with `launch` and end with `close`
- Only ONE action per message
- While browser session is open (between `launch` and `close`), no other tools can be used
- Close the browser before running commands, editing files, or using other tools
- Coordinates are viewport-relative (not page-relative)
- Must target visible elements within current viewport
- Console logs are automatically included in each response - no separate retrieval needed

### Authentication Strategy
PREFERRED: Login via querystring when safe and allowed:
http://localhost:5000/auth/login?email=[credentials]&password=[credentials]
- If any bug arises (including failed login with existing users), prepare a WTS package and delegate to `/debug`.
- After fix returns, retest the same flows.

### Token Optimization
- Screenshot quality: 40-60% for text-based testing (default: 75%).
- Viewport size: Small Desktop (900×600) or Mobile (360×640) recommended.
- Disable browser tool in settings when not actively testing.

## Code Patterns to Test
- Core vs Presentation Separation: `utils/*_core.py` vs `routes/utils_*_*.py`
- Route Helpers: verify usage of `handle_util_result()`, `handle_simple_util_result()`, `handle_delete_result()`
- Media Pipeline: CoreResult translation, atomic writes, idempotent deletes