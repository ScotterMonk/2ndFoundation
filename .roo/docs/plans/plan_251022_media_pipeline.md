# 251022_media_pipeline — Detailed Plan with Tasks
Short plan name: 251022_media_pipeline
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

## Phase 1: Architecture and contracts
Action: Create CoreResult and CoreError classes in `utils/media_core.py`.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Define CoreResult as a typed dict or dataclass with fields: ok (bool), data (dict), errors (list[str]), warnings (list[str]), code (str optional). Define CoreError exception class with taxonomy (VALIDATION_ERROR, TRANSFORM_ERROR, STORAGE_ERROR, etc.). Add docstrings with usage examples.
- Acceptance: CoreResult and CoreError defined with clear structure. No Flask imports. Types properly annotated.
- Integration: Will be imported by MediaFileHandler and all core functions returning results.

Action: Create MediaFileConfig dataclass in `utils/media_core.py`.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Define MediaFileConfig dataclass with fields: upload_folder (str), allowed_extensions (dict), max_file_sizes_mb (dict), enable_thumbnails (bool), enable_metadata_extraction (bool), enable_imdb (bool), enable_tvdb (bool), enable_tmdb (bool). Add validation method. Include docstring.
- Acceptance: MediaFileConfig defined. No default values reading from Flask config. Validation ensures required fields present.
- Integration: Routes will instantiate this from `current_app.config` and pass to handler.

Action: Define pipeline step interface in `utils/media_core.py`.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Create PipelineContext typed dict with fields: file_obj (FileStorage), user_id (int), media_type_code (str), config (MediaFileConfig), artifacts (dict), errors (list), warnings (list). Document that each pipeline step receives context and returns updated context or raises CoreError.
- Acceptance: PipelineContext clearly defined. Docstring explains pipeline pattern. No Flask dependencies.
- Integration: MediaFileHandler will use this interface for all pipeline steps.

Action: Update `config.py` to centralize media file settings.
- Mode: `/code-monkey`
- Files: `config.py`
- Action: Add MEDIA_UPLOAD_FOLDER, MEDIA_ALLOWED_EXTENSIONS (dict by media type), MEDIA_MAX_FILE_SIZES_MB (dict), MEDIA_ENABLE_THUMBNAILS, MEDIA_ENABLE_METADATA flags to Config class if not present. Ensure values match current hardcoded constants in `utils/media_core.py`.
- Acceptance: All media-related config centralized. Values accessible via `current_app.config` in routes.
- Integration: Routes will read these to build MediaFileConfig before calling core.

## Phase 2: Core handler foundation
Action: Create MediaFileHandler class skeleton in `utils/media_core.py`.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Define MediaFileHandler class with __init__ accepting MediaFileConfig. Add empty methods: validate_pipeline(ctx), transform_pipeline(ctx), storage_pipeline(ctx), process_file(file_obj, user_id, media_type_code) returning CoreResult. No Flask imports. Include comprehensive docstrings.
- Acceptance: MediaFileHandler class defined. Constructor stores config. Pipeline methods defined but not implemented. Returns CoreResult.
- Integration: Will be called by adapter functions in `utils/media.py` and eventually directly from routes.

Action: Implement validation pipeline in MediaFileHandler.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Implement validate_pipeline method. Check file exists, validate extension against config.allowed_extensions, seek to end for size check, validate size against config.max_file_sizes_mb, compute hash using existing `get_file_hash` logic (streaming), reset file pointer. Update context with file_size_bytes, file_hash. Raise CoreError on validation failure. Use pathlib for paths.
- Acceptance: validate_pipeline performs all checks. No Flask imports. Returns updated context. Raises CoreError with taxonomy code on failure.
- Integration: Called by process_file method. Uses config passed in, not Flask globals.

Action: Implement transform pipeline in MediaFileHandler.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Implement transform_pipeline method. If config.enable_thumbnails and media_type_code is 'image', generate thumbnail using PIL (if available) to temp location. If config.enable_metadata_extraction, extract metadata (image EXIF for images). Store thumbnail_path and metadata in context.artifacts. Handle missing PIL gracefully with warnings. Use pathlib. No Flask logging.
- Acceptance: transform_pipeline generates thumbnails and extracts metadata when enabled. Returns updated context with artifacts. No Flask dependencies. Handles PIL unavailable.
- Integration: Called by process_file method after validation.

Action: Implement storage pipeline in MediaFileHandler.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Implement storage_pipeline method. Create upload directory using pathlib (base_path from config / media_type_code / user_id). Generate unique filename (user_id_timestamp_securefilename). Use atomic write: save to temp file, then rename. Get MIME type. Store file_path, filename_stored, filename_original in context. Normalize path separators. Guard against path traversal.
- Acceptance: storage_pipeline saves file atomically. Creates directories. Returns context with file info. No Flask imports. Uses pathlib. Atomic writes implemented.
- Integration: Called by process_file method after transform. Uses config.upload_folder.

Action: Implement process_file orchestrator method in MediaFileHandler.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Implement process_file method to orchestrate all pipelines. Initialize PipelineContext. Call validate_pipeline, transform_pipeline, storage_pipeline in sequence. Catch CoreError exceptions and build CoreResult with errors. On success, return CoreResult with ok=True, data containing all file info and artifacts.
- Acceptance: process_file orchestrates full pipeline. Returns CoreResult in all cases. Handles errors gracefully. No Flask dependencies.
- Integration: Entry point for all file processing. Called by adapters and routes.

## Phase 3: Adapters and compatibility
Action: Create backward-compatible adapters in `utils/media.py`.
- Mode: `/code-monkey`
- Files: `utils/media.py`
- Action: For each existing function signature (validate_file, save_uploaded_file, process_uploaded_files, delete_media_files, generate_thumbnail, get_media_metadata), create adapter function that reads config from current_app.config, builds MediaFileConfig, instantiates MediaFileHandler, calls appropriate method, extracts result, and returns in original format (eg, tuple for validate_file). Mark with deprecation comment and `# Created by [model] | yyyy-mm-dd`.
- Acceptance: All original function signatures preserved. Adapters delegate to MediaFileHandler. Flask imports allowed in adapters. Original return formats maintained.
- Integration: Routes continue to work without changes initially.

Action: Add feature flag MEDIA_USE_NEW_HANDLER to `config.py`.
- Mode: `/task-simple`
- Files: `config.py`
- Action: Add MEDIA_USE_NEW_HANDLER = False to Config class. Document that this enables the new MediaFileHandler when True.
- Acceptance: Feature flag present and defaults to False for safety.
- Integration: Adapters will check this flag to decide between old and new code paths.

Action: Update adapters to check feature flag.
- Mode: `/code-monkey`
- Files: `utils/media.py`
- Action: Modify each adapter function to check current_app.config['MEDIA_USE_NEW_HANDLER']. If False, call original implementation (copy from `utils/media_core.py` duplicate functions). If True, use MediaFileHandler. Add logging to track which path is taken.
- Acceptance: Adapters support both code paths. Feature flag controls behavior. Logging indicates active path.
- Integration: Allows A/B testing and gradual rollout.

Action: Add shadow mode logging to adapters.
- Mode: `/code-monkey`
- Files: `utils/media.py`
- Action: When feature flag is False (using old code), also call MediaFileHandler in try/except, compare results (don't use), log discrepancies to current_app.logger. Mark as "SHADOW_MODE" in logs.
- Acceptance: Shadow mode runs new handler alongside old without affecting behavior. Logs comparison results and any errors.
- Integration: Enables validation of new handler before switching over.

## Phase 4: Route integration
Action: Update `routes/utils_admin_media.py` to use MediaFileHandler pattern.
- Mode: `/code-monkey`
- Files: `routes/utils_admin_media.py`
- Action: In upload_media_post_util (line 879), build MediaFileConfig from current_app.config. Pass to process_uploaded_files adapter. Use `utils/route_helpers.py` pattern if result is CoreResult: extract errors/warnings, flash appropriately, handle redirect. Keep existing UserAction logging.
- Acceptance: Route builds config and passes to adapter. Uses route_helpers for response handling. No changes to template contract.
- Integration: Admin upload flow uses new pattern (via adapter controlled by feature flag).

Action: Update `routes/utils_user_media.py` to use MediaFileHandler pattern.
- Mode: `/code-monkey`
- Files: `routes/utils_user_media.py`
- Action: Find media upload functions (search for validate_file, save_uploaded_file usage). Build MediaFileConfig from current_app.config. Pass to adapters. Use route_helpers for standardized responses. Preserve existing behavior.
- Acceptance: User routes build config and use adapters. Response handling via route_helpers. Existing tests pass.
- Integration: User upload flow uses new pattern (via adapter controlled by feature flag).

Action: Remove Flask imports from `utils/media_core.py`.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Remove line 22 (from flask import current_app). Find all current_app.logger usages (lines 592, 627, 654, 693, 738, etc.) and remove or replace with pass/warnings.warn. Find all current_app.config reads (lines 537, etc.) and remove (already using config parameter). Ensure no Flask dependencies remain.
- Acceptance: No Flask imports in `utils/media_core.py`. Code is framework-agnostic. All logging removed or replaced with warnings module.
- Integration: Core is now truly stateless and reusable.

## Phase 5: Data/file behavior hardening
Action: Implement atomic write pattern in storage_pipeline.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: In storage_pipeline method, modify to write to temp file (Path.with_suffix('.tmp')), then Path.rename() to final location. Ensure temp file cleanup on error. Add try/finally block.
- Acceptance: Files written atomically. No partial writes on error. Temp files cleaned up.
- Integration: Prevents corrupt files on failure.

Action: Add path traversal guards in storage_pipeline.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: In storage_pipeline, validate that resolved file_path (using Path.resolve()) is within expected upload directory. Raise CoreError(code='SECURITY_ERROR') if path traversal detected. Check filename doesn't contain '..' or absolute paths.
- Acceptance: Path traversal attempts raise security error. Only allows files within upload directory.
- Integration: Prevents malicious file path manipulation.

Action: Implement idempotent delete_media_files in MediaFileHandler.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Add delete_files method to MediaFileHandler accepting file_path and optional thumbnail_path. Use pathlib.Path.unlink(missing_ok=True). Return CoreResult with ok=True if files removed or didn't exist. Log warnings for errors but don't raise.
- Acceptance: Delete is idempotent. Returns success if files deleted or absent. Doesn't raise on missing files.
- Integration: Safe to call multiple times. Clean error handling.

Action: Standardize directory structure and document naming scheme.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Add module-level docstring documenting directory structure: `{upload_folder}/{media_type_code}/{user_id}/` for media files, `{upload_folder}/../thumbnails/{media_type_code}/{user_id}/` for thumbnails. Document filename format: `{user_id}_{timestamp}_{secure_original_name}`. Handle collisions by appending counter if needed.
- Acceptance: Directory structure documented. Naming scheme clear. Collision handling defined.
- Integration: Provides clear contract for file organization.

## Phase 6: Switch-over and de-duplication
Action: Enable feature flag in config for testing.
- Mode: `/task-simple`
- Files: `config.py`
- Action: Change MEDIA_USE_NEW_HANDLER to True in Config class. Commit change separately for easy revert.
- Acceptance: Feature flag enabled. New handler active.
- Integration: Routes now use MediaFileHandler through adapters.

Action: Verify shadow mode logs show parity.
- Mode: `/code-monkey`
- Files: Create `temp/verify_shadow_logs.py`
- Action: Write script to parse recent application logs for SHADOW_MODE entries. Count discrepancies between old and new handler results. Report statistics.
- Acceptance: Script runs successfully. Reports discrepancy count and details.
- Integration: Validates new handler produces same results as old.

Action: Remove duplicate function implementations from `utils/media_core.py`.
- Mode: `/code-monkey`
- Files: `utils/media_core.py`
- Action: Remove original standalone implementations of validate_file, allowed_file, generate_unique_filename, get_file_hash, get_file_size_mb, save_uploaded_file, generate_thumbnail, get_media_metadata, process_uploaded_files (lines 388-741). Keep only MediaFileHandler and constants (ALLOWED_EXTENSIONS, MAX_FILE_SIZES_MB until fully migrated to config).
- Acceptance: Duplicate implementations removed. Only MediaFileHandler remains in `utils/media_core.py`. File is significantly smaller.
- Integration: Old code no longer in core. All access via adapters.

Action: Update adapters to remove old code path.
- Mode: `/code-monkey`
- Files: `utils/media.py`
- Action: Remove feature flag check and old implementation branches from all adapter functions. Keep only MediaFileHandler code path. Remove shadow mode logging. Simplify to direct delegation.
- Acceptance: Adapters simplified. Single code path. No feature flag checks.
- Integration: Production code simplified.

Action: Add deprecation notices to adapter functions.
- Mode: `/task-simple`
- Files: `utils/media.py`
- Action: Add docstring warnings to each adapter function: "DEPRECATED: Call MediaFileHandler directly. This adapter maintained for backward compatibility only." Set deprecation date 30 days from current date.
- Acceptance: Deprecation notices clear. Timeline established.
- Integration: Encourages migration to direct handler usage.

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