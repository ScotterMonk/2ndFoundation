# Plan: Database Schema and Usage Audit
Meta
- Short plan name: 251026_db_audit
- User query: [plan_251026_db_audit_user.md](.roo/docs/plans/plan_251026_db_audit_user.md)
- Autonomy level: High
- Testing type: Custom (choose minimal, fit-for-purpose; no new tests unless required)

Objectives
- Inventory all DB interactions
- Establish PGDB as ground truth and reconcile docs/models/queries
- Standardize created_at/updated_at handling with DB-managed defaults
- Remove redundant scripts and converge documentation

Authoritative docs and tools
- Documentation schema (canonical): [.roo/docs/database_schema.md](.roo/docs/database_schema.md)
- Actual schema export: [database_schema_actual.md](database_schema_actual.md)
- Tools to reuse:
    - [generate_schema_documentation.py](generate_schema_documentation.py)
    - [inspect_database_schema.py](inspect_database_schema.py)
    - [compare_schemas.py](compare_schemas.py) – Primary doc-vs-actual diff tool
    - [schema_comparison.py](schema_comparison.py) – Fallback only if compare_schemas.py fails
    - [compare_models.py](compare_models.py)
- Safety notes:
    - Never modify PGDB directly from any comparison script; all DB changes must be scripted under [temp/](temp) and approved/logged before execution
- Change log: [.roo/docs/pgdb_changes.md](.roo/docs/pgdb_changes.md)

Phases

0) Initialize and guardrails
- Determine this plan instance status: New (see log).
- Backup existing docs to [.roo/docs/old_versions/](.roo/docs/old_versions/)
- Canonicalize doc paths: use [.roo/docs/database_schema.md](.roo/docs/database_schema.md) as maintained documentation and [database_schema_actual.md](database_schema_actual.md) as fresh export; eliminate drift to .github/docs/.
Acceptance:
- Backups created for existing docs
- Canonical paths recorded in this plan

Tasks (Phase 0)
- Action: Backup .roo/docs/database_schema.md to .roo/docs/old_versions with timestamp suffix
  - Mode: task-simple
  - Integration: filesystem
  - Acceptance: Backup file exists in .roo/docs/old_versions/
- Action: Update compare_schemas.py documented_schema path to .roo/docs/database_schema.md if currently pointing elsewhere
  - Mode: code
  - Integration: compare_schemas.py
  - Acceptance: Script imports the canonical doc path constant
- Action: Create placeholder database_schema_actual.md if missing (empty header and note)
  - Mode: task-simple
  - Integration: filesystem
  - Acceptance: database_schema_actual.md present (will be overwritten in Phase 2)
- Action: Verify Python venv is active and required DB libs installed (psycopg2/psycopg2-binary); if not, activate via .\activate.ps1 and install using requirements.txt
  - Mode: task-simple
  - Integration: terminal
  - Acceptance: Running schema scripts shows no import errors; commands available in terminal
- Action: Confirm .env contains valid PG connection settings for live PGDB (host, port, dbname, user, password, sslmode if applicable)
  - Mode: task-simple
  - Integration: .env
  - Acceptance: Schema scripts can connect and run without authentication errors

1) Inventory DB usage
- Enumerate files that: import SQLAlchemy; use db, db.session, Model.query; issue raw SQL; or are standalone DB scripts under root, scripts-debug, temp.
- Produce an inventory matrix: file, interaction type(s), risk level.
Acceptance:
- Inventory published (plan log or artifact) covering models/, routes/, utils/, scripts

Tasks (Phase 1)
- Action: Generate .roo/docs/db_inventory.md by searching patterns: "(?i)from flask_sqlalchemy|import sqlalchemy|db\.session|Model\.query|text\(|execute\(" across repo
  - Mode: code-monkey
  - Integration: search_files, codebase_search
  - Acceptance: .roo/docs/db_inventory.md exists and lists files with interaction types
- Action: Append any root-level Python scripts touching PGDB to the inventory
  - Mode: task-simple
  - Integration: repository root scan (*.py)
  - Acceptance: Inventory includes root scripts and scripts-debug/, temp/

2) Establish ground truth (PGDB)
- Run [generate_schema_documentation.py](generate_schema_documentation.py) to export to [database_schema_actual.md](database_schema_actual.md)
- Optionally run [inspect_database_schema.py](inspect_database_schema.py) for a detailed snapshot
Acceptance:
- Fresh export generated successfully; basic table/view counts noted

Tasks (Phase 2)
- Action: Execute python generate_schema_documentation.py
  - Mode: task-simple
  - Integration: PGDB via .env, Psycopg2
  - Acceptance: database_schema_actual.md updated; console shows table/view counts
- Action: Execute python inspect_database_schema.py and store outputs if deeper detail required
  - Mode: task-simple
  - Integration: PGDB
  - Acceptance: Detailed schema snapshot artifacts generated without errors

3) Docs vs actual reconciliation
- Compare [database_schema_actual.md](database_schema_actual.md) vs [.roo/docs/database_schema.md](.roo/docs/database_schema.md) using [compare_schemas.py](compare_schemas.py) or [schema_comparison.py](schema_comparison.py)
- Choose convergence direction: update docs to match DB or propose DB changes. All DB changes require approval, scripts under temp/, entries in [.roo/docs/pgdb_changes.md](.roo/docs/pgdb_changes.md), then docs update.
Acceptance:
- Diff artifact produced (eg, schema_discrepancies.json or markdown)
- Decision recorded; docs updated or DB-change scripts drafted and logged

Tasks (Phase 3)
- Action: Execute python compare_schemas.py and capture outputs to schema_discrepancies.json or schema_diff.txt
  - Mode: task-simple
  - Integration: filesystem paths to both schema files
  - Acceptance: Diff artifact present with tables/columns mismatches
- Action: Record convergence decision in .roo/docs/plans/plan_251026_db_audit_log.md
  - Mode: task-simple
  - Integration: plan log
  - Acceptance: Log entry added describing chosen direction
- Action: If converging docs → update .roo/docs/database_schema.md to reflect actual DB deltas
  - Mode: code
  - Integration: .roo/docs/database_schema.md
  - Acceptance: Re-run compare_schemas shows no or reduced doc vs actual diffs
- Action: If converging DB → draft idempotent SQL/psql script in temp/ to implement approved changes and log in .roo/docs/pgdb_changes.md
  - Mode: code
  - Integration: temp/*.py, .roo/docs/pgdb_changes.md
  - Acceptance: Script file created; change logged with date; not executed until approved

4) Models vs DB reconciliation
- Use [compare_models.py](compare_models.py) to identify discrepancies (tables, columns, PKs, FKs, types, nullability).
- Update models to align:
    - Table names, columns, types, nullability, unique
    - PKs/FKs and relationships
    - created_at: prefer DB-managed insert default via server_default (eg, text('now()'))
    - updated_at: use onupdate only if DB trigger exists; otherwise leave app-managed updates and document the approach
- Re-run comparison to verify alignment and regenerate [model_comparison_results.md](model_comparison_results.md)
Acceptance:
- Acceptable/no discrepancies reported in [model_comparison_results.md](model_comparison_results.md)

Tasks (Phase 4)
- Action: Execute python compare_models.py to generate model_comparison_results.md
  - Mode: task-simple
  - Integration: Flask app context; models/models_*.py
  - Acceptance: model_comparison_results.md generated with discrepancy breakdown
- Action: Verify compare_models.py includes all model files (models/models_*.py) in its model_files list/glob; adjust if any files are omitted
  - Mode: code
  - Integration: [compare_models.py](compare_models.py)
  - Acceptance: Subsequent run scans all model files with no omissions
- Action: Resolve tables_only_in_schema by adding/removing corresponding models as appropriate
  - Mode: code
  - Integration: models/
  - Acceptance: Re-run compare_models shows tables_only_in_schema resolved
- Action: Resolve tables_only_in_models by deprecating/removing stale models or routing required DB additions to Phase 6 via temp script and approval; do not alter PGDB in this phase
  - Mode: code
  - Integration: models/ (for model removals/renames); [temp/](temp) scripts + [.roo/docs/pgdb_changes.md](.roo/docs/pgdb_changes.md) for DB additions via Phase 6
  - Acceptance: Re-run compare_models shows tables_only_in_models resolved; any DB change proposals documented and handled in Phase 6
- Action: Align columns_only_in_schema by adding missing columns in models with correct types and constraints
  - Mode: code
  - Integration: models/
  - Acceptance: Re-run compare_models shows columns_only_in_schema resolved
- Action: Align columns_only_in_models by removing/renaming columns in models or proposing DB additions (with approval)
  - Mode: code
  - Integration: models/, temp/ scripts if DB changes required
  - Acceptance: Re-run compare_models shows columns_only_in_models resolved
- Action: Fix type_mismatches using SQLAlchemy types mapping to PG types
  - Mode: code
  - Integration: models/
  - Acceptance: Re-run compare_models shows type_mismatches resolved
- Action: Fix nullable_mismatches by setting nullable flags to match DB
  - Mode: code
  - Integration: models/
  - Acceptance: Re-run compare_models shows nullable_mismatches resolved
- Action: Fix primary_key_mismatch to match DB composite/single PKs
  - Mode: code
  - Integration: models/
  - Acceptance: Re-run compare_models shows primary_key_mismatch resolved
- Action: Fix foreign_keys_only_in_schema and foreign_keys_only_in_models to match DB relations
  - Mode: code
  - Integration: models/
  - Acceptance: Re-run compare_models shows FK sections resolved
- Action: Audit created_at/updated_at columns to ensure server_default=text('now()') and onupdate=text('now()') only when DB triggers exist
  - Mode: code
  - Integration: models/
  - Acceptance: Created/updated columns standardized; compare_models unaffected; note decisions in useful.md

5) Query audit and corrections
- Review queries in routes/utils_*_*.py, utils/*_core.py, and root scripts to match reconciled models.
- Enforce standardized route responses via [utils/route_helpers.py](utils/route_helpers.py).
- Remove deprecated helpers and dead code discovered during audit.
Acceptance:
- Audited file checklist complete; queries validated against PGDB/models

Tasks (Phase 5)
- Action: For each file in .roo/docs/db_inventory.md, validate ORM/SQL references exist in reconciled models/schema
  - Mode: code-monkey
  - Integration: routes/, utils/, scripts
  - Acceptance: Annotated inventory with OK/fix notes saved alongside db_inventory.md
- Action: Replace any deprecated query patterns with SQLAlchemy ORM equivalents aligned to models
  - Mode: code
  - Integration: routes/, utils/
  - Acceptance: File-specific changes complete; queries run without errors in app context
- Action: Ensure route handlers use utils/route_helpers.py standardized responses
  - Mode: code
  - Integration: routes/
  - Acceptance: Handlers call handle_util_result()/handle_simple_util_result()/handle_delete_result() appropriately

6) Constraints, indexes, and integrity
- Verify uniqueness, FKs, and indexes assumed by code exist in PGDB.
- Propose necessary DB changes via idempotent scripts under [temp/](temp/), seek approval, execute, log in [.roo/docs/pgdb_changes.md](.roo/docs/pgdb_changes.md), and update docs/models accordingly.
Acceptance:
- Approved scripts present; logs updated; docs/models consistent

Tasks (Phase 6)
- Action: Cross-check model UniqueConstraint/Index declarations vs database_schema_actual.md
  - Mode: task-simple
  - Integration: models/, docs
  - Acceptance: List of mismatches created in .roo/docs/constraints_gap.md
- Action: Draft idempotent scripts in temp/ to add missing constraints/indexes; add entries in .roo/docs/pgdb_changes.md
  - Mode: code
  - Integration: temp/, .roo/docs/pgdb_changes.md
  - Acceptance: Scripts created with guard checks; changes logged; pending approval
- Action: Add idempotency and transaction guards to all DB change scripts (IF NOT EXISTS/DO $$ blocks; BEGIN/COMMIT; rollback on error)
  - Mode: code
  - Integration: [temp/](temp)
  - Acceptance: Scripts are safe to re-run without side effects; pgdb_changes.md references safety checks used

7) Final review, cleanup, documentation
- Remove redundant/superseded scripts and converge on single documentation location plus the actual export.
- Update [.roo/docs/database_schema.md](.roo/docs/database_schema.md) and add notable practices to [.roo/docs/useful.md](.roo/docs/useful.md)
- Add final plan log entry noting completion of audit work and artifacts produced.
Acceptance:
- Problems panel clean; docs up to date; final changes logged

Tasks (Phase 7)
- Action: Remove or archive redundant DB scripts identified during audit into .roo/docs/old_versions with timestamp
  - Mode: task-simple
  - Integration: filesystem
  - Acceptance: Redundant files removed or archived; inventory updated
- Action: Update .roo/docs/useful.md with DB audit findings and practices
  - Mode: docs-writer
  - Integration: .roo/docs/useful.md
  - Acceptance: Useful.md contains a succinct section on schema/docs/models alignment
- Action: Add final completion entry to .roo/docs/plans/plan_251026_db_audit_log.md
  - Mode: task-simple
  - Integration: plan log
  - Acceptance: Log contains final completion record with artifact pointers

Deliverables
- Updated [.roo/docs/database_schema.md](.roo/docs/database_schema.md)
- Fresh [database_schema_actual.md](database_schema_actual.md)
- Fresh [model_comparison_results.md](model_comparison_results.md)
- Diff artifact: [schema_discrepancies.json](schema_discrepancies.json) or equivalent
- Inventory matrix of DB-interacting files [.roo/docs/db_inventory.md](.roo/docs/db_inventory.md)
- Approved DB change scripts under [temp/](temp/)
- Updated [.roo/docs/pgdb_changes.md](.roo/docs/pgdb_changes.md)