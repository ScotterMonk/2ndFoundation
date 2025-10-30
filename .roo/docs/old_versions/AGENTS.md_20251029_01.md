# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Environment
Windows 11, VS Code, Powershell.

## Run Commands
- Never use Linux commands in terminal.
- Start app: `python app.py` (not `flask run`)
- Activate venv: `.\activate.ps1`

## Database Schema Update Protocol
When making database schema changes, follow this strict workflow:
1) Modify PGDB - Make changes directly to the live PostgreSQL database. Use [`.env`](.env:1) for credentials.
2) Update models_*.py - Update the appropriate SQLAlchemy model files in `@\models\` to match database changes (eg, [`models/models_user.py`](models/models_user.py:1))
3) Regenerate documentation - Run `python utils/schema_inspector.py generate-docs` to update [`database_schema.md`](.roo/docs/database_schema.md:1)
4) Log changes - Record the date and change in [`pgdb_changes.md`](.roo/docs/pgdb_changes.md:1)

Source of Truth hierarchy:
1) PGDB (live PostgreSQL)
2) models_*.py (SQLAlchemy) (eg, [`models/models_user.py`](models/models_user.py:1))
3) database_schema.md (generated) ([`database_schema.md`](.roo/docs/database_schema.md:1))

Schema Inspector utility: [`utils/schema_inspector.py`](utils/schema_inspector.py:1)
Commands (Windows/PowerShell):
- `python utils/schema_inspector.py introspect`
- `python utils/schema_inspector.py compare-db-models`
- `python utils/schema_inspector.py generate-docs`
- `python utils/schema_inspector.py validate`

Notes:
- Windows 11/PowerShell environment; do not use Linux commands
- Users' passwords in DB are hashed
- For complete details, see [`02-database.md`](.roo/rules/02-database.md:1)

## API Information
CRITICAL to Keep in mind:
- IMDB is used in this application. Keep active and fully operational.
- TVDB and TMDB are not currently in use but may be used later:
    - Do not enable them.
    - Do not delete them.
- It is fine and preferred that TVDB and TMDB do not work.