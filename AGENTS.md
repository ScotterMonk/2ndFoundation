# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Environment & Run Commands
Windows 11 - Use PowerShell commands
- Activate venv: `.\activate.ps1`
- Run app: To be determined (skeleton - no app.py yet; will use Flask app factory pattern)
- Database port: 5433 (non-standard)
- Database scripts: Write to `temp/` folder (create if needed), never paste multi-line scripts in terminal

## Critical Non-Standard Patterns
Naming convention reverses typical order.
    Pattern: {specific}_{domain} -> {domain}_{specific}
    Examples:
    - `admin_dashboard_utils.py`, `user_dashboard_utils.py` -> `dashboard_utils_admin.py`, `dashboard_utils_user.py`
    - `scott_utils.py`, `kim_utils.py` -> `utils_scott.py`, `utils_kim.py`
    - `scott_core_utils.py`, `kim_core_utils.py` -> `utils_scott_core.py`, `utils_kim_core.py`
    - `edit_user`, `add_user` -> `user_edit`, `user_add`

All functions/classes MUST include header: `# [Created-or-Modified] by [LLM model] | yyyy-mm-dd_[iteration]`

Templates use `jinja-html` language mode, not `html`

File limit: <400 lines; modularize into `utils/` liberally.

## Database
PostgreSQL only (never SQLite) on port 5433
See `.env` file for db credentials.
Source of truth hierarchy: 1) Live PGDB → 2) `models/models_*.py` → 3) `.roo/docs/database_schema.md` (when created)

Schema changes workflow (when database is built):
1) Modify PGDB
2) Update `models/models_*.py`
3) Run: `python utils/schema_inspector.py generate-docs` (creates `.roo/docs/database_schema.md`)
4) Log in `.roo/docs/pgdb_changes.md` (create if needed)

## Testing
Testing types: "Run py scripts in terminal", "Use pytest", "Use browser", "Use all", "No testing", "Custom"

Multi-line Python scripts: Never run in terminal - write to `temp/` folder first (create folder if needed)

Browser testing: Use `browser_action` tool. Details in `.roo/rules/01-general.md`.

## Configuration
PostgreSQL port 5433 (not default 5432)
Embedding model default: sentence-transformers/all-MiniLM-L6-v2
Config object pattern: Use `config_by_name` dictionary in `config.py`

## Documentation
Markdown formatting:
- Minimal vertical spacing
- Numbered lists: `1)` not `1.`
- File refs: Back-ticks `file.py` not brackets `[file.py]()`
- Emphasis: Colons not bold
- No double-asterisks

Planning tracked in `.roo/docs/plans/` with specific naming: `plan_[timestamp]_[yymmdd_two_word]_[type].md`
Useful discoveries: `.roo/docs/useful.md` (create if needed)