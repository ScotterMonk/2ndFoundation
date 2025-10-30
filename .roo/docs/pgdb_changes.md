# PGDB Change Log
This file logs all PostgreSQL database changes, serving as the canonical record for modifications to schema, tables, columns, indexes, and related DB objects.2025-10-27 06:48; Added imdb_rating column (NUMERIC(3,1)) to tv_channels table

2025-10-27; Added primary key to users_faves_directors table (id column)
2025-10-27 - Verified imdb_rating NUMERIC(3, 1) already exists in tv_channels table (column was already present).
2025-10-27 - Renamed affinity_metadata to affinity_metadata_ in users_media_affinity table.2025-10-27 - Renamed metadata to _metadata in notifications table.
2025-10-27 - Renamed metadata to _metadata in media table.
2025-10-27 - Renamed metadata to _metadata in media_backup table.
2025-10-27 - Renamed metadata to _metadata in tv_channels table.
2025-10-27 - Renamed metadata to _metadata in media table.
2025-10-27 - Renamed metadata to _metadata in media_backup table.
2025-10-27 - Renamed metadata to _metadata in tv_channels table.
2025-10-27 - Renamed _metadata to metadata_ in media table.
2025-10-27 - Renamed _metadata to metadata_ in tv_channels table.

2025-10-27 17:06; Added primary key constraint to users_faves_directors.id column

2025-10-27 17:12; Added imdb_rating column to tv_channels table

2025-10-27 17:17; Task 3.16: Ensured tv_channels.imdb_rating NUMERIC(3,1) exists (ADD COLUMN IF NOT EXISTS executed; column already present). Reason: Align PGDB with reconciled ORM models (Phase 3, Task 3.16). Follow-up: Docs regenerated via Schema Inspector. Reference: temp/add_imdb_rating_tv_channels.py

2025-10-27 17:26; Task 3.18: Added PRIMARY KEY on users_faves_directors.id in PGDB after verifying non-null and uniqueness. Reason: Align PGDB and models; unblock model comparisons. Follow-up: Models updated; docs regenerated. Reference: temp/add_pk_users_faves_directors.py

2025-10-27 — Database Reconciliation Summary
- PGDB changes:
  - Added imdb_rating NUMERIC(3,1) to tv_channels (Task 3.16)
  - Added Primary Key on id for users_faves_directors (Task 3.18)
- Models:
  - Created models: users_media_affinity in [models/models_user.py](models/models_user.py), media_backup and tv_channels in [models/models_media.py](models/models_media.py)
  - Reconciled mismatches across all models in: [models/models_interaction.py](models/models_interaction.py), [models/models_media.py](models/models_media.py), [models/models_payment.py](models/models_payment.py), [models/models_referral.py](models/models_referral.py), [models/models_reseller.py](models/models_reseller.py), [models/models_support.py](models/models_support.py), [models/models_user.py](models/models_user.py)
  - Standardized timestamps: created_at uses server_default text('now()'); updated_at has no server default (application-managed)
  - Reserved/keyword columns reconciled: metadata columns mapped correctly as "metadata" with explicit Column mapping where needed
- Docs/Validation:
  - Regenerated canonical schema doc: [.roo/docs/database_schema.md](.roo/docs/database_schema.md)
  - Final validations:
    - compare-db-models: zero critical discrepancies
    - validate: PASS
    - VS Code Problems DB-related: none (per Task 6.3)
- Tooling/Cleanup:
  - Unified on single Schema Inspector utility: [utils/schema_inspector.py](utils/schema_inspector.py)
  - Obsolete scripts and duplicates archived under [.roo/docs/old_versions](.roo/docs/old_versions)
