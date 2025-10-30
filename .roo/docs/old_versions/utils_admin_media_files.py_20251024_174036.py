"""
File operation utilities for admin media workflows.

This module contains Flask-aware utilities focused on file uploads and
owner selection flows used by the admin blueprint.

Note: Keep business logic in utils/*_core.py modules; this module handles
request/response concerns and DB persistence for uploads.
"""

from flask import request, url_for, current_app
from flask_login import current_user
from flask_wtf.csrf import validate_csrf
from datetime import datetime, timezone
from sqlalchemy import or_
from utils.database import db

from models.models_user import User, UserType, UserAction
from models.models_media import Media, MediaType

# Import media processing facade that delegates to core implementation
from utils.media import process_uploaded_files

# Import required core utilities for admin media files
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


# Modified by GPT-5 | 2025-10-24
def upload_media_get_util():
    """Display the media upload form."""
    try:
        from routes.utils_admin_upload import validate_upload_requirements
        from utils.route_helpers import handle_util_result
        from flask import request, url_for
        from models.models_media import MediaType
        from utils.database import db
        from forms import UploadMediaForm  # Assuming forms.py provides this form
        import logging

        logger = logging.getLogger(__name__)

        # Extract parameters
        owner_user_id = request.args.get('owner_user_id', type=int)
        media_type_id = request.args.get('media_type_id', type=int)

        # Validate upload requirements (owner/media type are optional for GET)
        val_result = validate_upload_requirements(
            request, db.session,
            require_owner=False,
            require_media_type=False
        )

        # Handle invalid requirements
        if not val_result.get('valid', False):
            message = (val_result.get('errors') or ['Invalid upload parameters.'])[0]
            return handle_util_result({
                'success': False,
                'message': message,
                'redirect': url_for('admin.upload_media',
                                    owner_user_id=owner_user_id,
                                    media_type_id=media_type_id)
            })

        owner = val_result.get('owner')
        media_type = val_result.get('media_type')

        # Load all media types for dropdown
        media_types = MediaType.query.order_by(MediaType.name.asc()).all()

        # Prepare form with preselected values when available
        form = UploadMediaForm()
        if owner:
            setattr(form, 'owner_user_id', getattr(form, 'owner_user_id', None))
            if hasattr(form, 'owner_user_id') and hasattr(form.owner_user_id, 'data'):
                form.owner_user_id.data = owner.id
        if media_type:
            setattr(form, 'media_type_id', getattr(form, 'media_type_id', None))
            if hasattr(form, 'media_type_id') and hasattr(form.media_type_id, 'data'):
                form.media_type_id.data = media_type.id

        # Prepare data for template
        return {
            'success': True,
            'template': 'admin/upload_media.html',
            'data': {
                'form': form,
                'owner': owner,
                'media_type': media_type,
                'media_types': media_types
            }
        }
    except Exception as e:
        # Use logger in case Flask current_app isn't available during errors
        try:
            logger.error(f"Error in upload_media_get_util: {str(e)}", exc_info=True)
        except Exception:
            pass
        return handle_util_result({
            'success': False,
            'message': 'An unexpected error occurred while loading the upload page.',
            'redirect': url_for('admin.upload_media')
        })


# Modified by GPT-5 | 2025-10-24
def upload_media_post_util():
    """
    Process media file uploads by orchestrating validation, file handling,
    and database operations using modular helpers.
    """
    try:
        from routes.utils_admin_upload import (
            validate_upload_requirements, extract_uploaded_files,
            prepare_media_record_data
        )
        from utils.route_helpers import build_multi_message_response, handle_util_result
        from utils.media_core import MediaFileHandler, MediaFileConfig
        from flask_wtf.csrf import validate_csrf
        from flask import current_app, request, url_for
        from models.models_user import UserAction
        from models.models_media import Media
        from utils.database import db
        from flask_login import current_user
        
        # 1. CSRF validation
        try:
            validate_csrf(request.form.get('csrf_token'))
        except Exception:
            return handle_util_result({
                'success': False, 'message': 'CSRF token validation failed.',
                'redirect': url_for('admin.upload_media')
            })
            
        # 2. Validate prerequisites (owner, media type)
        val_result = validate_upload_requirements(request, db.session)
        if not val_result['valid']:
            return handle_util_result({
                'success': False, 'message': val_result['errors'][0],
                'redirect': url_for('admin.upload_media')
            })
        
        owner, media_type = val_result['owner'], val_result['media_type']
        
        # 3. Extract uploaded files from the request
        valid_files = extract_uploaded_files(request)
        if not valid_files:
            return handle_util_result({
                'success': False, 'message': 'Please select at least one file to upload.',
                'redirect': url_for('admin.upload_media', owner_user_id=owner.id, media_type_id=media_type.id)
            })
            
        # 4. Configure the media file handler from app config
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
        handler = MediaFileHandler(config)
        
        messages = []
        saved_count = 0
        
        # 5. Process each file individually
        for file in valid_files:
            result = handler.process_file(file, owner.id, media_type.code)
            
            # Fixed by Claude Sonnet 4 | 2025-10-24
            # CoreResult is implemented as TypedDict, use dictionary access patterns consistently
            if result.get('ok', False):
                try:
                    # Use a nested transaction for each database record
                    with db.session.begin_nested():
                        media_data = prepare_media_record_data(
                            result.get('data', {}), owner, media_type, current_user
                        )
                        new_media = Media(**media_data)
                        db.session.add(new_media)
                        
                        # Log the specific user action
                        UserAction.log_action(
                            user_id=current_user.id,
                            action_type='admin_upload_media', action_category='admin',
                            details={
                                'owner_user_id': owner.id,
                                'filename': result.get('data', {}).get('filename_original', file.filename)
                            },
                            ip_address=request.remote_addr,
                            user_agent=request.headers.get('User-Agent', '')
                        )
                    saved_count += 1
                except Exception as e:
                    current_app.logger.error(f"Database save failed for {file.filename}: {str(e)}", exc_info=True)
                    messages.append(('error', f"{file.filename}: Database save failed."))
            else:
                error_msgs = result.get('errors', [])
                if isinstance(error_msgs, list):
                    error_text = ', '.join(error_msgs)
                else:
                    error_text = str(error_msgs)
                messages.append(('error', f"{file.filename}: {error_text}"))
        
        # 6. Commit all successful records at once
        if saved_count > 0:
            db.session.commit()
            messages.append(('success', f'Successfully uploaded {saved_count} file(s).'))
        
        # 7. Build appropriate response with flashed messages
        redirect_url = (url_for('admin.media') if saved_count > 0 and not any(m[0] == 'error' for m in messages)
                        else url_for('admin.upload_media', owner_user_id=owner.id, media_type_id=media_type.id))
                        
        return build_multi_message_response(messages, redirect_url)
        
    except Exception as e:
        current_app.logger.error(f"Error in upload_media_post_util: {str(e)}", exc_info=True)
        return handle_util_result({
            'success': False, 'message': 'An unexpected error occurred during processing.',
            'redirect': url_for('admin.upload_media')
        })


# Modified by GPT-5 | 2025-10-24
def select_owner_util():
    """
    Display the owner selection page with filtering and pagination,
    orchestrating calls to core query and presentation helpers.
    """
    try:
        from utils.user_query_core import build_user_search_query, prepare_user_list_data
        from utils.media_query_core import paginate_media_query
        from utils.route_helpers import sanitize_redirect_url
        from models.models_user import User
        from utils.database import db
        from flask import request

        # 1. Extract and sanitize parameters
        next_url = sanitize_redirect_url(
            request.args.get('next', '/admin/media/upload'),
            allowed_paths=['/admin/media/upload']
        )
        show_all = request.args.get('show_all', '').lower() in ('true', '1', 'on', 'yes')
        resellers_only = request.args.get('resellers_only', '').lower() in ('true', '1', 'on', 'yes')
        search_term = request.args.get('q', '').strip() or request.args.get('search', '').strip()

        # 2. Build the user query using the core helper
        query = build_user_search_query(
            db.session, search_term,
            active_only=not show_all,
            resellers_only=resellers_only
        ).order_by(User.username.asc())
        
        # 3. Paginate the query using the unified pagination helper
        page = request.args.get('page', 1, type=int)
        page_result = paginate_media_query(query, page, per_page=20)
        
        # 4. Prepare the user data for the template
        user_data = prepare_user_list_data(page_result['items'])
        
        # 5. Return the structured data for rendering
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
        current_app.logger.error(f"Error in select_owner_util: {str(e)}", exc_info=True)
        return {'success': False, 'error': 'Error loading owner selection page', 'status_code': 500}


# Modified by GPT-5 | 2025-10-24
def select_owner_search_util():
    """
    Handle AJAX requests for searching users, orchestrating:
    - parameter extraction
    - core user query building
    - unified pagination
    - user data preparation
    Returns JSON structure consistent with select_owner_util pagination.
    """
    try:
        from utils.user_query_core import build_user_search_query, prepare_user_list_data
        from utils.media_query_core import paginate_media_query
        from models.models_user import User
        from utils.database import db
        from flask import request

        # 1) Extract parameters
        show_all = request.args.get('show_all', '').lower() in ('true', '1', 'on', 'yes')
        resellers_only = request.args.get('resellers_only', '').lower() in ('true', '1', 'on', 'yes')
        search_term = (request.args.get('q', '').strip()
                       or request.args.get('search', '').strip())
        page = request.args.get('page', 1, type=int)

        # 2) Build user query via core helper, ordered by username
        query = build_user_search_query(
            db.session,
            search_term,
            active_only=not show_all,
            resellers_only=resellers_only
        ).order_by(User.username.asc())

        # 3) Unified pagination (match select_owner_util per_page)
        page_result = paginate_media_query(query, page, per_page=20)

        # 4) Prepare user data
        user_data = prepare_user_list_data(page_result['items'])

        # 5) Return JSON-friendly structure consistent with page view util
        return {
            'success': True,
            'json_response': {
                'users': user_data,
                'pagination': page_result,
                'filters': {
                    'show_all': show_all,
                    'resellers_only': resellers_only,
                    'q': search_term
                }
            }
        }
    except Exception as e:
        current_app.logger.error(f"Error in select_owner_search_util: {str(e)}", exc_info=True)
        return {
            'success': False,
            'json_response': {'error': 'Failed to perform user search.'},
            'status_code': 500
        }