# Database Knowledge Sources - Consolidation Analysis

## Current State Assessment

### Primary Sources of Truth (Keep)
1. `PGDB` (PostgreSQL database) - Primary source
2. `.roo/docs/database_schema.md` - Human-readable schema doc (1382 lines)
3. `models/models_*.py` (7 files) - SQLAlchemy ORM models
4. `.roo/rules/02-database.md` - Database rules for agents

### Supporting Documentation (Need Review)
5. `.roo/docs/pgdb_changes.md` - Change log (mentioned but may not exist)
6. `database_schema_actual.md` - Auto-generated schema (appears redundant)
7. `schema_discrepancies.json` - Comparison output

### Utility Scripts (Consolidate/Archive)
8. Multiple comparison/inspection scripts:
   - `compare_models.py`
   - `compare_schemas.py`
   - `schema_comparison.py`
   - `inspect_database_schema.py`
   - `generate_schema_documentation.py`
   - `get_schema.py`
   - `get_db_schema.py`
   - `check_db_schema.py`

## Recommendations for Consolidation

### 1) CRITICAL - Establish Single Source of Truth Hierarchy
```
PGDB → models_*.py → database_schema.md
```
- PGDB is reality
- Models are code truth
- database_schema.md is documentation truth

### 2) Consolidate Utility Scripts
Create single unified script: `utils/schema_inspector.py`

Combine functionality:
- Generate schema docs from PGDB
- Compare PGDB vs models
- Compare models vs schema doc
- List discrepancies
- Output to standardized location

Benefits:
- Reduces 8 scripts to 1
- Single command for all schema operations
- Consistent output format
- Easier to maintain

### 3) Documentation Consolidation
Keep:
- `.roo/docs/database_schema.md` - Primary human-readable doc
- `.roo/docs/pgdb_changes.md` - Change log (create if missing)

Remove/Archive:
- `database_schema_actual.md` - Redundant with database_schema.md
- `schema_discrepancies.json` - Generate on-demand only
- `model_comparison_results.md` - Generate on-demand only
- `model_discrepancies.md` - Generate on-demand only

### 4) Reduce Token Usage in Rules

Current `.roo/rules/02-database.md` is good but could reference instead of duplicate:
```markdown
## Structure
Primary doc: `.roo/docs/database_schema.md`
Models: `models/models_*.py` (7 files organized by domain)
Change log: `.roo/docs/pgdb_changes.md`
Inspector: `utils/schema_inspector.py` for comparisons
```

### 5) Establish Update Protocol
When DB changes occur:
1. Update PGDB first
2. Log change in `pgdb_changes.md`
3. Update appropriate `models_*.py`
4. Run `schema_inspector.py --update-docs` to regenerate `database_schema.md`
5. Commit all changes together

### 6) Archive Analysis Scripts
Move to `.roo/scripts/schema_analysis/`:
- All comparison scripts
- Historical analysis results
- Keep out of main directory

## Token Savings Estimate

Current per-task token load:
- 8 utility scripts × ~200 lines = ~1600 lines
- Duplicate schema docs = ~1400 lines
- Total: ~3000 lines of redundant context

After consolidation:
- 1 utility script = ~300 lines
- 1 schema doc = ~1400 lines
- Total: ~1700 lines

**Savings: ~43% reduction in schema-related token usage**

## Implementation Priority

High Priority:
1. Create `utils/schema_inspector.py` consolidating all scripts
2. Archive redundant schema documents
3. Create/verify `pgdb_changes.md` exists
4. Update `.roo/rules/02-database.md` with simplified references

Medium Priority:
5. Move analysis scripts to `.roo/scripts/schema_analysis/`
6. Document the new workflow in `agents.md`

Low Priority:
7. Add automated validation in CI/CD
8. Create schema version tracking

## Detailed Plan with Tasks

Project settings
- Size: Multi-Phase (larger project), many tasks per phase
- Autonomy: High
- Testing: Run py scripts in terminal (temporary helpers in `temp/` per `@\.roo\rules\01-general.md`)

Prep (common)
- Task 0.1: Create reports folder `.roo/docs/schema_reports/`.
    Mode hint: /task-simple.
    Action: Create directory `.roo/docs/schema_reports/` with `.gitkeep` file if directory is empty.

Phase 1) Establish Source-of-Truth policy and baseline
Purpose: Ratify SoT hierarchy and ensure baseline artifacts exist before tooling.
- Task 1.1: Create PG change log file.
    Mode hint: /docs-writer.
    Action: Create or touch `@/.roo/docs/pgdb_changes.md` with header "PGDB Change Log" and brief purpose line.
- Task 1.2: Add SoT statement to plan file.
    Mode hint: /docs-writer.
    Action: Verify plan file contains explicit SoT statement (PGDB → models → database_schema.md); add if missing.
- Task 1.3: Create inventory script for legacy artifacts.
    Mode hint: /code.
    Action: Author helper script `temp/inventory_schema_artifacts.py` that lists presence of `database_schema_actual.md`, `schema_discrepancies.json`, `model_comparison_results.md`, `model_discrepancies.md` and writes timestamped report to `.roo/docs/schema_reports/inventory_YYYYMMDD.md`.
    Leverage: Use stdlib only (os, pathlib, datetime); reference existing scripts for discovery patterns.
- Task 1.4: Execute inventory script.
    Mode hint: /task-simple.
    Action: Run `python temp/inventory_schema_artifacts.py` to generate inventory report in `.roo/docs/schema_reports/`.

Phase 2) Unified schema inspector utility
Purpose: Replace ad-hoc scripts with one canonical utility.
- Task 2.1: Create schema inspector CLI skeleton.
    Mode hint: /code.
    Action: Create `utils/schema_inspector.py` with argparse defining subcommands: introspect, compare-db-models, compare-models-doc, generate-docs, report; include proper file header with Created-or-Modified comment.
    Leverage: `utils/database.py` for DB connection; argparse for CLI.
- Task 2.2: Implement introspect subcommand.
    Mode hint: /code.
    Action: In `utils/schema_inspector.py`, implement introspect subcommand using SQLAlchemy Inspector to collect tables, columns, PK/FK, indexes, constraints, defaults from PGDB; output timestamped JSON to `.roo/docs/schema_reports/sok_introspect_YYYYMMDD_HHMM.json`.
    Leverage: `get_schema.py` introspection queries; `utils/database.py` connection.
- Task 2.3: Extract schema doc parser to shared utility.
    Mode hint: /code.
    Action: Extract `parse_markdown_schema()` function from `compare_schemas.py` into new utility `utils/schema_doc_parser.py`; update `compare_schemas.py` imports to use new module.
    Leverage: Existing `compare_schemas.py` parsing logic.
- Task 2.4: Implement compare-db-models subcommand.
    Mode hint: /code.
    Action: In `utils/schema_inspector.py`, implement compare-db-models to diff PGDB against ORM models (`models/models_*.py`); detect table/column presence, types, nullability, PK/FK, indexes; categorize discrepancies as critical vs warning; output timestamped JSON.
    Leverage: `schema_comparison.py` type maps; handle edge cases (type mismatches, composite PKs, FK actions, ORM naming differences).
- Task 2.5: Implement compare-models-doc subcommand.
    Mode hint: /code.
    Action: In `utils/schema_inspector.py`, implement compare-models-doc using `utils/schema_doc_parser.py` to diff ORM models against `@/.roo/docs/database_schema.md`; output timestamped JSON with consistent PK/column/FK parsing.
    Leverage: `utils/schema_doc_parser.py`.
- Task 2.6: Implement generate-docs subcommand.
    Mode hint: /code.
    Action: In `utils/schema_inspector.py`, implement generate-docs to (re)write `@/.roo/docs/database_schema.md` from PGDB with standardized header (generator notice, SoT reminder, UTC timestamp, command used); ensure stable table/column ordering matching PG.
    Leverage: `generate_schema_documentation.py` SQL patterns.
- Task 2.7: Implement report subcommand.
    Mode hint: /code.
    Action: In `utils/schema_inspector.py`, implement report to read JSON outputs and emit human-readable timestamped `sok_summary_*.md` listing totals and categorized discrepancies.

Phase 3) Documentation consolidation
Purpose: Single authoritative human-readable doc and maintained change log.
- Task 3.1: Regenerate database_schema.md with standardized format.
    Mode hint: /task-simple.
    Action: Run `python utils/schema_inspector.py generate-docs` to update `@/.roo/docs/database_schema.md` with standardized header and domain-organized sections.
- Task 3.2: Remove duplicate schema docs outside canonical path.
    Mode hint: /task-simple.
    Action: Verify no duplicate schema documentation exists outside `.roo/docs/database_schema.md` and `.roo/docs/schema_reports/`; document any found duplicates for Phase 5 archival.

Phase 4) Rules and workflow updates
Purpose: Align rules and agent guidance to canonical sources and protocol.
- Task 4.1: Update database rules file.
    Mode hint: /docs-writer.
    Action: Update `@/.roo/rules/02-database.md` to reference four canonical sources: `@\.roo\docs\database_schema.md`, `models/models_*.py`, `@\.roo\docs\pgdb_changes.md`, `utils/schema_inspector.py`; remove duplicated content.
- Task 4.2: Update agents.md with update protocol.
    Mode hint: /docs-writer.
    Action: Update `agents.md` with explicit DB update protocol: (1) Update PGDB, (2) Log in pgdb_changes.md, (3) Update ORM models, (4) Run schema_inspector.py generate-docs and comparisons, (5) Commit together; include example CLI invocations.

Phase 5) Repository restructuring and archival
Purpose: Remove redundancy from root; preserve history.
- Task 5.1: Create schema analysis directories.
    Mode hint: /task-simple.
    Action: Create `.roo/scripts/schema_analysis/` and `.roo/scripts/schema_analysis/history/` with `.gitkeep` files.
- Task 5.2: Move legacy comparison scripts to archive.
    Mode hint: /task-simple.
    Action: Move eight legacy scripts (`compare_models.py`, `compare_schemas.py`, `schema_comparison.py`, `inspect_database_schema.py`, `generate_schema_documentation.py`, `get_schema.py`, `get_db_schema.py`, `check_db_schema.py`) from repo root to `.roo/scripts/schema_analysis/`.
- Task 5.3: Move historical schema outputs to archive.
    Mode hint: /task-simple.
    Action: Move historical outputs (`database_schema_actual.md`, `schema_discrepancies.json`, `model_comparison_results.md`, `model_discrepancies.md`) from repo root to `.roo/scripts/schema_analysis/history/`.
- Task 5.4: Verify app startup after archival.
    Mode hint: /task-simple.
    Action: Run `python app.py` to verify application starts without import/runtime errors after file moves.

Phase 6) Validation and drift checks
Purpose: Ensure no critical drift remains before declaring consolidation done.
- Task 6.1: Generate final drift reports.
    Mode hint: /task-simple.
    Action: Run `python utils/schema_inspector.py compare-db-models` and `compare-models-doc` to write final reports `sok_compare_*_final.json` and `sok_summary_final.md` to `.roo/docs/schema_reports/`.
- Task 6.2: Resolve documentation drift.
    Mode hint: /docs-writer.
    Action: If final reports show doc drift, regenerate `@/.roo/docs/database_schema.md` from PGDB using generate-docs subcommand.
- Task 6.3: Resolve ORM model critical drifts.
    Mode hint: /code.
    Action: For each critical drift flagged by compare-db-models, align specific `models/models_*.py` definitions to match PGDB; re-run comparisons to verify downgrade to none/warning; verify app still starts.
    Handle: Missing tables/columns, type/nullability/PK/FK mismatches, essential indexes.
- Task 6.4: Verify zero critical drift remains.
    Mode hint: /task-simple.
    Action: Run final comparisons and generate `sok_summary_final.md`; verify zero critical drift reported; document any warnings with rationale; if critical drift remains, return to Task 6.3.

Phase 7) Future enhancements (low priority)
Purpose: Optional hardening after consolidation.
- Task 7.1: Create schema version tracking file.
    Mode hint: /docs-writer.
    Action: Create `@/.roo/docs/schema_version.txt` with initial version and document manual increment protocol tied to `pgdb_changes.md` updates.
- Task 7.2: Draft CI drift job design.
    Mode hint: /docs-writer.
    Action: Create `@/.roo/docs/ci_schema_drift.md` outlining pipeline step to run inspector comparisons and fail on critical drift; include commands and pass/fail criteria.

Success criteria
- One canonical inspector utility replaces ad-hoc scripts
- Single human-readable schema doc plus maintained change log
- Updated rules/docs point to canonical sources and new workflow
- Redundant scripts/docs archived outside main directories
- Clean comparison reports with no unresolved critical discrepancies
