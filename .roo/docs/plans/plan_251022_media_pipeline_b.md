# 251022_media_pipeline_b — Detailed Plan with Tasks
Short plan name: 251022_media_pipeline_b
Project size/complexity: Multi-Phase (larger project), many tasks per phase
Autonomy level: High (rare direction)
Testing type: Use browser

## Context
Goal: Simplify media file operations by consolidating 21 duplicate functions into a single pipeline-based handler. Follow `@/.roo/docs/simplification.md`. Keep IMDB integration first-class; leave TVDB/TMDB pluggable for later.

## Constraints and principles
- Maintain core vs presentation separation: new core-only implementation (no Flask) lives in `utils/media_core.py`; routes call via presentation utils.
- Unify validation → transform → store/retrieve as a pipeline.
- Backwards-compatible adapters for current route utilities before removal of duplicates.
- Standardize error model (stateless dict result objects) for core; routes use `utils/route_helpers.py` to translate.
- Keep directories under `static/uploads/media` with consistent naming by media_type_code.
- Plan for future TVDB/TMDB transformers without adding dependencies now.
- Remove Flask/current_app usage from `utils/media_core.py`; core remains framework-agnostic. Logging and flash messaging occur in `routes/utils_*` via route_helpers.
- Centralize file-type and size limits in `config.py` and pass into core via parameters; core must not read Flask config directly.
- Standardize a CoreResult schema returned by core operations: ok (bool), data (dict), errors (list[str]), warnings (list[str]), code (str optional).

## Current state summary
- Duplicate groups across `utils/media.py` and `utils/media_core.py`: validate_file, allowed_file, generate_unique_filename, get_file_hash, get_file_size_mb, process_uploaded_files, save_uploaded_file, delete_media_files, generate_thumbnail, create_upload_directories, get_media_metadata.
- Existing imports show routes already using `process_uploaded_files` from `media_core` (line 879 in `routes/utils_admin_media.py`).
- Flask imports currently in `utils/media_core.py` (line 22: current_app) violate core/presentation separation.
- Config reading from current_app.config in `utils/media_core.py` (lines 537, 592, 627, 654, 693, 738).

## Target architecture (pipeline)
- MediaFileHandler (core): orchestrates three pipelines.
- Validation pipeline: file type, size, hash; configurable per media_type_code.
- Transform pipeline: thumbnail generation, metadata extraction (IMDB-first).
- Storage pipeline: unique naming, directory selection/creation, move/cleanup.
- Extensibility: optional transformers for TVDB/TMDB guarded by config flags.
- Compatibility layer: thin functions retaining current signatures for routes until migration completes.
- Pipeline step interface: each step consumes/produces a context dict (file, user_id, media_type_code, config, artifacts) and returns an updated context or raises a defined CoreError; handler aggregates into CoreResult.
- Config injection: routes build a config object (limits, directories, flags) and pass to the handler; core never reads Flask globals.
- File I/O strategy: use pathlib with atomic writes (temp file then rename) and normalized path separators.
- Security: guard against path traversal; validate MIME and extension; enforce max size.

## Phase 1: Architecture and contracts (completed phase)
Established core contracts and configuration patterns for the media pipeline architecture.

## Phase 2: Core handler foundation (completed phase)
Implemented the MediaFileHandler class with validation, transform, and storage pipelines.

## Phase 3: Adapters and compatibility (completed phase)
Created backward-compatible adapters with feature flags and shadow mode logging for gradual migration.

## Phase 4: Route integration (completed phase)
Updated route utilities to use the new MediaFileHandler pattern through adapters.

## Phase 5: Data/file behavior hardening (completed phase)
Implemented atomic writes, path traversal guards, and standardized directory structure.

## Phase 6: Switch-over and de-duplication (completed phase)
Removed duplicate implementations and simplified adapters to single code path.

## Phase 7: Browser verification
Action: Test admin media upload flow with Puppeteer.
- Mode: `/tester`
- Testing: Browser
- Action: Use Puppeteer to navigate to http://localhost:5000/auth/login with querystring auth (email and hashed password from `@\.env`). Navigate to admin media upload page. Select owner from dropdown. Select media type 'image'. Upload a test image file. Capture screenshot. Verify success message in UI. Check console logs (console://logs) for errors. Verify file appears in media list.
- Acceptance: Upload completes successfully. No console errors. File visible in admin media list. Thumbnail generated.
- Integration: Validates entire admin upload flow end-to-end.

Action: Test user media upload flow with Puppeteer.
- Mode: `/tester`
- Testing: Browser
- Action: Use Puppeteer with querystring login as regular user. Navigate to user media upload page. Select media type. Upload test file. Capture screenshot. Verify success. Check console logs. Verify file in user's media list.
- Acceptance: User upload works. No errors. File visible in user media list.
- Integration: Validates user upload flow.

Action: Test thumbnail generation verification with Puppeteer.
- Mode: `/tester`
- Testing: Browser
- Action: After admin upload, navigate to media detail/edit page for uploaded item. Capture screenshot. Verify thumbnail image loads (check for <img> element with thumbnail_path). Use puppeteer_evaluate to check if image loaded successfully (naturalWidth > 0).
- Acceptance: Thumbnail displays correctly. Image element present and loaded.
- Integration: Validates transform pipeline thumbnail generation.

Action: Test metadata population with Puppeteer.
- Mode: `/tester`
- Testing: Browser
- Action: After image upload, use puppeteer_evaluate to inspect media object or page content for metadata fields (width, height, format). Verify EXIF data present if applicable. Capture screenshot showing metadata.
- Acceptance: Metadata populated correctly. Width/height/format present for images.
- Integration: Validates transform pipeline metadata extraction.

Action: Test file deletion with Puppeteer.
- Mode: `/tester`
- Testing: Browser
- Action: Navigate to media management page. Click delete button for test media item. Confirm deletion in modal. Capture screenshot. Verify item removed from list. Verify no console errors.
- Acceptance: Deletion works. Item removed. No errors.
- Integration: Validates delete_files method.

Action: Test negative case - oversized file with Puppeteer.
- Mode: `/tester`
- Testing: Browser
- Action: Attempt to upload file larger than max size limit for media type. Capture screenshot. Verify error message displays in UI. Verify file not saved (check media list). No console errors except expected validation failure.
- Acceptance: Oversized file rejected. Clear error message. File not saved.
- Integration: Validates validation pipeline size check.

Action: Test negative case - disallowed file type with Puppeteer.
- Mode: `/tester`
- Testing: Browser
- Action: Attempt to upload .exe or other disallowed extension. Capture screenshot. Verify error message about file type. File not saved. No console errors.
- Acceptance: Disallowed type rejected. Clear error message shown.
- Integration: Validates validation pipeline extension check.

Action: Test negative case - transform failure handling.
- Mode: `/code-monkey` (setup) then `/tester` (verify)
- Action: Setup: Temporarily modify transform_pipeline to inject failure (eg, PIL import error simulation). Testing: Upload image via browser. Verify graceful degradation (file saved but no thumbnail). Verify warning message. Restore code. Re-test normal path works.
- Acceptance: Transform failures don't block upload. Warnings logged. File still saved.
- Integration: Validates error handling in transform pipeline.

## Phase 8: Documentation and handoff
Action: Create architecture diagram for media file pipeline.
- Mode: `/task-simple`
- Files: Create `.roo/docs/media_pipeline_architecture.md`
- Action: Document pipeline flow: Routes → Config Building → MediaFileHandler → Validation → Transform → Storage → CoreResult → Route Helpers → Response. Include class diagrams (text-based), data flow, and integration points. Reference existing files.
- Acceptance: Architecture clearly documented. Diagram shows flow and components.
- Integration: Provides reference for future developers.

Action: Create function mapping matrix.
- Mode: `/task-simple`
- Files: Create `.roo/docs/media_pipeline_migration.md`
- Action: Create table mapping old function names to new equivalents: validate_file → MediaFileHandler.validate_pipeline, process_uploaded_files → MediaFileHandler.process_file, etc. Include migration guide for developers.
- Acceptance: Clear mapping provided. Migration path documented.
- Integration: Helps developers transition to new API.

Action: Update `@\.roo\docs\useful.md` with pipeline pattern.
- Mode: `/task-simple`
- Files: `.roo/docs/useful.md`
- Action: Add section on MediaFileHandler pipeline pattern. Include example of building MediaFileConfig, calling process_file, handling CoreResult. Note benefits: framework-agnostic, testable, reusable.
- Acceptance: Pattern documented in useful discoveries. Example code included.
- Integration: Knowledge preserved for future reference.

Action: Document deprecation timeline.
- Mode: `/task-simple`
- Files: `.roo/docs/media_pipeline_migration.md`
- Action: Add timeline: Adapters in `utils/media.py` deprecated 30 days from plan completion. Routes should migrate to direct MediaFileHandler usage. After 60 days, adapters may be removed if no usage detected.
- Acceptance: Timeline clear. Migration expectations set.
- Integration: Provides transition period for cleanup.

Action: Update `agents.md` with media pipeline information.
- Mode: `/task-simple`
- Files: `agents.md`
- Action: Add section under Critical Non-Standard Patterns documenting MediaFileHandler: location (`utils/media_core.py`), usage pattern (build MediaFileConfig from routes, pass to handler.process_file, handle CoreResult), key principles (no Flask in core, config injection, pipeline pattern).
- Acceptance: `agents.md` updated. Pattern discoverable by future agents.
- Integration: Ensures knowledge persists for AI and human developers.

## Summary
This plan consolidates 21 duplicate media file functions into a unified pipeline-based MediaFileHandler. The implementation strictly maintains core/presentation separation, uses config injection, provides backward compatibility during migration, and includes comprehensive browser testing. Total estimated impact: ~1200 lines removed, single source of truth established, extensible architecture for future API integrations.