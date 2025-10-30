# Plan: Database Documentation Final Reconciliation

Meta
- Short plan name: 251027_db_final
- User query: `plan_251027_db_final_user.md`
- Autonomy level: High
- Testing type: No testing

Objectives
- Inventory all DB documentation that agents/modes use
- Establish PGDB as ground truth and reconcile docs, models, queries
- Standardize created_at with DB-managed defaults; updated_at application-managed
- Remove redundant scripts and converge documentation
- Complete work started in previous plans (251026_db_audit, 251026_db_sok_consolidation)

Source of Truth Hierarchy (per `@\.roo\rules\02-database.md`)
1) `PGDB` - Live PostgreSQL database (ultimate authority)
2) `models_*.py` - SQLAlchemy model definitions
3) `database_schema.md` - Generated documentation

Primary Tool
- `utils/schema_inspector.py` - Unified schema inspection and comparison utility
    - Commands: introspect, compare-db-models, compare-models-doc, generate-docs, report

Phases

## COMPLETED: Phase 1: Complete Documentation Inventory
Objective: Create comprehensive inventory of ALL database-related documentation, tools, and references across the project.
Scope:
- All documentation files referencing database schema
- All scripts/utilities for schema inspection or comparison
- All agent rule files that reference DB documentation
- Identify redundant, conflicting, or obsolete documentation
Acceptance:
- Inventory consolidated in `.roo/docs/db_audit_inventory.md` and marked canonical
- Redundant files identified for removal; categorized by archive/remove/update
- Single canonical documentation path confirmed: `.roo/docs/database_schema.md`
- Cross-references in agent/rule docs noted for Phase 4 updates

## COMPLETED: Phase 2: Establish PGDB Ground Truth
Objective: Use PGDB as definitive source and generate fresh, accurate documentation.
Scope:
- Run `python utils/schema_inspector.py introspect` to capture PGDB structure
- Run `python utils/schema_inspector.py generate-docs` to create fresh `database_schema.md`
- Run `python utils/schema_inspector.py compare-db-models` to identify ALL model discrepancies
- Document all findings in structured comparison report

Acceptance:
- Fresh `database_schema.md` generated from PGDB
- Comprehensive discrepancy report available in `.roo/reports/`
- Baseline established for all reconciliation work

## Phase 3: Reconcile Models with PGDB
Objective: Align all SQLAlchemy models exactly with PGDB structure.
Scope:
- Fix table name mismatches
- Fix column name mismatches
- Fix type mismatches
- Fix nullable mismatches
- Fix primary key mismatches
- Fix foreign key mismatches
- Standardize created_at with DB-managed defaults; ensure updated_at has no server defaults (application-managed)
- Verify all changes with re-run of compare-db-models

Tasks:
- Task 3.1: Analyze discrepancy report for critical issues.
    Mode hint: `/code-monkey`
    Action: Review `.roo/reports/db_models_discrepancies.json` and create prioritized fix list categorizing discrepancies as: table mismatches, column mismatches, type mismatches, nullable issues, PK/FK issues, timestamp handling.
    Output: Structured fix plan saved to working file.
- Task 3.2.1: Fix table/column/type/nullable issues in `models_interaction.py`.
    Mode hint: `/code`
    Action: Update `models/models_interaction.py` to match PGDB: fix `__tablename__` if needed, update column names/types/nullable per discrepancy report, use explicit `Column('db_name', ...)` syntax where ORM attributes differ from DB columns.
- Task 3.2.2: Fix table/column/type/nullable issues in `models_media.py`.
    Mode hint: `/code`
    Action: Update `models/models_media.py` to match PGDB: fix `__tablename__` if needed, update column names/types/nullable per discrepancy report, use explicit `Column('db_name', ...)` syntax where ORM attributes differ from DB columns.
- Task 3.2.3: Fix table/column/type/nullable issues in `models_payment.py`.
    Mode hint: `/code`
    Action: Update `models/models_payment.py` to match PGDB: fix `__tablename__` if needed, update column names/types/nullable per discrepancy report, use explicit `Column('db_name', ...)` syntax where ORM attributes differ from DB columns.
- Task 3.2.4: Fix table/column/type/nullable issues in `models_referral.py`.
    Mode hint: `/code`
    Action: Update `models/models_referral.py` to match PGDB: fix `__tablename__` if needed, update column names/types/nullable per discrepancy report, use explicit `Column('db_name', ...)` syntax where ORM attributes differ from DB columns.
- Task 3.2.5: Fix table/column/type/nullable issues in `models_reseller.py`.
    Mode hint: `/code`
    Action: Update `models/models_reseller.py` to match PGDB: fix `__tablename__` if needed, update column names/types/nullable per discrepancy report, use explicit `Column('db_name', ...)` syntax where ORM attributes differ from DB columns.
- Task 3.2.6: Fix table/column/type/nullable issues in `models_support.py`.
    Mode hint: `/code`
    Action: Update `models/models_support.py` to match PGDB: fix `__tablename__` if needed, update column names/types/nullable per discrepancy report, use explicit `Column('db_name', ...)` syntax where ORM attributes differ from DB columns.
- Task 3.2.7: Fix table/column/type/nullable issues in `models_user.py`.
    Mode hint: `/code`
    Action: Update `models/models_user.py` to match PGDB: fix `__tablename__` if needed, update column names/types/nullable per discrepancy report, use explicit `Column('db_name', ...)` syntax where ORM attributes differ from DB columns.
- Task 3.3.1: Fix PK/FK mismatches in `models_interaction.py`.
    Mode hint: `/code-monkey`
    Action: Update PK definitions and FK relationships in `models/models_interaction.py` to match PGDB constraints per discrepancy report.
- Task 3.3.2: Fix PK/FK mismatches in `models_media.py`.
    Mode hint: `/code-monkey`
    Action: Update PK definitions and FK relationships in `models/models_media.py` to match PGDB constraints per discrepancy report.
- Task 3.3.3: Fix PK/FK mismatches in `models_payment.py`.
    Mode hint: `/code-monkey`
    Action: Update PK definitions and FK relationships in `models/models_payment.py` to match PGDB constraints per discrepancy report.
- Task 3.3.4: Fix PK/FK mismatches in `models_referral.py`.
    Mode hint: `/code-monkey`
    Action: Update PK definitions and FK relationships in `models/models_referral.py` to match PGDB constraints per discrepancy report.
- Task 3.3.5: Fix PK/FK mismatches in `models_reseller.py`.
    Mode hint: `/code-monkey`
    Action: Update PK definitions and FK relationships in `models/models_reseller.py` to match PGDB constraints per discrepancy report.
- Task 3.3.6: Fix PK/FK mismatches in `models_support.py`.
    Mode hint: `/code-monkey`
    Action: Update PK definitions and FK relationships in `models/models_support.py` to match PGDB constraints per discrepancy report.
- Task 3.3.7: Fix PK/FK mismatches in `models_user.py`.
    Mode hint: `/code-monkey`
    Action: Update PK definitions and FK relationships in `models/models_user.py` to match PGDB constraints per discrepancy report.
- Task 3.3.8: Run timestamp column audit.
    Mode hint: `/task-simple`
    Action: Execute `python temp/audit_timestamp_columns.py` to generate comprehensive audit report of all `created_at`/`updated_at` columns across PGDB tables.
    Output: Generates `.roo/docs/timestamp_audit_[timestamp].md` and `.roo/docs/timestamp_audit_[timestamp].json` reports identifying tables missing timestamp columns, columns lacking proper DB-managed defaults, and nullable timestamp columns.
    Reference: Use this report to inform Tasks 3.4.1-3.4.7 timestamp standardization work.
- Task 3.4.1: Standardize timestamps in `models_interaction.py`.
    Mode hint: `/code-monkey`
    Action: Update `created_at` in `models/models_interaction.py` to use `server_default=text('now()')` matching PGDB; ensure updated_at has NO server default (application-managed only).
- Task 3.4.2: Standardize timestamps in `models_media.py`.
    Mode hint: `/code-monkey`
    Action: Update `created_at` in `models/models_media.py` to use `server_default=text('now()')` matching PGDB; ensure updated_at has NO server default (application-managed only).
- Task 3.4.3: Standardize timestamps in `models_payment.py`.
    Mode hint: `/code-monkey`
    Action: Update `created_at` in `models/models_payment.py` to use `server_default=text('now()')` matching PGDB; ensure updated_at has NO server default (application-managed only).
- Task 3.4.4: Standardize timestamps in `models_referral.py`.
    Mode hint: `/code-monkey`
    Action: Update `created_at` in `models/models_referral.py` to use `server_default=text('now()')` matching PGDB; ensure updated_at has NO server default (application-managed only).
- Task 3.4.5: Standardize timestamps in `models_reseller.py`.
    Mode hint: `/code-monkey`
    Action: Update `created_at` in `models/models_reseller.py` to use `server_default=text('now()')` matching PGDB; ensure updated_at has NO server default (application-managed only).
- Task 3.4.6: Standardize timestamps in `models_support.py`.
    Mode hint: `/code-monkey`
    Action: Update `created_at` in `models/models_support.py` to use `server_default=text('now()')` matching PGDB; ensure updated_at has NO server default (application-managed only).
- Task 3.4.7: Standardize timestamps in `models_user.py`.
    Mode hint: `/code-monkey`
    Action: Update `created_at` in `models/models_user.py` to use `server_default=text('now()')` matching PGDB; ensure updated_at has NO server default (application-managed only).

- Task 3.8: Create missing model for `users_media_affinity`.
    Mode hint: `/code`
    Action: Create a new SQLAlchemy model class in an appropriate `models_*.py` file for the `users_media_affinity` table. The model should accurately reflect the columns and types discovered during introspection.
    Reference: Use the introspection report (`sok_introspect_latest.json`) to define the model.
- Task 3.9: Create missing model for `media_backup`.
    Mode hint: `/code`
    Action: Create a new SQLAlchemy model class in an appropriate `models_*.py` file for the `media_backup` table.
    Reference: Use the introspection report (`sok_introspect_latest.json`) to define the model.
- Task 3.10: Create missing model for `tv_channels`.
    Mode hint: `/code`
    Action: Create a new SQLAlchemy model class in an appropriate `models_*.py` file for the `tv_channels` table.
    Reference: Use the introspection report (`sok_introspect_latest.json`) to define the model.
- Task 3.11: Correct PK mismatch in `users_faves_directors`.
    Mode hint: `/code-monkey`
    Action: In the `UserFaveDirector` model (likely in `models_user.py`), remove the `primary_key=True` attribute from the `id` column to align with the database, which has no primary key on this table.
- Task 3.13: Correct `metadata` column name mismatches.
    Mode hint: `/code`
    Action: Perform a search and replace across all `models_*.py` files. Replace any instance of a model attribute named `media_metadata`, `channel_metadata`, or `notification_metadata` with the correct database column name, `metadata`. Ensure this is done by updating the SQLAlchemy `Column` object, for example: `media_metadata = db.Column("metadata", db.JSON)` should become `metadata = db.Column("metadata", db.JSON)`.
- Task 3.14: Correct PK mismatch in `users_faves_directors`.
    Mode hint: `/code-monkey`
    Action: In the `UserFaveDirector` model in `models_user.py`, ensure the `id` column does NOT have `primary_key=True`. This is a re-verification of Task 3.11.
- Task 3.16: Add missing `imdb_rating` column to `tv_channels` table.
    Mode hint: `/code`
    Action: Create and execute a SQL script to add the `imdb_rating` column to the `tv_channels` table in the PGDB. The column should be of type `NUMERIC(3, 1)`. Log this change in `.roo/docs/pgdb_changes.md`.
- Task 3.17: Add missing `imdb_rating` column to `MediaBackup` model.
    Mode hint: `/code-monkey`
    Action: Add the `imdb_rating` attribute to the `MediaBackup` model in `models/models_media.py`. The column type should be `db.Numeric(3, 1)`.
- Task 3.18: Add Primary Key to `users_faves_directors` table.
    Mode hint: `/code`
    Action: Create and execute a SQL script to add a primary key to the `id` column of the `users_faves_directors` table in the PGDB. Log this change in `.roo/docs/pgdb_changes.md`.
- Task 3.19: Final, Escalated Verification Run.
    Mode hint: `/task-simple`
    Action: Re-run `python utils/schema_inspector.py compare-db-models --format json` for the last time to confirm that all critical discrepancies have been resolved.

Acceptance:
- `python utils/schema_inspector.py compare-db-models` shows zero critical discrepancies
- All models in `models_*.py` match PGDB structure
- created_at columns use DB defaults (server_default); updated_at columns have no server defaults (application-managed)

## Phase 3b: Reconcile Queries with PGDB
Objective: Ensure all application queries (ORM usage and any raw SQL) are consistent with PGDB and reconciled models.
Scope:
- Project-wide scan for raw SQL and column/table name usage in key areas: routes, utils, models, scripts-debug, and root scripts
- Cross-check usages against PGDB and updated models from Phase 3
- Update mismatched attribute/column references, including renamed columns and explicit mappings where db columns differ from ORM attribute names
- Remove or refactor obsolete queries touching dropped/renamed tables or columns
- Document notable fixes and patterns in `.roo/docs/useful.md`

Tasks:
- Task 3b.1: Search for raw SQL queries in codebase.
    Mode hint: `/code-monkey`
    Action: Use `search_files` with regex pattern `text\(|execute\(|db\.session\.execute|query\.filter_by|filter\(` in routes/, utils/, models/ to identify all direct SQL and ORM queries.
    Output: List of files/lines with SQL queries for review.
- Task 3b.2: Identify table/column references in queries.
    Mode hint: `/code-monkey`
    Action: Extract all table and column names referenced in queries found in Task 3b.1 and cross-reference against PGDB schema from `.roo/docs/database_schema.md`.
    Output: List of mismatched references requiring updates.
- Task 3b.3.1: Create per-file query update plan for routes.
    Mode hint: `/code-monkey`
    Action: Review Task 3b.2 mismatch list and create explicit file-by-file update plan for `routes/` directory, listing each affected file with specific column/table changes needed.
    Output: Structured update plan for Tasks 3b.3.2.x.
- Task 3b.3.2: Batch update all identified routes files.
    Mode hint: `/code`
    Action: For each file in Task 3b.3.1 plan, update queries to use correct PGDB column names or ORM attributes per Phase 3 reconciliation.
    Note: Single task handles all routes/ files identified in 3b.3.1 since they share common pattern (column name updates).
- Task 3b.3.3: Create per-file query update plan for utils.
    Mode hint: `/code-monkey`
    Action: Review Task 3b.2 mismatch list and create explicit file-by-file update plan for `utils/` directory, listing each affected file with specific column/table changes needed.
    Output: Structured update plan for Task 3b.3.4.
- Task 3b.3.4: Batch update all identified utils files.
    Mode hint: `/code`
    Action: For each file in Task 3b.3.3 plan, update queries to use correct PGDB column names or ORM attributes per Phase 3 reconciliation.
    Note: Single task handles all utils/ files identified in 3b.3.3 since they share common pattern (column name updates).
- Task 3b.3.5: Update relationship queries in models files.
    Mode hint: `/code-monkey`
    Action: Update relationship queries in `models/` files that reference old column names to use correct PGDB column names or ORM attributes per Phase 3 reconciliation.
    Note: Models already updated in Phase 3; this addresses any relationship/backref queries.
- Task 3b.4.1: Create obsolete query removal plan.
    Mode hint: `/code-monkey`
    Action: Review Phase 2 discrepancy report and create list of files in `routes/` and `utils/` that query dropped/renamed tables or columns, with specific removal actions.
    Output: File-specific removal plan for Task 3b.4.2.
- Task 3b.4.2: Batch remove/refactor obsolete queries.
    Mode hint: `/code`
    Action: For each file in Task 3b.4.1 plan, remove or refactor code querying non-existent tables/columns.
    Note: Single task handles all files since pattern is consistent (remove references to dropped entities).
- Task 3b.5: Document query reconciliation patterns.
    Mode hint: `/code-monkey`
    Action: Add entry to `.roo/docs/useful.md` documenting: common column remapping patterns, queries updated, and best practices for ORM attribute vs DB column name handling.

Acceptance:
- No references to non-existent tables/columns in codebase (verified via search and code review)
- ORM attributes map cleanly to PGDB columns; explicit mappings are accurate
- Re-run `python utils/schema_inspector.py compare-db-models` shows zero critical discrepancies
## Phase 4: Update Agent Documentation References
Objective: Ensure all agent rules and documentation point to single canonical source.
Scope:
- Update `.roo/rules/02-database.md` to reference canonical paths
- Update `agents.md` with Schema Inspector workflow
- Verify no conflicting documentation paths in rule files
- Remove or update references to obsolete tools/docs

Tasks:
- Task 4.1: Update `.roo/rules/02-database.md` with canonical paths.
    Mode hint: `/code-monkey`
    Action: Review and update all file path references in `.roo/rules/02-database.md` to point to canonical locations: `.roo/docs/database_schema.md` for schema docs, `utils/schema_inspector.py` for tooling, `models/models_*.py` for models.
    Note: Ensure Source of Truth hierarchy is clearly stated.
- Task 4.2: Update `agents.md` with Schema Inspector workflow.
    Mode hint: `/code-monkey`
    Action: Update Database Schema Update Protocol section in `agents.md` to reflect complete workflow using `utils/schema_inspector.py` commands (introspect, compare-db-models, generate-docs, validate).
    Reference: Existing workflow already documented; verify accuracy and completeness.
- Task 4.3: Scan rule files for obsolete DB doc references.
    Mode hint: `/code-monkey`
    Action: Use `search_files` with pattern `database_schema|db.*schema|schema.*doc` in `.roo/rules*/` to find all DB documentation references and create list for Task 4.4.
- Task 4.4.1: Update `.roo/rules/01-general.md` references.
    Mode hint: `/code-monkey`
    Action: Update all DB documentation references in `.roo/rules/01-general.md` to point to canonical `.roo/docs/database_schema.md`.
- Task 4.4.2.1: Update `.roo/rules-planner-a/01-planner-a.md` references.
    Mode hint: `/code-monkey`
    Action: Update all DB documentation references in `.roo/rules-planner-a/01-planner-a.md` to point to canonical `.roo/docs/database_schema.md`.
- Task 4.4.2.2: Update `.roo/rules-planner-b/01-planner-b.md` references.
    Mode hint: `/code-monkey`
    Action: Update all DB documentation references in `.roo/rules-planner-b/01-planner-b.md` to point to canonical `.roo/docs/database_schema.md`.
- Task 4.4.2.3: Update `.roo/rules-planner-c/01-planner-c.md` references.
    Mode hint: `/code-monkey`
    Action: Update all DB documentation references in `.roo/rules-planner-c/01-planner-c.md` to point to canonical `.roo/docs/database_schema.md`.
- Task 4.4.2.4: Update `.roo/rules-planner-d/01-planner-d.md` references.
    Mode hint: `/code-monkey`
    Action: Update all DB documentation references in `.roo/rules-planner-d/01-planner-d.md` to point to canonical `.roo/docs/database_schema.md`.
- Task 4.4.3: Update any other rule files per Task 4.3 findings.
    Mode hint: `/code-monkey`
    Action: Update DB documentation references in any additional `.roo/rules*/` files identified in Task 4.3 (if any) to point to canonical `.roo/docs/database_schema.md`.
    Note: Conditional task; execute only if Task 4.3 identifies files beyond those in 4.4.1 and 4.4.2.x.

Acceptance:
- All agent rules reference `.roo/docs/database_schema.md` as canonical
- Schema Inspector commands documented in agent rules
- No references to obsolete documentation files

## Phase 5: Clean Up Redundant Files
Objective: Remove or archive ALL redundant database scripts and documentation.
Scope:
- Archive redundant schema scripts from root and `temp/`
- Remove conflicting documentation files
- Clean up old comparison/introspection scripts
- Update `.roo/docs/useful.md` with lessons learned

Tasks:
- Task 5.1: Create archive task list from Phase 1 inventory.
    Mode hint: `/code-monkey`
    Action: Review Phase 1 inventory and create explicit list of files to archive from root directory and `temp/` folder, grouping by category (schema scripts, check scripts, introspection scripts).
    Output: Structured list for Tasks 5.2.x.
- Task 5.2.1: Archive root-level check scripts.
    Mode hint: `/task-simple`
    Action: Move `check_db*.py` files from root directory to `.roo/docs/old_versions/` with timestamp suffix per Task 5.1 list.
- Task 5.2.2: Archive root-level schema scripts.
    Mode hint: `/task-simple`
    Action: Move `*schema*.py` files from root directory to `.roo/docs/old_versions/` with timestamp suffix per Task 5.1 list.
- Task 5.2.3: Archive temp introspection scripts.
    Mode hint: `/task-simple`
    Action: Move `temp/test_introspect*.py` and `temp/inventory_schema_artifacts.py` to `.roo/docs/old_versions/` with timestamp suffix per Task 5.1 list.
- Task 5.4: Identify competing documentation files.
    Mode hint: `/code-monkey`
    Action: Review Phase 1 inventory and create explicit list of schema documentation files to archive (excluding canonical `.roo/docs/database_schema.md`).
    Output: List saved to working file for Tasks 5.5.x.
- Task 5.5: Archive competing documentation per inventory list.
    Mode hint: `/task-simple`
    Action: Move each competing schema documentation file from Task 5.4 list to `.roo/docs/old_versions/` with timestamp suffix, leaving only `.roo/docs/database_schema.md`.
- Task 5.6: Verify single schema operation tool.
    Mode hint: `/task-simple`
    Action: Confirm only `utils/schema_inspector.py` exists for schema operations by verifying no other schema inspection/comparison tools remain in `utils/` or root directories.
- Task 5.7: Document lessons learned in `useful.md`.
    Mode hint: `/code-monkey`
    Action: Add comprehensive entry to `.roo/docs/useful.md` documenting: (a) schema reconciliation process, (b) PGDB as SoT hierarchy, (c) proper use of `utils/schema_inspector.py`, (d) column mapping patterns discovered, (e) timestamp handling: created_at with server_default, updated_at application-managed.

Acceptance:
- Only `utils/schema_inspector.py` remains for schema operations
- Only `.roo/docs/database_schema.md` exists for schema documentation
- Obsolete files moved to `.roo/docs/old_versions/`
- `useful.md` updated with schema reconciliation best practices

## Phase 6: Final Validation & Documentation
Objective: Verify complete reconciliation and document the process.
Scope:
- Run all Schema Inspector validation commands
- Verify VS Code Problems panel is clean
- Update `.roo/docs/pgdb_changes.md` with reconciliation summary
- Create final reconciliation report

Tasks:
- Task 6.1: Run final schema validation.
    Mode hint: `/task-simple`
    Action: Execute `python utils/schema_inspector.py validate` to verify `.roo/docs/database_schema.md` is current with PGDB.
    Expected: Validation passes with no discrepancies.
- Task 6.2: Run final DB-models comparison.
    Mode hint: `/task-simple`
    Action: Execute `python utils/schema_inspector.py compare-db-models` to verify zero critical discrepancies between PGDB and all `models_*.py` files.
    Expected: Zero critical discrepancies reported.
- Task 6.3: Check VS Code Problems panel.
    Mode hint: `/task-simple`
    Action: Review VS Code Problems panel for any database-related errors or warnings in models, queries, or schema-related code.
    Expected: No database-related problems.
- Task 6.4: Update `pgdb_changes.md` with reconciliation summary.
    Mode hint: `/code-monkey`
    Action: Add dated entry to `.roo/docs/pgdb_changes.md` documenting: reconciliation date, changes made to models, timestamp standardization implemented, files archived, final validation results.
- Task 6.5: Create final reconciliation report.
    Mode hint: `/code-monkey`
    Action: Generate comprehensive reconciliation report documenting: (a) inventory results, (b) discrepancies found and fixed, (c) models updated, (d) queries reconciled, (e) documentation updated, (f) files archived, (g) validation results. Save to `.roo/reports/db_reconciliation_final.md`.
- Task 6.6.1: Archive completed plan file.
    Mode hint: `/task-simple`
    Action: Move `plan_251027_db_final.md` to `.roo/docs/plans_completed/` with completion timestamp.
- Task 6.6.2: Archive completed log file.
    Mode hint: `/task-simple`
    Action: Move `plan_251027_db_final_log.md` to `.roo/docs/plans_completed/` with completion timestamp.
- Task 6.6.3: Archive user query file.
    Mode hint: `/task-simple`
    Action: Move `plan_251027_db_final_user.md` to `.roo/docs/plans_completed/` with completion timestamp.

Acceptance:
- All validation commands pass
- No VS Code Problems related to database code
- Complete reconciliation documented
- Project ready for ongoing development with clear SoT hierarchy