# Code Mode - Non-Obvious Patterns

This file provides guidance to agents when working with code in this repository.

## Core vs Presentation Separation (MANDATORY)
- `utils/*_core.py` - stateless business logic (no Flask context)
- `routes/utils_*_*.py` - Flask-aware presentation utilities
- Never mix Flask imports into `*_core.py` files - this separation is architectural, not optional

## Route Helpers Pattern (REQUIRED)
- `utils/route_helpers.py` provides standardized response handling
- Always use `handle_util_result()`, `handle_simple_util_result()`, or `handle_delete_result()`
- Do not create custom response handling - these functions handle success/error states, flash messages, and redirects

## Media File Processing Pipeline
- Legacy adapters in `utils/media.py` are deprecated - prefer direct handler usage from `utils/media_core.py`
- Routes must translate CoreResult via `utils/route_helpers.py`
- Atomic writes: write to .tmp then rename; cleanup on error
- Idempotent deletes using Path.unlink(missing_ok=True)

## API Provider Framework
- `utils/api_provider_core.py` contains centralized `BaseApiProvider` class
- New API providers configured in `utils/api_provider_descriptors.py` by adding `DESCRIPTOR` dictionary
- Do not create separate utility files for each new API - use descriptor-based approach
- `TokenCache` class handles automatic token refresh and caching

## Naming Convention (NON-STANDARD)
- Pattern: `{domain}_{specific}` not `{specific}_{domain}`
- Examples: `utils_admin_dashboard.py` not `admin_dashboard_utils.py`

## Code Standards
- All functions/classes MUST include: `# [Created-or-Modified] by [model] | yyyy-mm-dd`
- Templates use `jinja-html` language mode (not standard html)