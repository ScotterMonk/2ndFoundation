from flask import Blueprint, render_template, request, jsonify, url_for, flash, redirect, current_app
from flask_login import login_required
import time

# Note: TVDB integration temporarily disabled; do not re-add imports from utils.utils_tvdb during plan 280925_api_cleanup.

# Import authentication and route utilities
from utils.auth_admin import admin_required
from utils.route_helpers import handle_util_result, handle_simple_util_result, handle_delete_result

# Import utility functions for admin functionality - FIXED: Moved to top to resolve import timing issue
from .utils_admin_dashboard import dashboard_util
from .utils_admin_users import view_users_util, delete_user_util, add_user_util, edit_user_util
from .utils_admin_genres import genre_management_util, genre_add_util
from .utils_admin_settings import settings_util
from .utils_admin_payments import payments_management_util
from .utils_admin_support import support_management_util
from .utils_admin_media import (
    media_management_util, media_edit_util,
    upload_media_get_util, upload_media_post_util, select_owner_util, select_owner_search_util
)
from routes.utils_admin_api import imdb_pull_admin, imdb_import_admin, imdb_rating_admin, imdb_search_admin, imdb_search_results_admin

"""
ADMIN BLUEPRINT ARCHITECTURE

This file serves as the main admin blueprint for the MediaShare Flask application,
providing routes for administrative functionality with a separation-of-concerns approach.

ARCHITECTURE OVERVIEW:
The admin routes follow a layered architecture:
- Core Layer: Stateless business logic in utils/ (genres_core.py, media_core.py, etc.)
- Presentation Layer: Flask-aware admin utilities in routes/ that delegate to core modules
- Routes Layer: This file handles HTTP requests and responses using admin utilities

UTILITY FILES ORGANIZATION:
All admin business logic is separated into utility files in the routes/ directory.
Each utility file handles admin-specific presentation logic and delegates to core modules.
Functions return standardized response dictionaries for consistent route handling.

ADMIN UTILITY FILES BY DOMAIN:

utils_admin_dashboard.py - Dashboard & Analytics
    - dashboard_util(): Platform metrics using dashboard_core.py

admin_utils_users.py - User Management
    - view_users_util(): List users with filtering/pagination using users_core.py
    - add_user_util(): Create users with validation using users_core.py
    - edit_user_util(): Modify user profiles using users_core.py
    - delete_user_util(): Remove users using users_core.py

utils_admin_media.py - Media Management
    - media_management_util(): Browse/search media using media_core.py + imdb_core.py
    - media_edit_util(): Edit metadata using media_core.py
    - upload_media_get_util(): Upload form using media_core.py
    - upload_media_post_util(): Process uploads using media_core.py
    - select_owner_util(): Owner selection interface
    - select_owner_search_util(): AJAX owner search

utils_admin_genres.py - Genre Management
    - genre_management_util(): Global genre system using genres_core.py

admin_utils_payments.py - Financial Management
    - payments_management_util(): Payment metrics using payments_core.py

admin_utils_support.py - Support System
    - support_management_util(): Support tickets using support models

admin_utils_settings.py - System Configuration
    - settings_util(): Platform configuration

utils_admin_api.py - IMDb/TMDB/TVDB Integration
    - imdb_pull_admin(): Fetch IMDb data using imdb_core.py
    - imdb_search_admin(): Search IMDb using imdb_core.py
    - imdb_import_admin(): Import IMDb metadata using imdb_core.py
    - imdb_rating_admin(): Update IMDb ratings using imdb_core.py

CORE MODULES (Used by Admin Utilities):
- genres_core.py: Genre CRUD and search operations
- media_core.py: Media file handling, search, and deduplication
- users_core.py: User profile and validation operations
- payments_core.py: Payment processing logic
- dashboard_core.py: Metrics and analytics aggregation
- imdb_core.py: IMDb API operations (RapidAPI integration)
- api_core.py: Base API patterns for future TMDB/TVDB reactivation

HOW TO USE:
1. Import required utility functions at top of this file (FIXED: No longer at bottom)
2. Create route function that calls utility with parameters
3. Handle returned dictionary for template rendering or redirects
4. All utilities follow consistent return format: {'success': bool, 'data': dict, ...}

FINDING THE RIGHT UTILITY:
- User operations -> admin_utils_users.py (uses users_core.py)
- Media/content -> utils_admin_media.py (uses media_core.py)
- External APIs -> utils_admin_api.py (uses imdb_core.py)
- Financial data -> admin_utils_payments.py (uses payments_core.py)
- System config -> admin_utils_settings.py
- Customer service -> admin_utils_support.py
- Analytics -> utils_admin_dashboard.py (uses dashboard_core.py)
"""

# Define blueprint for admin
admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """
    Display the admin dashboard with comprehensive metrics and data.
    """
    template_data = dashboard_util()
    return render_template('admin/dashboard.html', **template_data)

# User management routes using utility functions
@admin_bp.route('/users')
@login_required
@admin_required
def view_users():
    """List all users for admin management."""
    return handle_simple_util_result(view_users_util(), 'admin/users.html')

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user (POST only to prevent accidental deletion)."""
    success, message, message_type = delete_user_util(user_id)
    return handle_delete_result(success, message, message_type, url_for('admin.view_users'))

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """Add a new user to the system."""
    return handle_util_result(add_user_util())

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit user profiles with enhanced security checks."""
    return handle_util_result(edit_user_util(user_id), url_for('admin.view_users'))

# Genre management routes using utility functions
@admin_bp.route('/genres', methods=['GET'])
@login_required
@admin_required
def genre_management():
    """Manage global genres."""
    return handle_util_result(genre_management_util())

@admin_bp.route('/genres/add', methods=['POST'])
@login_required
@admin_required
def genre_add():
    """Add a new genre via JSON API."""
    result = genre_add_util()
    if result.get('success'):
        return jsonify(result)
    else:
        return jsonify(result), result.get('status_code', 500)

# Settings management routes using utility functions
@admin_bp.route('/settings')
@login_required
@admin_required
def settings():
    """Admin settings management page."""
    return handle_simple_util_result(settings_util(), 'admin/settings.html')

# Payment management routes using utility functions
@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    """Payment Management: metrics + search + listing."""
    return handle_simple_util_result(payments_management_util(), 'admin/payments.html')

# Support management routes using utility functions
@admin_bp.route('/support')
@login_required
@admin_required
def support():
    """Support Management: metrics and recent tickets."""
    return handle_simple_util_result(support_management_util(), 'admin/support.html')

# Media management routes using utility functions
@admin_bp.route('/media')
@login_required
@admin_required
def media():
    """Manage media items with metrics, search, and sorting."""
    return handle_util_result(media_management_util())

@admin_bp.route('/media_edit/<int:media_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def media_edit(media_id):
    """Edit media items."""
    return handle_util_result(media_edit_util(media_id), url_for('admin.media'))

@admin_bp.route('/media/upload', methods=['GET'])
@login_required
@admin_required
def upload_media():
    """Display the media upload form."""
    return handle_util_result(upload_media_get_util())

@admin_bp.route('/media/upload', methods=['POST'])
@login_required
@admin_required
def upload_media_post():
    """Process media upload form submission."""
    return handle_util_result(upload_media_post_util())

@admin_bp.route('/media/select-owner', methods=['GET'])
@login_required
@admin_required
def select_owner():
    """Display the owner selection page with filtering and pagination."""
    return handle_util_result(select_owner_util(), url_for('admin.media'))

@admin_bp.route('/media/select-owner/search', methods=['GET'])
@login_required
@admin_required
def select_owner_search():
    """AJAX endpoint for owner selection with pagination support."""
    result = select_owner_search_util()
    if result['success']:
        return jsonify(result['json_response'])
    else:
        return jsonify(result['json_response']), result.get('status_code', 500)

@admin_bp.route('/media/<int:media_id>/attach-tvdb', methods=['POST'])
@login_required
@admin_required
def attach_tvdb(media_id):
    """TVDB functionality temporarily disabled."""
    # TVDB disabled: route temporarily returns 501; imports removed per plan 280925_api_cleanup
    return jsonify({'success': False, 'error': 'TVDB functionality temporarily disabled'}), 501

@admin_bp.route('/media/<int:media_id>/pull-imdb', methods=['POST'])
@login_required
@admin_required
def pull_imdb(media_id):
    """
    Fetch IMDb details via RapidAPI and return fields to populate the form.
    
    First searches for the media title to detect single vs. multiple results:
    - Single result: Auto-populate form with IMDb data (existing behavior)
    - Multiple results: Store in session and redirect to selection page
    - Zero results or error: Return error response
    """
    from flask import session
    
    # OPTIMIZATION: First perform lightweight search to get count of matches
    # This only fetches basic search results (title, year, poster, IMDb ID)
    # Full detailed data is only fetched if count = 1
    search_result = imdb_search_results_admin(media_id)
    
    # Handle search errors
    if not search_result or not search_result.get('success'):
        error_msg = search_result.get('error', 'Failed to search IMDb') if search_result else 'Failed to search IMDb'
        return jsonify({'success': False, 'error': error_msg}), 500
    
    result_count = search_result.get('count', 0)
    
    # Handle zero results
    if result_count == 0:
        return jsonify({
            'success': False,
            'error': f"No IMDb results found for '{search_result.get('media_title', 'this title')}'"
        }), 404
    
    # Handle single result - fetch full IMDb details since we know it's the right match
    if result_count == 1:
        result = imdb_pull_admin(media_id)  # This fetches complete IMDb data
        if result['success']:
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Unknown error')}), 500
    
    # Handle multiple results - redirect to selection page WITHOUT fetching full data
    # This avoids expensive API calls for all 42+ results
    if result_count > 1:
        # Store only essential data to avoid session cookie size limit (4KB)
        # Lightweight search results will be re-fetched on the selection page
        session['imdb_search_pending'] = {
            'media_id': media_id,
            'timestamp': int(time.time())
        }
        # Explicitly mark session as modified to ensure it persists
        session.modified = True
        
        # Return JSON response indicating multiple results and redirect needed
        return jsonify({
            'success': True,
            'multiple_results': True,
            'count': result_count,
            'redirect_url': url_for('admin.media_edit_pull_results', media_id=media_id)
        })
    
    # Fallback error (should not reach here)
    return jsonify({'success': False, 'error': 'Unexpected result count'}), 500

@admin_bp.route('/media/<int:media_id>/pull-imdb/results', methods=['GET'])
@login_required
@admin_required
def media_edit_pull_results(media_id):
    """
    Display IMDb search results selection page when multiple results are found.
    
    Re-fetches search results for the media to avoid session cookie size limits.
    Validates that a search was recently initiated via session flag.
    
    Args:
        media_id: The ID of the media item being edited
        
    Returns:
        Rendered template with search results or redirect on error
    """
    import time
    from flask import session
    from models.models_media import Media, MediaType
    
    # Check session for pending search indicator
    search_pending = session.get('imdb_search_pending')
    
    # Validate session data exists and is recent (within 5 minutes)
    if not search_pending:
        flash('IMDb search results expired or not found. Please try searching again.', 'warning')
        return redirect(url_for('admin.media_edit', media_id=media_id))
    
    # Validate media_id matches
    if search_pending.get('media_id') != media_id:
        flash('IMDb search results do not match the requested media item.', 'error')
        session.pop('imdb_search_pending', None)
        return redirect(url_for('admin.media_edit', media_id=media_id))
    
    # Validate timestamp (5 minute expiry)
    search_timestamp = search_pending.get('timestamp', 0)
    if int(time.time()) - search_timestamp > 300:  # 5 minutes
        flash('IMDb search results expired. Please try searching again.', 'warning')
        session.pop('imdb_search_pending', None)
        return redirect(url_for('admin.media_edit', media_id=media_id))
    
    # Retrieve media record
    media = Media.query.get_or_404(media_id)
    
    # Re-fetch search results
    search_result = imdb_search_results_admin(media_id)
    
    # Handle search errors
    if not search_result or not search_result.get('success'):
        error_msg = search_result.get('error', 'Failed to retrieve search results') if search_result else 'Failed to retrieve search results'
        flash(error_msg, 'error')
        session.pop('imdb_search_pending', None)
        return redirect(url_for('admin.media_edit', media_id=media_id))
    
    search_results = search_result.get('results', [])
    result_count = search_result.get('count', 0)
    media_title = search_result.get('media_title', media.title)
    
    # Validate we have results
    if not search_results or result_count == 0:
        flash('No search results found. Please try searching again.', 'warning')
        session.pop('imdb_search_pending', None)
        return redirect(url_for('admin.media_edit', media_id=media_id))
    
    # Build IMDb type code to display name mapping from database
    # Query all media types that have IMDb codes defined
    imdb_type_mapping = {}
    media_types = MediaType.query.filter(MediaType.codes_imdb.isnot(None)).all()
    
    for mt in media_types:
        if mt.codes_imdb:
            # Split comma-separated codes and map each to the name
            codes = [code.strip().lower() for code in mt.codes_imdb.split(',') if code.strip()]
            for code in codes:
                imdb_type_mapping[code] = mt.name
    
    # Render the selection template with context data
    return render_template(
        'admin/media_edit_pull_results.html',
        media=media,
        search_results=search_results,
        result_count=result_count,
        media_title=media_title,
        imdb_type_mapping=imdb_type_mapping
    )
@admin_bp.route('/media/<int:media_id>/pull-imdb/select/<string:imdb_id>', methods=['GET'])
@login_required
@admin_required
def media_edit_pull_select(media_id, imdb_id):
    """
    Handle user selection from IMDb search results and populate media edit form.
    
    This route is called when the admin selects a specific IMDb result from the
    selection page. It validates the media_id, calls imdb_pull_admin with the
    selected imdb_id to fetch full IMDb data, and returns a JSON response with
    the populated media data for the frontend to use in the edit form.
    
    Args:
        media_id: The ID of the media item being edited
        imdb_id: The selected IMDb ID (format: tt1234567)
        
    Returns:
        JSON response with success status and populated media data, or error details
    """
    from flask import session
    from models.models_media import Media
    
    try:
        # Validate media_id exists in database
        media = Media.query.get_or_404(media_id)
        
        # Validate imdb_id format (basic validation)
        imdb_id = (imdb_id or '').strip()
        if not imdb_id or not imdb_id.startswith('tt'):
            return jsonify({
                'success': False,
                'error': 'Invalid IMDb ID format. Expected format: tt1234567'
            }), 400
        
        # Call imdb_pull_admin with the selected imdb_id to get full IMDb data
        result = imdb_pull_admin(media_id=media_id, imdb_id=imdb_id)
        
        # Check if the pull was successful
        if not result or not result.get('success'):
            error_msg = result.get('error', 'Failed to fetch IMDb data') if result else 'Failed to fetch IMDb data'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 500
        
        # Clean up session data from the search process
        session.pop('imdb_search_pending', None)
        
        # Return successful response with populated data
        return jsonify({
            'success': True,
            'media_id': media_id,
            'imdb_id': result.get('imdb_id'),
            'rating': result.get('rating'),
            'rating_rounded_1dp': result.get('rating_rounded_1dp'),
            'rating_rounded': result.get('rating_rounded'),
            'data': result.get('data', {})
        })
        
    except Exception as e:
        current_app.logger.error(f"[DEBUG] media_edit_pull_select error for media {media_id}, imdb_id {imdb_id}: {str(e)}")
        # Clean up session on error
        session.pop('imdb_search_pending', None)
        return jsonify({
            'success': False,
            'error': f'Error processing selection: {str(e)}'
        }), 500


# Import IMDb item by imdb_id (for external IMDb search results)
@admin_bp.route('/imdb/import/<string:imdb_id>', methods=['GET'])
@login_required
@admin_required
def import_imdb(imdb_id):
    """Import IMDb metadata item and redirect to appropriate page."""
    return handle_util_result(imdb_import_admin(imdb_id))


