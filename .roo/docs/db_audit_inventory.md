# Database Audit Inventory

## Documentation Files

### Primary Documentation
- `.roo/docs/database_schema.md` - Canonical schema documentation
- `.roo/docs/pgdb_changes.md` - Database change log
- `.roo/docs/schema_version.md` - Schema version tracking

### Audit and Analysis Reports
- `.roo/docs/db_audit_inventory.md` - Database usage inventory
- `.roo/docs/ci_drift_detection_design.md` - CI drift detection design
- `.roo/docs/simplifications-needed.md` - Simplification needs
- `.roo/docs/simplification.md` - Simplification documentation

### Schema Reports
- `.roo/docs/schema_reports/inventory_20251026_1548.md`
- `.roo/docs/schema_reports/inventory_20251026_1549.md`
- `.roo/docs/schema_reports/phase6_drift_analysis_summary.md`

### Old Versions
- `.roo/docs/old_versions/database_schema_20251026_112906.md`
- `.roo/docs/old_versions/01-general.md_20251025_160923.md`
- `.roo/docs/old_versions/AGENTS.md_2025-10-25_103012.md`
- `.roo/docs/old_versions/agents.md_20251025_101843.md`
- `.roo/docs/old_versions/agents.md_20251025_105207.md`
- `.roo/docs/old_versions/agents.md_20251025_161021.md`
- `.roo/docs/old_versions/AGENTS.md_20251025_162330.md`
- `.roo/docs/old_versions/analysis_app_backup_20251013.md`
- `.roo/docs/old_versions/model_discrepancies_20251026_2318.md`
- `.roo/docs/old_versions/model_comparison_results_20251026_2318.md`

### Plan Documents
- `.roo/docs/plans/plan_251022_api_unify.md`
- `.roo/docs/plans/plan_251022_media_pipeline.md`
- `.roo/docs/plans/plan_251022_media_pipeline_b.md`
- `.roo/docs/plans/plan_251023_media_refactor.md`
- `.roo/docs/plans/plan_251024_media_refactor.md`
- `.roo/docs/plans/plan_251025_consolidate_agents_files.md`
- `.roo/docs/plans/plan_251026_db_audit.md`
- `.roo/docs/plans/plan_251026_db_audit_user.md`
- `.roo/docs/plans/plan_251026_db_audit_log.md`
- `.roo/docs/plans/plan_251026_db_sok_consolidation.md`
- `.roo/docs/plans/plan_251026_db_sok_consolidation_user.md`
- `.roo/docs/plans/plan_251026_db_sok_consolidation_log.md`
- `.roo/docs/plans/plan_251027_db_final.md`
- `.roo/docs/plans/plan_251027_db_final_user.md`
- `.roo/docs/plans/plan_251027_db_final_log.md`
- `.roo/docs/plans_completed/plan_290929_core_separation.md`

### Rules Documentation
- `.roo/rules/02-database.md` - Database rules and workflow
- `.roo/rules/01-general.md` - General rules (includes DB references)

### Root Directory Documentation
- `agents.md` - Agent documentation (includes DB schema update protocol)
- `agents-backup.md` - Backup of agent documentation
- `reseller_conversion_summary.md` - Reseller conversion summary
- `login_registration_testing_plan.md` - Login/registration testing plan
- `authentication_feature_plan.md` - Authentication feature plan
- `redundancy_analysis.md` - Redundancy analysis
- `redundancy_analysis_detailed.json` - Detailed redundancy analysis
- `redundancy_analysis_report.md` - Redundancy analysis report

## Schema & Utility Scripts

### Root Directory Scripts
- `check_db_schema.py`
- `admin_setup.py`

### Temp Directory Scripts
#### Schema Inspection Scripts
- `temp/inventory_schema_artifacts.py` - Inventory schema artifacts
- `temp/test_introspect.py` - Test schema introspection
- `temp/test_introspect_simple.py` - Simple introspection test
- `temp/test_introspect_final.py` - Final introspection test
- `temp/test_introspect_basic.py` - Basic introspection test
- `temp/test_introspect_basicst.py` - Basic introspection test
- `temp/test_introspect_simplest.py` - Simplest introspection test
- `temp/test_schema_inspector_compare.py` - Test schema inspector compare
- `temp/run_schema_validate.py` - Run schema validation
- `temp/run_schema_compare.py` - Run schema comparison
- `temp/run_generate_docs.py` - Run documentation generation

#### Database Connection and Query Scripts
- `temp/verify_table_exists.py` - Verify table exists
- `temp/verify_database_connection.py` - Verify database connection
- `temp/get_db_tables.py` - Get database tables
- `temp/check_all_schemas.py` - Check all schemas
- `temp/get_model_tables.py` - Get model tables
- `temp/check_media_status.py` - Check media status
- `temp/check_media_ignore.py` - Check media ignore table
- `temp/temp_check_media.py` - Temporary check media
- `temp/temp_create_test_media.py` - Create test media
- `temp/temp_check_create_user.py` - Check create user
- `temp/temp_check_app_startup.py` - Check app startup

#### User and Authentication Scripts
- `temp/temp_update_database_passwords.py` - Update database passwords
- `temp/temp_password_analysis.py` - Analyze passwords
- `temp/temp_fix_user_password.py` - Fix user password
- `temp/temp_create_test_user.py` - Create test user
- `temp/check_user_admin_status.py` - Check user admin status
- `temp/diagnose_admin_access.py` - Diagnose admin access
- `temp/debug_admin_access_issue.py` - Debug admin access issue
- `temp/debug_delete_media.py` - Debug delete media
- `temp/test_admin_media_page.py` - Test admin media page
- `temp/test_missing_fields.py` - Test missing fields
- `temp/test_db_constraint_validation.py` - Test DB constraint validation
- `temp/test_log_action_fix.py` - Test log action fix
- `temp/test_upload_diagnosis.py` - Test upload diagnosis

#### Database Modification Scripts
- `temp/drop_user_media_affinity.py` - Drop user media affinity table
- `temp/temp_check_media_ignore.py` - Check media ignore table
- `remove_resellers_table.py` - Remove resellers table (in root)

### Utils Directory Scripts
- `utils/database.py` - Database connection and configuration
- `utils/schema_inspector.py` - Schema inspection utility
- `utils/schema_commands.py` - Schema commands utility
- `utils/schema_compare_core.py` - Schema comparison core
- `utils/schema_doc_parser.py` - Schema documentation parser

### Database Model Files
- `models/models_interaction.py` - Interaction models
- `models/models_media.py` - Media models
- `models/models_payment.py` - Payment models
- `models/models_referral.py` - Referral models
- `models/models_reseller.py` - Reseller models
- `models/models_support.py` - Support models
- `models/models_user.py` - User models

### Database Configuration
- `config.py` - Application configuration (includes DB settings)
- `.env` - Environment variables (includes DB credentials)

## Redundant/Obsolete Files

### Redundant Schema Inspection Scripts
- `temp/test_introspect.py` (Action: Archive - superseded by schema_inspector.py)
- `temp/test_introspect_simple.py` (Action: Archive - superseded by schema_inspector.py)
- `temp/test_introspect_final.py` (Action: Archive - superseded by schema_inspector.py)
- `temp/test_introspect_basic.py` (Action: Archive - superseded by schema_inspector.py)
- `temp/test_introspect_basicst.py` (Action: Archive - superseded by schema_inspector.py)
- `temp/test_introspect_simplest.py` (Action: Archive - superseded by schema_inspector.py)
- `temp/test_schema_inspector_compare.py` (Action: Archive - functionality now in schema_inspector.py)
- `temp/run_schema_validate.py` (Action: Archive - use schema_inspector.py validate instead)
- `temp/run_schema_compare.py` (Action: Archive - use schema_inspector.py compare-db-models instead)
- `temp/run_generate_docs.py` (Action: Archive - use schema_inspector.py generate-docs instead)

### Redundant Database Connection Scripts
- `temp/verify_database_connection.py` (Action: Archive - functionality now in utils/database.py)
- `temp/get_db_tables.py` (Action: Archive - functionality now in utils/schema_inspector.py)

### Redundant Documentation
- `.roo/docs/old_versions/agents.md_20251025_101843.md` (Action: Archive - multiple versions of same file)
- `.roo/docs/old_versions/agents.md_20251025_105207.md` (Action: Archive - multiple versions of same file)
- `.roo/docs/old_versions/agents.md_20251025_161021.md` (Action: Archive - multiple versions of same file)
- `.roo/docs/old_versions/AGENTS.md_2025-10-25_103012.md` (Action: Archive - multiple versions of same file)
- `.roo/docs/old_versions/AGENTS.md_20251025_162330.md` (Action: Archive - multiple versions of same file)

### Legacy Files
- `compare_models.py` (Action: Archive - superseded by schema_inspector.py)
- `schema_comparison.py` (Action: Archive - superseded by schema_inspector.py)
- `get_db_schema.py` (Action: Archive - superseded by schema_inspector.py)
- `inspect_database_schema.py` (Action: Archive - superseded by schema_inspector.py)
- `get_schema.py` (Action: Archive - superseded by schema_inspector.py)
- `generate_schema_documentation.py` (Action: Archive - superseded by schema_inspector.py)
- `compare_schemas.py` (Action: Archive - superseded by schema_inspector.py)

## Agent Rule Files Requiring Updates

- `.roo/rules/02-database.md` (Action: Update references in Phase 4)
- `.roo/rules/01-general.md` (Action: Update references in Phase 4)
- `agents.md` (Action: Update references in Phase 4)