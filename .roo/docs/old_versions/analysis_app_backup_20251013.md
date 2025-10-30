# MediaShare Application — Technical Overview

MediaShare Flask application: architecture, config, data model, security, and core routes.

## Application Purpose
MediaShare is a Flask-based platform for uploading, organizing, and streaming media with role-based access across admins, resellers, and end users. It combines a hierarchical reseller model (resellers manage customer accounts and branding), a credit-based consumption system, secure authentication (CSRF, hashed passwords, lockout), and comprehensive audit logging, with modular domains (media, payments, support) implemented via Blueprints and SQLAlchemy for straightforward expansion.

## Architecture Overview
- Framework: Flask with Blueprints, Jinja2 templating, SQLAlchemy ORM, Flask-Login, Flask-WTF CSRF, Flask-Mail
- Entrypoint: `app.py`
- Application factory: `create_app()`
- Blueprints:
    - Auth: `routes/auth.py`
    - Admin: `routes/admin.py`
    - User: `routes/user.py`
    - Reseller: `routes/reseller.py`
    - Media: `routes/media.py`
- DB instance (single source): `utils/database.py`, `db = SQLAlchemy()`
- Config classes: `config.py`
- Models (core user management + system): `models/models_user.py`

## Core Separation Architecture
MediaShare implements a clean separation between business logic and presentation layers through core modules:
- Core Layer: Stateless, role-agnostic business logic in `utils/*_core.py` modules
- Presentation Layer: Flask-aware route handlers with user context and logging
- API Layer: Unified external API interface with provider abstraction

### Core Modules
- `utils/imdb_core.py`: Consolidated IMDb API operations (search, details, rating, import)
- `utils/api_core.py`: Base API provider interface with IMDb active, TMDB/TVDB preserved
- `utils/dashboard_core.py`: Platform metrics and analytics without Flask dependencies
- `utils/media_core.py`: Media processing, validation, and file operations
- `utils/users_core.py`: User management business logic
- `utils/genres_core.py`: Genre system operations
- `utils/payments_core.py`: Payment processing logic

### Presentation Layers
- Admin: `routes/utils_admin_*.py` - Admin-specific operations with current_user logging
- User: `routes/utils_user_*.py` - User-facing utilities with appropriate access controls
- Shared: Core modules accessible by both admin and user layers

### Utility Infrastructure
- `utils/route_helpers.py`: Standardized response handling for route utilities
- `utils/deprecation.py`: Deprecation shim system for backward compatibility
- `utils/auth.py`: Authentication utilities
- `utils/auth_admin.py`: Admin-specific authentication helpers
- `utils/email.py`: Email functionality
- `utils/forms.py`: Form handling utilities
- `utils/payments.py`: Payment integration helpers

## Application Lifecycle, App Factory
- Global app symbol, factory:
    - Flask app symbol: `app = Flask(__name__)`
    - Factory to configure app, extensions, and routes: `def create_app()`
- Extensions initialization within factory:
    - SQLAlchemy: `db.init_app(app)`
    - Flask-Login: `login_manager.init_app(app)`
    - CSRF: `csrf.init_app(app)`
    - Mail: `mail.init_app(app)`
- Login config:
    - `login_manager.login_view = 'auth.login'`
    - `login_manager.login_message = 'Please log in to access this page.'`
- User loader (Flask-Login):
    - Declaration: `def load_user()`
    - Implementation uses session.get with int cast and error handling: `return db.session.get(User, int(user_id))`
- DB bootstrapping:
    - On app context startup: `db.create_all()`
    - Error handling for database initialization failures
- Error handlers:
    - 404: `@app.errorhandler(404)` renders `templates/errors/404.html`
    - 500: `@app.errorhandler(500)` renders `templates/errors/500.html` with session rollback
- Specialized home routes:
    - Home (referral/admin redirect logic): `@app.route('/')`
    - Home-register: `@app.route('/register')`
    - Home-admin landing: `@app.route('/admin')`
    - Referred landing: `@app.route('/referred')`
    - Static policy pages: `@app.route('/privacy-policy')`, `@app.route('/terms-of-service')`
- Blueprints registration:
    - Auth: `app.register_blueprint(auth_bp, url_prefix='/auth')`
    - Admin: `app.register_blueprint(admin_bp, url_prefix='/admin')`
    - Reseller: `app.register_blueprint(reseller_bp, url_prefix='/reseller')`
    - User: `app.register_blueprint(user_bp, url_prefix='/user')`
    - Media: `app.register_blueprint(media_bp, url_prefix='/media')`
- Development server guard:
    - `if __name__ == '__main__':`
    - Environment-based configuration (host, port, debug mode)
    - Comprehensive startup logging and error handling

## Config
- Base and environments: `config.py`
    - Base: `class Config`
    - Development: `class DevelopmentConfig`
    - Production: `class ProductionConfig`
    - Testing: `class TestingConfig`
    - Mapping: `config_by_name = {...}`
- DB URI resolution:
    - Uses `DATABASE_URL` when present; otherwise constructs PostgreSQL URI from `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` into `SQLALCHEMY_DATABASE_URI`
- SQLAlchemy engine options (pre-ping, pool recycle, optional echo): `SQLALCHEMY_ENGINE_OPTIONS`
- Email settings via environment variables: `MAIL_*`
- Testing config disables CSRF: `WTF_CSRF_ENABLED = False`

## DB and ORM
- DB instance and init helper:
    - Instance: `db = SQLAlchemy()` in `utils/database.py`
    - Helper: `def init_db(app)`
- Core models (user system): `models/models_user.py`
- User types/roles:
    - Declaration: `class UserType`
    - Notable columns: `code`, `name`, limits and flags; relationship `users`
- User (hierarchical):
    - Declaration: `class User`
    - Notable columns: `username`, `email`, `pw_hashed`, `users_type_id`, `parent_id`, `credit_balance`, verification flags, auth lockout fields (`failed_login_attempts`, `is_locked_out`, `lockout_until`)
    - Relationships: `user_type`, `parent` (self-referential), `children`, `sessions`, `devices`, `notifications`, `actions`
    - Hierarchy helpers: `def get_hierarchy_level()`, `def get_all_descendants()`, `def can_manage_user()`
    - Token helpers: `def get_reset_token()`, `@staticmethod def verify_reset_token()`
- Session tracking:
    - Declaration: `class UserSession`
    - Indexing for token and expiry; `is_expired`, `update_activity`
- Device tracking:
    - Declaration: `class UserDevice`
- Notifications:
    - Declaration: `class Notification`
- Audit trail:
    - Declaration: `class UserAction`
    - Logger utility: `@classmethod def log_action()`
- Additional domain models (referenced in admin):
    - Media: `models/models_media.py`
    - Payments/Subscriptions: `models/models_payment.py`
    - Support tickets: `models/models_support.py`
    - Reseller: `models/models_reseller.py`
    - Interactions: `models/models_interaction.py`
    - Referrals: `models/models_referral.py`

## Authentication, Authorization, Security
- Blueprint: `routes/auth.py`
- Login route: `def login()`
    - CSRF validation for POST when enabled: `validate_csrf(...)`
    - Validations (email format, required fields): `validation_errors.append(...)`
    - Password hashing check: `check_password_hash(user.pw_hashed, password)`
    - Account lockout (>=5 failed attempts; 15 mins): `user.failed_login_attempts += 1`, `user.is_locked_out = True`
    - Session login: `login_user(user)`
    - Security/audit logging: `UserAction.log_action(...)`
- Registration route: `def register()`
    - Server-side validations (username/email/password): see validation block `routes/auth.py`
    - Default user type ensured/created (`basic`): `basic_user_type = UserType.query.filter_by(code='basic').first()`
    - Secure password hashing: `generate_password_hash(password)`
    - User creation with safe defaults: `new_user = User(...)`
    - Auto-login and verification email (skipped in TESTING): `login_user(new_user)`
- Logout: `def logout()`
- Forgot/reset password: `def forgot_password()`, `def reset_password()`
- Email verification with testing override: `def verify_email()`
- Authorization:
    - Admin access guard: `def admin_required(f)` in `utils/auth_admin.py`
    - Checks `current_user.user_type.code == 'admin'`
- CSRF:
    - Global protection enabled via CSRFProtect; per-route POST validations: `validate_csrf(...)`
- Passwords:
    - Stored as `pw_hashed` (Werkzeug) — never plaintext
- Sessions:
    - Flask-Login managed; user_loader uses safe int casting and try/except: `def load_user()`

## Feature Areas, Blueprints

### Admin Blueprint Architecture
- Main file: `routes/admin.py` - implements clean separation-of-concerns pattern
- Business logic delegation: All admin functionality separated into specialized utility files
- Route helper integration: Uses standardized `utils/route_helpers.py` functions for consistent response handling
- Utility files by domain:
    - `routes/utils_admin_dashboard.py` - Platform metrics and dashboard data
    - `routes/utils_admin_users.py` - User management CRUD operations
    - `routes/utils_admin_media.py` - Media management, upload, and metadata operations
    - `routes/utils_admin_genres.py` - Global genre system management
    - `routes/utils_admin_payments.py` - Financial metrics and transaction history
    - `routes/utils_admin_support.py` - Support ticket metrics and management
    - `routes/utils_admin_settings.py` - Platform configuration management
    - `routes/utils_admin_api.py` - External API integration (IMDb operations)
    - `routes/utils_admin_resellers.py` - Partner management system

### Admin Routes Implementation
- Dashboard: `/admin/` - comprehensive platform metrics via `dashboard_util()`
- User Management:
    - `/admin/users` - list users with filtering via `view_users_util()`
    - `/admin/users/add` - create users via `add_user_util()`
    - `/admin/edit_user/<int:user_id>` - modify users via `edit_user_util()`
    - `/admin/user/<int:user_id>/delete` - delete users via `delete_user_util()`
- Media Management:
    - `/admin/media` - browse/search media via `media_management_util()`
    - `/admin/media_edit/<int:media_id>` - edit media metadata via `media_edit_util()`
    - `/admin/media/upload` - upload form and processing via `upload_media_get_util()` and `upload_media_post_util()`
    - `/admin/media/select-owner` - owner selection interface via `select_owner_util()`
    - `/admin/media/select-owner/search` - AJAX owner search via `select_owner_search_util()`
- External API Integration:
    - `/admin/media/<int:media_id>/pull-imdb` - IMDb data retrieval via `imdb_pull_admin()`
    - `/admin/media/search-imdb` - IMDb search via `imdb_search_admin()`
    - `/admin/media/import-imdb` - IMDb import via `imdb_import_admin()`
    - `/admin/media/<int:media_id>/rating-imdb` - IMDb rating via `imdb_rating_admin()`
- System Management:
    - `/admin/genres` - genre management via `genre_management_util()`
    - `/admin/payments` - payment metrics via `payments_management_util()`
    - `/admin/support` - support ticket management via `support_management_util()`
    - `/admin/settings` - platform configuration via `settings_util()`
    - `/admin/resellers` - reseller management via `reseller_management_util()`

### Route Helper Functions
- `handle_util_result(result, success_redirect=None)` - standard utility result processing with template rendering or redirects
- `handle_simple_util_result(result, template_name, success_redirect=None)` - simplified template rendering for read-only operations
- `handle_delete_result(success, message, message_type, redirect_url)` - specialized delete operation handling with flash messages

### User Blueprint
- Main file: `routes/user.py`
- Utility files:
    - `routes/utils_user_dashboard.py` - User dashboard data
    - `routes/utils_user_profile.py` - Profile management
    - `routes/utils_user_media.py` - Media browsing and playback
    - `routes/utils_user_imdb.py` - IMDb search for users
- Routes:
    - Dashboard: `def dashboard()` - user metrics and activity
    - Profile edit with form + audit log: `def profile()`
    - Media/favorites/history/subscriptions/credits/support placeholders

### Reseller Blueprint
- Main file: `routes/reseller.py`
- Routes (placeholders):
    - Dashboard: `def dashboard()`
    - Customers: `def customers()`
    - Earnings: `def earnings()`
    - Branding: `def branding()`
    - Settings: `def settings()`

### Media Blueprint
- Main file: `routes/media.py`
- Routes:
    - Public media list placeholder: `def list_media()`

## Templates, Static
- Layout and shared UI in `templates/` with Jinja2; routes render:
    - Home pages: `templates/home.html` (variants: default/register/referred), `templates/home_admin.html`
    - Auth: `templates/auth/*.html` (login, register, forgot_password, reset_password)
    - Admin: `templates/admin/*.html` (dashboard, users, media, media_edit, media_upload, select_owner, genres, payments, support, settings, resellers)
    - User: `templates/user/*.html` (dashboard, profile, media)
    - Reseller: `templates/reseller/*.html` (dashboard, customers, earnings, branding, settings)
    - Media: `templates/media/media.html`
    - Errors: `templates/errors/{404,500}.html`
    - Policy pages: `templates/privacy_policy.html`, `templates/terms_of_service.html`
- Static assets under `static/`:
    - CSS: `static/css/main.css`
    - JavaScript: `static/js/` (main.js, auth.js, dashboard.js, media_player.js, select_owner.js, tvdb.js)
    - Images: `static/images/` (logo.png, favicon.ico)
    - Uploads: `static/uploads/media/`, `static/uploads/reseller_assets/`, `static/uploads/thumbnails/`

## Observability, Audit
- Consistent action logging:
    - Utility: `UserAction.log_action()`
    - Widespread usage in auth and profile flows for security and analytics
- Debug logging present in auth and admin flows for traceability

## Operational Notes
- DB setup on boot via `create_all()` — convenient for dev; production should rely on migrations
- Default DB target is PostgreSQL (via env or defaults) per `config.py`
- CSRF disabled in testing config only
- Email uses Flask-Mail with environment-provided SMTP settings
- Development server configuration via environment variables (FLASK_HOST, FLASK_PORT, FLASK_DEBUG)

## APIs and External Integrations
- IMDb API: `@\.roo\docs\api-imdb-docs.md` - Movie and TV show metadata retrieval
- Payment APIs: [Future - Stripe/PayPal integration]
- Email Services: [Future - SendGrid/Mailgun documentation]

## Core Modules Documentation
Detailed documentation for the core separation architecture:
- `@\.roo\docs\core_modules\imdb_core.md` - Comprehensive IMDb functionality
- `@\.roo\docs\core_modules\api_core.md` - Unified API provider interface
- `@\.roo\docs\core_modules\dashboard_core.md` - Platform metrics and analytics
- `@\.roo\docs\core_modules\media_core.md` - Media processing and file operations

## Primary Code References (Quick Jump)
- App factory and runtime:
    - `def create_app()`, `def load_user()`, `app.py`
- Config:
    - `class Config`, `class DevelopmentConfig`, `class ProductionConfig`, `class TestingConfig`
- DB:
    - `db = SQLAlchemy()`, `def init_db()`
- Models:
    - `class UserType`, `class User`, `class UserSession`, `class UserDevice`, `class Notification`, `class UserAction`
- Auth routes:
    - `def login()`, `def register()`, `def logout()`, `def forgot_password()`, `def reset_password()`, `def verify_email()`
- Admin routes and utilities:
    - Main blueprint: `routes/admin.py` - route definitions with utility delegation
    - Dashboard: `routes/utils_admin_dashboard.py` - `dashboard_util()`
    - User management: `routes/utils_admin_users.py` - `view_users_util()`, `add_user_util()`, `edit_user_util()`, `delete_user_util()`
    - Media management: `routes/utils_admin_media.py` - `media_management_util()`, `upload_media_get_util()`, `upload_media_post_util()`, `select_owner_util()`
    - Genre system: `routes/utils_admin_genres.py` - `genre_management_util()`
    - External APIs: `routes/utils_admin_api.py` - `imdb_pull_admin()`, `imdb_search_admin()`, `imdb_import_admin()`, `imdb_rating_admin()`
    - System management: `routes/utils_admin_settings.py`, `routes/utils_admin_payments.py`, `routes/utils_admin_support.py`, `routes/utils_admin_resellers.py`
- Core modules:
    - IMDb: `utils/imdb_core.py` - `imdb_search_core()`, `imdb_details_fetch_core()`, `imdb_rating_core()`, `imdb_import_core()`
    - API: `utils/api_core.py` - `get_api_provider()`, `get_active_providers()`, `BaseApiProvider`, `ImdbApiProvider`
    - Dashboard: `utils/dashboard_core.py` - platform metrics functions
    - Media: `utils/media_core.py` - media processing functions
    - Users: `utils/users_core.py` - user management business logic
    - Genres: `utils/genres_core.py` - genre operations
    - Payments: `utils/payments_core.py` - payment processing
- Route helpers:
    - `utils/route_helpers.py` - `handle_util_result()`, `handle_simple_util_result()`, `handle_delete_result()`
- User routes:
    - `def profile()`, `def dashboard()`
    - Utilities: `routes/utils_user_dashboard.py`, `routes/utils_user_profile.py`, `routes/utils_user_media.py`, `routes/utils_user_imdb.py`
- Reseller routes:
    - `def dashboard()`, `def customers()`, `def earnings()`, `def branding()`, `def settings()`
- Media routes:
    - `def list_media()`

## Media Handling and Storage
- Storage base path:
    - Upload base directory is read from app config ("UPLOAD_FOLDER"); defaults to "static/uploads/media". See config access in `utils/media_core.py`
    - Per-user, per-type directory structure is created as "base_path/media_type_code/user_id" by directory creation functions
- Allowed types and sizes:
    - Allowed extensions by media type are defined in `utils/media_core.py`
    - Maximum file sizes (MB) by media type are defined in `utils/media_core.py`
    - Extension check helper: validation functions in media_core
    - Validation pipeline (presence, extension, size): validation functions
- Upload workflow (server-side):
    - Orchestrator for multi-file uploads: processing functions in `utils/media_core.py`
    - Steps per file:
        - Validate: file validation
        - Save to disk and compute metadata: SHA-256 hashing, MIME type detection
        - Optional thumbnail generation (images): thumbnail creation
        - Extract basic metadata (images, EXIF if present): metadata extraction
    - Returns (per successful file): original/stored filenames, project-relative file_path, size bytes/MB, file_hash, mime_type, optional thumbnail_path, metadata dict
    - Admin-facing upload UI and POST handler leverage these utils; see `routes/admin.py` and `routes/utils_admin_media.py`
- Thumbnails:
    - Currently generated only for images (Pillow required). Non-image (video/audio) thumbnails are not implemented
    - Output directory: "static/uploads/thumbnails/media_type_code/user_id"
    - Thumbnails are saved as optimized JPEGs (max 300×300, aspect preserved)
- Cleanup:
    - Disk cleanup helper to remove main file and optional thumbnail: deletion functions in media_core
- Public media routes:
    - Media blueprint definition: see `routes/media.py`
    - Route: "/" → list all media (placeholder): `def list_media()`. Template: `templates/media/media.html`
- Notes and TODOs:
    - Video/audio thumbnailing would require ffmpeg or similar (not yet integrated)
    - Allowed extensions and size limits are currently code-defined; consider sourcing from DB model (eg, "MediaType") in `models/models_media.py` to make runtime-configurable

## Admin Media Upload & Owner Selection Flow
- Pages and endpoints:
    - Upload UI: `/admin/media/upload` GET/POST — handled via `upload_media_get_util()` and `upload_media_post_util()`
    - Owner selection: `/admin/media/select-owner` — dynamic user selection interface via `select_owner_util()`
    - Owner search: `/admin/media/select-owner/search` — AJAX endpoint with pagination via `select_owner_search_util()`
    - Media management: `/admin/media` — browse/search interface via `media_management_util()`
    - Media editing: `/admin/media_edit/<int:media_id>` — metadata editing via `media_edit_util()`
- Templates and assets:
    - Upload interface: `templates/admin/media_upload.html`
    - Owner selection: `templates/admin/select_owner.html` with `static/js/select_owner.js`
    - Media management: `templates/admin/media.html`
    - Media editing: `templates/admin/media_edit.html`
- Search and filtering capabilities:
    - Supports `q` or `search` query parameters
    - Advanced filters: `resellers_only`, `active_only`, `limit` (backend enforced limits)
    - Pagination support with configurable page sizes
- Owner selection workflow:
    - Dynamic user search with real-time filtering
    - Callback mechanism via `next` parameter for workflow integration
    - JavaScript helpers for seamless form integration
- Upload processing architecture:
    - File validation: `utils/media_core.py` - validation functions
    - File storage: `utils/media_core.py` - storage functions
    - Thumbnail generation: `utils/media_core.py` - thumbnail functions
    - Metadata extraction: `utils/media_core.py` - metadata functions
    - Database persistence: `models/models_media.py`
    - Audit trail: Automatic action logging for all admin operations

## External API Integrations

### Core Separation Architecture
MediaShare implements a clean three-layer API architecture:
- Core Layer: Stateless business logic in `utils/*_core.py` modules
- Provider Layer: Unified API interface in `utils/api_core.py` with pluggable providers
- Presentation Layer: Role-specific wrappers with Flask context and user logging

### API Provider System
The `utils/api_core.py` module provides a unified interface for all external APIs:
- BaseApiProvider: Abstract interface defining search, details, rating, and import operations
- ImdbApiProvider: Active provider using consolidated `utils/imdb_core.py` functionality
- TmdbApiProvider: Preserved structure, disabled but ready for future reactivation
- TvdbApiProvider: Preserved structure, disabled but ready for future reactivation

### Import Examples
```python
# Unified API provider interface
from utils.api_core import get_api_provider, get_active_providers
provider = get_api_provider('imdb')
results = provider.search('movie title')

# Core functions (stateless, role-agnostic)
from utils.imdb_core import imdb_search_core, imdb_details_fetch_core
from utils.media_core import merge_and_deduplicate_results

# Admin presentation layer (Flask-aware)
from routes.utils_admin_api import imdb_pull_admin, imdb_search_admin

# User presentation layer (Flask-aware with access controls)
from routes.utils_user_imdb import search_imdb_for_user
```

### Active IMDb Integration
- Core Module: `utils/imdb_core.py` - Comprehensive IMDb functionality
    - `imdb_search_core()`: Search titles with validation and pagination
    - `imdb_details_fetch_core()`: Fetch detailed metadata for titles
    - `imdb_rating_core()`: Retrieve IMDb ratings via scraping
    - `imdb_import_core()`: Prepare data for system import
- Admin Routes: `/admin/media/<int:media_id>/pull-imdb` POST
- User Access: Available through user utilities with appropriate limitations
- API Provider: RapidAPI for IMDb data retrieval with fallback scraping

### Preserved API Structures
TMDB and TVDB APIs maintain their interface structure but are currently disabled:
- TMDB: Preserved in `utils/api_core.py` TmdbApiProvider for future reactivation
- TVDB: Preserved in `utils/api_core.py` TvdbApiProvider for future reactivation
- Reactivation: Simply set `enabled=True` and implement provider methods

### Genre Management System
- Route: `/admin/genres` GET
- Implementation: `routes/utils_admin_genres.py` - `genre_management_util()`
- Features: Global genre system management with media count metrics
- Database: Centralized genre taxonomy in `models/models_media.py`

## Testing Infrastructure
- Test directory: `tests/`
- Configuration: `tests/conftest.py` - pytest fixtures and configuration
- Test modules:
    - `tests/test_auth.py` - Authentication flow testing
    - `tests/test_e2e_auth.py` - End-to-end authentication testing
    - `tests/test_email.py` - Email functionality testing
    - `tests/test_models.py` - Database model testing
    - `tests/test_user.py` - User operations testing
- Testing approach: Uses pytest framework with Flask test client

## Development Tools and Scripts
- Admin setup: `admin_setup.py` - Create admin users
- Database scripts: Various `check_*.py` and `update_*.py` scripts for database operations
- Analysis tools: `analyze_redundant_functions.py` - Code quality analysis
- Schema tools: `generate_schema_documentation.py`, `get_db_schema.py` - Database documentation
- Population scripts: `populate_media_final.py`, `populate_sample_media.py` - Test data generation
- Testing scripts: `test_*.py` - Various testing utilities

## Project Documentation Structure
- Main docs: `.roo/docs/`
- Analysis: `agents.md` (this file)
- Database: `database_schema.md`, `pgdb_changes.md`
- APIs: `api-imdb-docs.md`
- Core modules: `core_modules/` directory
- Plans: `plan_*.md` files for project planning
- Old versions: `old_versions/` for backups
- Completed plans: `plans_completed/` for archived plans