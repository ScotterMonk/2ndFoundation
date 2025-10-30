# Useful Discoveries

## IMDB Media Update Redirect Bug Fix (2025-10-25)

**Problem**: After selecting an IMDB search result in admin media edit workflow, redirect failed with 404 error.

**Root Cause**: JavaScript hardcoded redirect URL in [`templates/admin/media_edit_pull_results.html`](templates/admin/media_edit_pull_results.html:273) used outdated URL pattern `/admin/media_edit/` instead of correct `/admin/media/edit/`.

**Fix**: Updated line 273 from:
```javascript
window.location.href = `/admin/media_edit/${mediaId}?imdb_success=true&message=IMDb data successfully imported`;
```
To:
```javascript  
window.location.href = `/admin/media/edit/${mediaId}?imdb_success=true&message=IMDb data successfully imported`;
```

**Context**: Flask route was correctly refactored from `/media_edit/<id>` to `/media/edit/<id>` for consistency, but this template redirect wasn't updated. All other references use proper Flask `url_for('admin.media_edit')` pattern.

**Testing**: Verified fix works - IMDB selection now successfully redirects to edit page with HTTP 200 instead of 404.

**Backup**: Created backup at `media_edit_pull_results.html_20251025_152130`.

**Pattern**: When refactoring route URLs, check for hardcoded JavaScript redirects in templates that might need updating alongside Flask `url_for()` calls.
## Database query reconciliation patterns (Phase 3b, 2025-10-27/28)
- Summary: Phase 3b scan completed with 0 mismatches and 0 obsolete references; see reports: [`temp/query_scan_20251027_3b1.json`](temp/query_scan_20251027_3b1.json), [`temp/query_scan_20251027_3b1.md`](temp/query_scan_20251027_3b1.md), [`temp/query_mismatches_20251027_3b2.json`](temp/query_mismatches_20251027_3b2.json), [`temp/query_mismatches_20251027_3b2.md`](temp/query_mismatches_20251027_3b2.md), [`temp/obsolete_query_removal_plan_20251027.json`](temp/obsolete_query_removal_plan_20251027.json), [`temp/obsolete_query_removal_plan_20251027.md`](temp/obsolete_query_removal_plan_20251027.md), [`temp/routes_query_update_plan_20251027.json`](temp/routes_query_update_plan_20251027.json), [`temp/routes_query_update_plan_20251027.md`](temp/routes_query_update_plan_20251027.md), [`temp/utils_query_update_plan_20251027.json`](temp/utils_query_update_plan_20251027.json), [`temp/utils_query_update_plan_20251027.md`](temp/utils_query_update_plan_20251027.md), [`temp/models_relationship_query_updates_20251027.json`](temp/models_relationship_query_updates_20251027.json), [`temp/models_relationship_query_updates_20251027.md`](temp/models_relationship_query_updates_20251027.md)
- Search patterns used: inline matches for raw/ORM queries including: text(, execute(, db.session.execute, query.filter_by, filter(, join(, select(, update(, delete(, order_by(; regex built with [`python.re.compile()`](utils/schema_inspector.py:1)
- Common mapping patterns:
  - Explicit column mapping via [`python.db.Column()`](models/models_user.py:1): attr_name = db.Column("db_column_name", Type, nullable=..., primary_key=..., unique=...)
  - Reserved keyword avoidance for metadata: use attribute metadata_ mapped to DB column "_metadata"; example in [`models/models_user.py`](models/models_user.py)
- Timestamp handling: created_at uses DB default server_default=text('now()'); updated_at has no server_default and is managed in application logic; acceptance reference: [`plan_251027_db_final_Part-02.md`](.roo/docs/plans/plan_251027_db_final_Part-02.md:252)
- Source of Truth hierarchy: PGDB > models_*.py > database_schema.md; refs: [`02-database.md`](.roo/rules/02-database.md), [`database_schema.md`](.roo/docs/database_schema.md)
- Schema Inspector commands: compare-db-models, generate-docs, validate; entry points in [`utils/schema_inspector.py`](utils/schema_inspector.py:1)
Entry date: 2025-10-28
## 2025-10-27 DB Reconciliation: Lessons Learned
PGDB was affirmed as ground truth; SQLAlchemy models (models_*.py) were reconciled iteratively until compare-db-models yielded zero critical discrepancies; app/raw queries were cross-checked against live columns and types; documentation was standardized to one canonical generator; redundant scripts/docs were archived to converge on a single tool and a single set of schema docs.

Source of Truth (SoT):
- 1) PGDB (live)
- 2) models_*.py (SQLAlchemy)
- 3) @\.roo\docs\database_schema.md (generated)

Schema Inspector usage:
- `python utils/schema_inspector.py introspect` — capture live schema
- `python utils/schema_inspector.py compare-db-models` — find discrepancies
- `python utils/schema_inspector.py generate-docs` — regenerate @\.roo\docs\database_schema.md
- `python utils/schema_inspector.py validate` — verify docs current

Column/type mapping patterns:
- INTEGER → `db.Integer`; BIGINT → `db.BigInteger`; SMALLINT → `db.SmallInteger`
- VARCHAR(n) → `db.String(n)`; TEXT → `db.Text`; BOOLEAN → `db.Boolean`
- NUMERIC(p, s) → `db.Numeric(p, s)`; JSON/JSONB → `db.JSON`
- TIMESTAMP W/O TZ → `db.DateTime(timezone=False)`; W/ TZ → `db.DateTime(timezone=True)`
- UUID → `db.UUID(as_uuid=True)` or `db.String(36)` when needed
- Explicit column mapping when ORM attribute differs: `attr = db.Column('db_column_name', Type, ...)`
- Reserved name handling: use safe attribute name (eg, `metadata_`) explicitly mapped to db column (eg, `"_metadata"`)

Timestamp handling standard:
- `created_at`: DB-managed default, `server_default=text('now()')`
- `updated_at`: application-managed only (no server default)

Archival and convergence outcomes:
- Archived root-level check and schema scripts into @\.roo\docs\old_versions
- Archived temp introspection scripts into @\.roo\docs\old_versions
- Archived competing docs from @\.roo\docs\schema_reports\ into @\.roo\docs\old_versions
- Verified and enforced single schema tool: `utils/schema_inspector.py`
- Archived extra utils: `utils/schema_commands.py`, `utils/schema_compare_core.py`, `utils/schema_doc_parser.py`

Final verification note:
After archive enforcement, proceed to Phase 6 validation runs using the single tool.