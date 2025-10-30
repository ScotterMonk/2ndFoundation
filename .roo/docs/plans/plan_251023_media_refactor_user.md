# User Query: Media Route Refactoring

Refactor admin media route utilities (`routes/utils_admin_media.py` and `routes/utils_admin_media_files.py`) into smaller, modular, reusable components following the Core vs Presentation separation pattern.

Goals:
- Reduce files to ~150 lines (orchestration only)
- Extract stateless logic to `utils/*_core.py` files
- Create reusable components across admin and user routes
- Improve testability by separating business logic from Flask context
- Eliminate ~200 lines of near-duplicate code
- Align with existing `utils/route_helpers.py` and BaseApiProvider patterns
- Maintain template compatibility throughout

Settings:
- Autonomy Level: High
- Testing: Terminal and Browser (MCP Puppeteer with querystring auth)