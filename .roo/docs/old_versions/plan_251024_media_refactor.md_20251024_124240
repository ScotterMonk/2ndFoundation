# Refactoring Plan: Admin Media Routes Modularization

## Overview
## EXECUTION NOTES FOR ORCHESTRATOR

Mode: `/code-monkey` for all code creation/refactoring tasks
Mode: `/tester` for Phase 4, Task 4.3
Mode: `/front-end` for Phase 4, Task 4.1 (template verification)

Autonomy Level: High
Testing Strategy: Terminal (Python scripts in `temp/` + live PostgreSQL pytest) and Browser (MCP Puppeteer with querystring auth)

CRITICAL Task Atomicity:
- Task 1.1: Contains 4 functions - execute as 4 iterative sub-tasks
- Task 1.3: Contains 2 functions - execute as 2 iterative sub-tasks
- Task 2.1: Contains 2 functions - execute as 2 iterative sub-tasks
- Task 2.2: Contains 3 functions - execute as 3 iterative sub-tasks
- Task 2.3: Contains 3 functions - execute as 3 iterative sub-tasks
- Task 4.3: Contains 4 test files - execute as 4 iterative sub-tasks

EXISTING CODE TO REUSE:
- Sort helpers already exist in `utils/media_core.py` lines 408-483 (_created_sort_tuple, _title_tuple, _type_tuple, _rating_tuple) - DO NOT duplicate
- CoreResult schema, error taxonomy, MediaFileConfig, MediaFileHandler already exist in `utils/media_core.py`
- merge_and_deduplicate_results exists in `utils/media_core.py` lines 485-581

Refactor admin media route utilities (`routes/utils_admin_media.py` and `routes/utils_admin_media_files.py`) into smaller, modular, reusable components following the Core vs Presentation separation pattern.

## Current State

### routes/utils_admin_media.py (702 lines)
- `media_management_util()`: 237 lines
- `media_edit_util()`: 431 lines
- Heavy duplication in genre/director/performer processing (~200 lines)
- Repetitive AJAX vs regular request handling (~8 occurrences)

### routes/utils_admin_media_files.py (551 lines)
- `upload_media_get_util()`: 106 lines
- `upload_media_post_util()`: 211 lines
- `select_owner_util()`: 112 lines
- `select_owner_search_util()`: 118 lines
- Duplicated user query building logic (~80 lines between two functions)
- Repetitive validation patterns (owner, media type, CSRF)
- Extensive logging throughout

Total: 1,253 lines across 6 functions

## Goals
- Reduce files to ~150 lines (orchestration only)
- Extract stateless logic to `utils/*_core.py` files
- Create reusable components across admin and user routes
- Improve testability by separating business logic from Flask context
- Eliminate ~200 lines of near-duplicate code
- Align with existing `utils/route_helpers.py` and BaseApiProvider patterns
- Maintain template compatibility throughout

## Phase 0: Pre-flight Bug Fixes

Action: Address critical bugs that are currently blocking the testing and validation of the refactoring work.

### Task 0.1: Fix `NotNullViolation` in User Action Logging
Mode hint: /debug
Action: Modify the `UserAction.log_action` method in `models/models_user.py` to correctly handle logging for unauthenticated users.
Details:
- The `user_login_failed` action type is logged without a valid `user_id`, causing a `NotNullViolation` because the `users_id` column in the `users_actions` table does not allow null values.
- The `log_action` static method should be updated to provide a default or placeholder value if `user_id` is `None`, or the call sites need to be fixed to not log actions for non-existent users. The former is preferable to ensure all actions are logged.
Integration points:
- `models/models_user.py`

### Task 0.2: Fix `404` Error for Admin Upload Route
Mode hint: /debug
Action: Correct all invalid references to the admin upload URL.
Details:
- The terminal logs show GET requests to `/admin/upload`, which results in a `404 Not Found` error.
- The correct route is defined in `routes/admin.py` with the URL `/media/upload` under the `admin_bp` blueprint, making the full path `/admin/media/upload`.
- Search the codebase for any hardcoded URLs or `url_for` calls that incorrectly generate `/admin/upload` and correct them to `/admin/media/upload`.
Integration points:
- `routes/admin.py`
- Any template or Python file making an incorrect call.

### Task 0.3: Fix `AttributeError: 'dict' object has no attribute 'ok'` in Upload Util
Mode hint: /debug
Action: Resolve the data contract mismatch for the return value of `MediaFileHandler.process_file`.
Details:
- The `upload_media_post_util` function in `routes/utils_admin_media_files.py` expects `handler.process_file` to return a `CoreResult` object (with an `.ok` attribute).
- However, it is receiving a dictionary, causing the `AttributeError`. The previous fix using `.get('ok', False)` was a temporary patch, not the correct solution.
- The root cause must be fixed by ensuring `MediaFileHandler.process_file` in `utils/media_core.py` consistently returns a `CoreResult` object as defined by the project's architectural standards.
Integration points:
- `routes/utils_admin_media_files.py`
- `utils/media_core.py`

---

## Phase 1: Core Logic Extraction

### Task 1.1: Create `utils/media_query_core.py`
Mode hint: /code-monkey
Action: Extract stateless query, filtering, sorting, and pagination logic into new core module.

Functions to create:
- `build_media_search_query(db_session, search_term, genre_id=None)` 
  - Returns SQLAlchemy query with filters applied
  - Use SQL-level filtering for performance
  - No Flask imports
- `normalize_media_results(media_list)`
  - Convert ORM objects to dicts
  - Add computed fields (timestamps, sort keys)
  - Ensure consistent shape for templates
  - Input/output contract: accepts list of Media ORM objects, returns list of dicts with keys: id, title, rating, created_at, media_type, owner_username
- `sort_media_results(results, sort_field, direction)`
  - Leverage existing sort helper functions from `utils/media_core.py` (_created_sort_tuple, _title_tuple, etc.)
  - Support multiple sort fields: rating, title, type, created_at
  - Pure function operating on normalized dicts
- `paginate_media_query(query, page, per_page=20, allow_python_fallback=False)`
  - UNIFIED pagination function (simplifies from original plan's two functions)
  - Primary: SQL-level pagination using limit/offset and count for SQLAlchemy queries
  - Fallback: Python-level pagination for list results (only if allow_python_fallback=True)
  - Returns dict: {items: results, total: count, page: page, per_page: per_page, has_next: bool, has_prev: bool}
  - Raises warning if Python fallback used on large datasets (>100 items)

Integration points:
- Reuse existing private sort helpers from `utils/media_core.py` (_created_sort_tuple, _title_tuple, etc.) - do NOT create duplicates
- Use CoreResult schema for error handling
- Use Python logging (not Flask logger): `logger = logging.getLogger(__name__)`
- Document data shape contracts for template compatibility

### Task 1.2: Create `utils/media_associations_core.py`
Mode hint: /code-monkey
Action: Create generic association processor to replace 200+ lines of repetitive code.

SIMPLIFIED parameterized function:
```python
def process_media_associations(
    db_session,
    media_id,
    csv_string,
    association_model,  # MediaGenre, MediaDirector, MediaPerformer
    entity_model,       # Genre, Director, Performer  
    entity_field='name',
    create_if_missing=True
):
    """
    Generic processor for media associations (genres, directors, performers).
    
    Returns: CoreResult with {ok, data: {created, skipped, entity_ids}, errors, code}
    """
```

### Task 1.3: Create `utils/user_query_core.py`
Mode hint: /code-monkey
Action: Extract stateless user query building and filtering logic (owner selection).

Functions to create:
- `build_user_search_query(db_session, search_term, active_only=True, resellers_only=False)`
  - Used by both `select_owner_util()` and `select_owner_search_util()`
  - Returns SQLAlchemy query with User filters applied
  - Handles active/inactive filtering
  - Handles reseller-type filtering
  - Handles search pattern matching (username, email)
  - No Flask imports
- `prepare_user_list_data(users)`
  - Convert User ORM objects to dict format
  - Add `is_reseller` flag based on user_type
  - Pure data transformation
  - Returns list of dicts with keys: id, username, email, is_active, is_reseller

Replaces:
- Query building in `select_owner_util()` (lines 352-376)
- Query building in `select_owner_search_util()` (lines 480-504)
- User data preparation (lines 390-399 and 517-527)

## Phase 2: Presentation Layer Extraction

### Task 2.1: Create `routes/utils_admin_forms.py`
Mode hint: /code-monkey
Action: Extract Flask-aware request parameter and form data extraction.

Functions to create:
- `extract_search_params(request)`
  - Returns: `{search_term, genre_id, sort, direction}`
  - Handle multiple parameter name variations
  - Default values for missing parameters
- `extract_media_form_data(request)`
  - Returns dict with all form fields
  - Handles type conversions (int, bool)
  - Validates required fields
  - Returns tuple: (data_dict, validation_errors)

### Task 2.2: Extend `utils/route_helpers.py`
Mode hint: /code-monkey
Action: SIMPLIFIED - Add minimal helpers that complement existing functions, NOT a complete rewrite.

CRITICAL: The existing `handle_util_result()` already handles most cases. Only add what's truly missing.

Functions to add (REDUCED from 6 to 3):
- `is_ajax_request(request)`
  - Checks `X-Requested-With` header and `accept_mimetypes`
  - Centralizes AJAX detection logic
  - Reusable across admin and user routes
- `build_multi_message_response(messages, redirect_url)`
  - Handle list of (message_type, message_text) tuples
  - Flash all messages before redirect
  - Return redirect response
  - Useful for upload processing with multiple file results
- `sanitize_redirect_url(url, allowed_paths=None, default='/')`
  - Validates redirect URLs to prevent open redirect vulnerabilities
  - Checks against whitelist of allowed paths
  - Returns sanitized URL or default

REMOVED unnecessary functions:
- build_validation_error_response - use existing handle_util_result with appropriate dict
- build_success_response - use existing handle_util_result
- build_processing_error_response - use existing handle_util_result
- validate_csrf_token - Flask-WTF already provides this, no need to wrap it

Integration with existing route_helpers.py:
- Complement (don't replace) existing handle_util_result pattern
- Single source of truth for response formatting
- No duplication with existing functions

File size addition: ~50 lines (reduced from 140)

### Task 2.3: Create `routes/utils_admin_upload.py`
Mode hint: /code-monkey
Action: Extract upload-specific form validation and data extraction.

Functions to create:
- `validate_upload_requirements(request, db_session, require_owner=True, require_media_type=True)`
  - Extract and validate owner_user_id and media_type_id
  - Verify owner exists and is active
  - Verify media_type exists
  - Returns dict: `{valid: bool, owner: User|None, media_type: MediaType|None, errors: list}`
- `extract_uploaded_files(request, file_field='file')`
  - Get files from request
  - Filter empty file entries
  - Returns list of valid FileStorage objects
- `prepare_media_record_data(file_info, owner, media_type, admin_user)`
  - Build Media model fields from MediaFileHandler result
  - Set default values (is_public, is_featured, etc.)
  - Returns dict ready for Media() constructor

Replaces:
- Validation in `upload_media_post_util()` (lines 136-185)
- File extraction (lines 188-199)
- Media record creation (lines 214-240)

## Phase 3: Refactor Main Functions

### Task 3.1: Refactor `media_management_util()`
Mode hint: /code-monkey
Action: Simplify to orchestration-only using extracted modules.

Key changes:
- Use `utils/imdb_core.py` (already uses BaseApiProvider - no transition needed)
- Use unified pagination function for both DB and mixed results
- Separate display: DB results paginated, external suggestions in sidebar

New structure:
```python
def media_management_util():
    """Orchestrate media management page display."""
    try:
        from utils.media_query_core import (
            build_media_search_query, normalize_media_results,
            sort_media_results, paginate_media_query
        )
        from utils.imdb_core import search_media as imdb_search
        from routes.utils_admin_forms import extract_search_params
        
        # Extract params
        params = extract_search_params(request)
        
        # Build and paginate DB query (SQL-level)
        query = build_media_search_query(
            db.session, params['search_term'], params['genre_id']
        )
        page = request.args.get('page', 1, type=int)
        page_result = paginate_media_query(query, page)
        
        # Load genres for dropdown
        genres = Genre.query.order_by(Genre.name.asc()).all()
        
        # IMDb search (capped to 20 results for suggestions)
        external_results = []
        if params['search_term']:
            imdb_result = imdb_search(params['search_term'], limit=20)
            if imdb_result.ok:
                external_results = imdb_result.data.get('results', [])
        
        # Normalize and sort DB results
        normalized = normalize_media_results(page_result['items'])
        sorted_media = sort_media_results(normalized, params['sort'], params['direction'])
        
        return {
            'success': True,
            'template': 'admin/media.html',
            'data': {
                'media': sorted_media,
                'external_suggestions': external_results[:10],
                'q': params['search_term'],
                'sort': params['sort'],
                'direction': params['direction'],
                'genres': genres,
                'genre_id': params['genre_id'],
                'pagination': {
                    'page': page_result['page'],
                    'per_page': page_result['per_page'],
                    'total': page_result['total'],
                    'has_next': page_result['has_next'],
                    'has_prev': page_result['has_prev']
                }
            }
        }
    except Exception as e:
        logger.error(f"Error in media_management_util: {str(e)}", exc_info=True)
        return {'success': False, 'error': str(e), 'status_code': 500}
```

Target size: ~60 lines (down from 237)

Acceptance criteria:
- Same query filters/total counts as before
- Same visible sort order for identical inputs
- Same flashes/redirects for error cases
- DB round trips: 2 queries max (count + results)
- External API: graceful degradation if provider fails
- Template renders without changes

### Task 3.2: Refactor `media_edit_util()`
Mode hint: /code-monkey
Action: Simplify using extracted modules, especially association processor.

Key changes:
- Use simplified process_media_associations (fewer parameters)
- Use existing handle_util_result from utils/route_helpers.py
- Transaction wrapping for association updates

New structure for POST processing:
```python
# After basic field updates

# Process genres (uses CoreResult)
if imdb_genres_str:
    from utils.media_associations_core import process_media_associations
    genre_result = process_media_associations(
        db.session, media_item.id, imdb_genres_str,
        MediaGenre, Genre, 
        create_if_missing=False
    )
    if not genre_result.ok:
        return handle_util_result({
            'success': False,
            'message': f"Error processing genres: {', '.join(genre_result.errors)}",
            'template': 'admin/media_edit.html',
            'data': {'media': media_item, 'media_types': media_types}
        })

# Similar for directors and performers
```

Target size: ~120 lines (down from 431)

### Task 3.3: Refactor `upload_media_get_util()`
Mode hint: /code-monkey
Action: Simplify to orchestration using extracted validation.

Target size: ~50 lines (down from 106)

### Task 3.4: Refactor `upload_media_post_util()`
Mode hint: /code-monkey
Action: Simplify using extracted validation, upload helpers.

CLARIFICATION: The plan acknowledges that MediaFileHandler is already used internally via the adapter. The refactoring keeps the same underlying handler but makes the orchestration cleaner.

New structure:
```python
def upload_media_post_util():
    """Process media file upload."""
    try:
        from routes.utils_admin_upload import (
            validate_upload_requirements, extract_uploaded_files,
            prepare_media_record_data
        )
        from utils.route_helpers import build_multi_message_response, is_ajax_request
        from utils.media_core import MediaFileHandler, MediaFileConfig
        from flask_wtf.csrf import validate_csrf
        
        # CSRF validation (use Flask-WTF directly)
        try:
            validate_csrf(request.form.get('csrf_token'))
        except Exception as e:
            return handle_util_result({
                'success': False,
                'message': 'CSRF token validation failed.',
                'redirect': url_for('admin.upload_media')
            })
        
        # Validate requirements
        result = validate_upload_requirements(request, db.session)
        if not result['valid']:
            return handle_util_result({
                'success': False,
                'message': result['errors'][0],
                'redirect': url_for('admin.upload_media')
            })
        
        owner = result['owner']
        media_type = result['media_type']
        
        # Extract files
        valid_files = extract_uploaded_files(request)
        if not valid_files:
            return handle_util_result({
                'success': False,
                'message': 'Please select at least one file to upload.',
                'redirect': url_for('admin.upload_media',
                    owner_user_id=owner.id, media_type_id=media_type.id)
            })
        
        # Build MediaFileConfig from centralized config
        config = MediaFileConfig(
            upload_folder=current_app.config['MEDIA_UPLOAD_FOLDER'],
            allowed_extensions=current_app.config['MEDIA_ALLOWED_EXTENSIONS'],
            max_file_sizes_mb=current_app.config['MEDIA_MAX_FILE_SIZES_MB'],
            enable_thumbnails=current_app.config['MEDIA_ENABLE_THUMBNAILS'],
            enable_metadata_extraction=current_app.config['MEDIA_ENABLE_METADATA'],
            enable_imdb=current_app.config['MEDIA_ENABLE_IMDB'],
            enable_tvdb=current_app.config['MEDIA_ENABLE_TVDB'],
            enable_tmdb=current_app.config['MEDIA_ENABLE_TMDB']
        )
        
        # Process files using MediaFileHandler
        handler = MediaFileHandler(config)
        messages = []
        saved_count = 0
        
        for file in valid_files:
            result = handler.process_file(file, owner.id, media_type.code)
            
            if result.ok:
                try:
                    media_data = prepare_media_record_data(
                        result.data, owner, media_type, current_user
                    )
                    new_media = Media(**media_data)
                    db.session.add(new_media)
                    saved_count += 1
                    
                    # Log action
                    UserAction.log_action(
                        user_id=current_user.id,
                        action_type='admin_upload_media',
                        action_category='admin',
                        details={
                            'owner_user_id': owner.id,
                            'filename': result.data['filename_original']
                        },
                        ip_address=request.remote_addr,
                        user_agent=request.headers.get('User-Agent', ''),
                        target_type='media'
                    )
                except Exception as e:
                    logger.error(f"Database save failed: {str(e)}")
                    messages.append(('error', f"{file.filename}: Database save failed"))
            else:
                messages.append(('error', f"{file.filename}: {', '.join(result.errors)}"))
        
        # Commit
        if saved_count > 0:
            db.session.commit()
            messages.append(('success', f'Successfully uploaded {saved_count} file(s).'))
        
        # Determine redirect
        redirect_url = (url_for('admin.media') if saved_count > 0 and not any(m[0] == 'error' for m in messages)
                       else url_for('admin.upload_media',
                           owner_user_id=owner.id, media_type_id=media_type.id))
        
        return build_multi_message_response(messages, redirect_url)
        
    except Exception as e:
        logger.error(f"Error in upload_media_post_util: {str(e)}", exc_info=True)
        return handle_util_result({
            'success': False,
            'message': 'An unexpected error occurred during processing.',
            'redirect': url_for('admin.upload_media')
        })
```

Target size: ~100 lines (down from 211)

### Task 3.5: Refactor `select_owner_util()`
Mode hint: /code-monkey
Action: Simplify using extracted query builder and unified pagination.

Key changes:
- Use unified pagination function
- Use sanitize_redirect_url for security

New structure:
```python
def select_owner_util():
    """Display owner selection page with filters and pagination."""
    try:
        from utils.user_query_core import build_user_search_query, prepare_user_list_data
        from utils.media_query_core import paginate_media_query
        from utils.route_helpers import sanitize_redirect_url
        
        # Extract and sanitize parameters
        next_url = sanitize_redirect_url(
            request.args.get('next', '/admin/media/upload'),
            allowed_paths=['/admin/media/upload']
        )
        
        show_all = request.args.get('show_all', '').lower() in ('true', '1', 'on', 'yes')
        resellers_only = request.args.get('resellers_only', '').lower() in ('true', '1', 'on', 'yes')
        search_term = request.args.get('q', '').strip() or request.args.get('search', '').strip()
        
        # Build query
        query = build_user_search_query(
            db.session, search_term,
            active_only=not show_all,
            resellers_only=resellers_only
        )
        query = query.order_by(User.username.asc())
        
        # Unified pagination
        page = request.args.get('page', 1, type=int)
        page_result = paginate_media_query(query, page, per_page=20)
        
        # Prepare user data
        user_data = prepare_user_list_data(page_result['items'])
        
        return {
            'success': True,
            'template': 'admin/select_owner.html',
            'data': {
                'users': user_data,
                'pagination': page_result,
                'filters': {
                    'show_all': show_all,
                    'resellers_only': resellers_only,
                    'q': search_term
                },
                'next': next_url
            }
        }
    except Exception as e:
        logger.error(f"Error in select_owner: {str(e)}", exc_info=True)
        return {'success': False, 'error': 'Error loading owner selection', 'status_code': 500}
```

Target size: ~55 lines (down from 112)

### Task 3.6: Refactor `select_owner_search_util()`
Mode hint: /code-monkey
Action: Simplify AJAX owner search using unified pagination.

Key changes:
- Use unified pagination function
- Consistent with select_owner_util pagination

Target size: ~60 lines (down from 118)

## Phase 4: Template Compatibility and Testing

### Task 4.1: Verify Template Compatibility
Mode hint: /front-end
Action: Ensure all refactored functions maintain template data contracts.

CRITICAL: Templates expect specific data structures. Any changes must be verified.

Verification steps:
- Compare pagination dict structure in `templates/admin/media.html` with new pagination format
- Verify media list structure matches template expectations
- Test user list structure in `templates/admin/select_owner.html`
- Add presentation adapters if needed to maintain compatibility
- Document any template changes required

Templates to verify:
- `templates/admin/media.html`
- `templates/admin/media_edit.html`
- `templates/admin/select_owner.html`
- `templates/admin/upload_media.html`

### Task 4.2: Update imports in route files
Mode hint: /task-simple
Action: Add imports for new modules.

`routes/utils_admin_media.py` imports:
```python
from utils.media_query_core import (
    build_media_search_query, normalize_media_results,
    sort_media_results, paginate_media_query
)
from utils.media_associations_core import process_media_associations
from routes.utils_admin_forms import extract_search_params, extract_media_form_data
from utils.route_helpers import is_ajax_request
```

`routes/utils_admin_media_files.py` imports:
```python
from utils.user_query_core import build_user_search_query, prepare_user_list_data
from utils.media_query_core import paginate_media_query
from utils.media_core import MediaFileHandler, MediaFileConfig
from routes.utils_admin_upload import (
    validate_upload_requirements, extract_uploaded_files,
    prepare_media_record_data
)
from utils.route_helpers import (
    build_multi_message_response, sanitize_redirect_url
)
```

### Task 4.3: Create unit tests
Mode hint: /tester
Action: Create test files for new core modules using live PostgreSQL.

Test files to create:
- `tests/test_media_query_core.py`
  - Test query building with various filters
  - Test normalization edge cases
  - Test sorting with different fields
  - Test unified pagination with both query and list inputs
  - Test pagination edge cases (empty results, single page, etc.)
  - Use live PG test DB with baseline fixtures
- `tests/test_media_associations_core.py`
  - Test CSV parsing and deduplication
  - Test Unicode normalization (NFC)
  - Test entity creation vs lookup
  - Test association creation with transactions
  - Test error handling and rollback
  - Test CoreResult return format
  - Test concurrent access scenarios
- `tests/test_user_query_core.py`
  - Test user search query building
  - Test active/inactive filtering
  - Test reseller filtering
  - Test user data preparation
- `tests/test_route_helpers_extensions.py`
  - Test new helper functions (is_ajax_request, build_multi_message_response, sanitize_redirect_url)
  - Test integration with existing handle_util_result

Testing strategy:
- Use pytest with live PostgreSQL (not test DB per project standards)
- Create baseline test fixtures for Media, User, Genre, Director, Performer
- Test both happy paths and error conditions
- Verify transaction rollback behavior
- Test edge cases (empty results, null values, special characters)

## Phase 5: Extend to User Routes

### Task 5.1: Apply pattern to `routes/utils_user_media.py`
Mode hint: /code-monkey
Action: Refactor user media routes using same extracted modules.

Reusable components:
- `utils/media_query_core.py` functions
- Generic pagination and sorting
- `utils/route_helpers.py` response functions

Template compatibility:
- Add presentation adapters that maintain existing template input shapes
- Verify pagination dict structure matches template expectations
- Test thoroughly before deployment

## Success Metrics

File size reductions:
- `routes/utils_admin_media.py`: 702 → ~180 lines (74% reduction)
- `routes/utils_admin_media_files.py`: 551 → ~265 lines (52% reduction)
- Combined total: 1,253 → ~445 lines (64% reduction)

New core files created:
- `utils/media_query_core.py`: ~150 lines
- `utils/media_associations_core.py`: ~100 lines
- `utils/user_query_core.py`: ~70 lines
Total new core: ~320 lines

New/extended presentation files:
- `routes/utils_admin_forms.py`: ~80 lines
- `utils/route_helpers.py`: +~50 lines (extension)
- `routes/utils_admin_upload.py`: ~100 lines
Total new presentation: ~230 lines

Net impact:
- Original code: 1,253 lines
- Refactored code: 445 lines (orchestration) + 320 lines (core) + 230 lines (presentation) = 995 lines
- Net reduction: ~258 lines (21% overall reduction)
- Duplication eliminated: ~350 lines
- Code quality: significantly improved (testability, reusability, separation of concerns)

## Dependencies

Required existing modules:
- `utils/database.py` - db session
- `utils/media_core.py` - MediaFileHandler, CoreResult, existing sort helpers
- `models/models_media.py` - all media models
- `utils/imdb_core.py` - IMDb search (already uses BaseApiProvider)
- `utils/route_helpers.py` - existing response handling (will be extended minimally)
- `config.py` - centralized MEDIA_* configuration keys

## Risks and Mitigation

Risk: Breaking existing functionality
- Mitigation: Comprehensive unit tests for each extracted function against live PG
- Mitigation: Integration tests for refactored routes
- Mitigation: Manual QA of admin media pages
- Mitigation: Gradual rollout (one function at a time)

Risk: Template incompatibility
- Mitigation: CRITICAL - Verify template data contracts before and after refactoring
- Mitigation: Add presentation adapters to maintain template input shapes
- Mitigation: Test pagination dict structure matches template expectations
- Mitigation: Document any required template changes

Risk: Import circular dependencies
- Mitigation: Core modules have zero Flask imports
- Mitigation: Presentation layer imports from core, not vice versa
- Mitigation: Review import graph before implementation

Risk: Performance regression
- Mitigation: Benchmark query performance before/after
- Mitigation: Profile pagination logic
- Mitigation: Monitor DB round trip counts
- Mitigation: SQL-level pagination for large result sets

Risk: External API failures
- Mitigation: Graceful degradation - UI renders DB results with warning if provider fails
- Mitigation: Existing imdb_core already handles this well
- Mitigation: Rate limiting awareness in provider calls

## Implementation Order

Priority 1 (High Impact - Eliminates Most Duplication):
1) Phase 1, Task 1.2: Simplified association processor (~200 lines eliminated)
2) Phase 1, Task 1.3: User query builder (~80 lines eliminated)
3) Phase 2, Task 2.2: Minimal route_helpers extensions (single source of truth)

Priority 2 (Medium Impact - Core Refactoring):
4) Phase 1, Task 1.1: Media query/sort/pagination extraction (unified approach)
5) Phase 2, Task 2.1: Form extraction helpers
6) Phase 2, Task 2.3: Upload validation helpers

Priority 3 (Refactor utils_admin_media.py):
7) Phase 3, Task 3.2: Refactor `media_edit_util()` (uses simplified association processor)
8) Phase 3, Task 3.1: Refactor `media_management_util()` (uses query core)

Priority 4 (Refactor utils_admin_media_files.py):
9) Phase 3, Task 3.4: Refactor `upload_media_post_util()`
10) Phase 3, Task 3.5: Refactor `select_owner_util()` (unified pagination)
11) Phase 3, Task 3.6: Refactor `select_owner_search_util()` (unified pagination)
12) Phase 3, Task 3.3: Refactor `upload_media_get_util()`

Priority 5 (Quality Assurance):
13) Phase 4, Task 4.1: CRITICAL - Verify template compatibility
14) Phase 4, Task 4.2: Update imports
15) Phase 4, Task 4.3: Create comprehensive tests
16) Phase 5: Extend pattern to user routes

## Acceptance Criteria

Per-endpoint validation (applies to all refactored functions):
- Same query filters/total counts as before
- Same visible sort order for identical inputs
- Same flashes/redirects/AJAX JSON contract
- Equivalent logging side effects
- No net increase in DB round trips in common cases
- CRITICAL: Template renders without errors or missing data
- Pagination controls work correctly

Data integrity:
- Association creation: no duplicates under concurrent access
- Transaction boundaries: proper rollback on partial failures
- File uploads: atomic writes, cleanup on error
- Path security: no traversal vulnerabilities

Performance benchmarks:
- Media list query: <200ms for 1000 records
- Owner selection: <100ms for 500 users
- Association processing: <50ms for 20 entities
- Upload processing: acceptable file sizes per config

Template compatibility:
- All existing templates render without modification
- Pagination dict structure matches template expectations
- All template variables present with correct types
- No breaking changes to template data contracts

## Notes for Implementation

- All new functions must include docstrings with type hints
- Follow naming convention: `{domain}_{specific}`
- Add model/date comments: `# Created by [model] | yyyy-mm-dd`
- Preserve all existing logging (convert Flask logger to Python logging in core)
- Maintain backward compatibility during rollout
- No changes to database schema
- CRITICAL: No changes to templates initially (add adapters if needed)
- Use CoreResult schema consistently across core modules
- Centralize configuration in `config.py` (MEDIA_* keys)
- Use existing sort helpers from `utils/media_core.py` (don't duplicate)
- Unified pagination function handles both SQL and Python pagination
- Minimal additions to `utils/route_helpers.py` (complement, don't replace)
- Flask-WTF provides CSRF validation - use it directly, no need to wrap
