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


# Modified by openai/gpt-5 | 2025-10-23
def upload_media_get_util():
    """
    Utility function to display the media upload form.
    
    This function handles the business logic for rendering the upload form
    with media types populated and owner preselected when provided.
    
    Returns:
        dict: Result containing success status and template data
    """
    try:
        # Get query parameters
        owner_user_id = request.args.get('owner_user_id', type=int)
        selected_media_type_id = request.args.get('media_type_id', type=int)
        
        # DEBUG: Log all query parameters
        current_app.logger.info(f"[DEBUG] upload_media GET - All query args: {dict(request.args)}")
        current_app.logger.info(f"[DEBUG] upload_media GET - owner_user_id: {owner_user_id} (type: {type(owner_user_id)})")
        current_app.logger.info(f"[DEBUG] upload_media GET - selected_media_type_id: {selected_media_type_id}")
        
        # Load MediaTypes list ordered by name
        media_types = MediaType.query.order_by(MediaType.name.asc()).all()
        
        # Prepare owner summary and validation if owner_user_id is present
        owner_summary = None
        owner_invalid = False
        
        if owner_user_id:
            current_app.logger.info(f"[DEBUG] Looking up owner with user_id: {owner_user_id}")
            # Fetch user by primary key without pre-filtering by is_active
            user = User.query.get(owner_user_id)
            
            if user:
                current_app.logger.info(f"[DEBUG] Found user: {user.username}, is_active: {user.is_active}")
                # Check if user is active after fetching
                if user.is_active:
                    owner_summary = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_active': user.is_active
                    }
                    current_app.logger.info(f"[DEBUG] Owner summary created for active user: {user.username}")
                else:
                    current_app.logger.info(f"[DEBUG] User {user.username} exists but is inactive")
                    owner_invalid = True
            else:
                current_app.logger.info(f"[DEBUG] No user found with id: {owner_user_id}")
                owner_invalid = True
        else:
            current_app.logger.info("[DEBUG] No owner_user_id parameter provided")
        
        # Prepare context for template
        context = {
            'owner_user_id': owner_user_id,
            'owner_summary': owner_summary,
            'owner_invalid': owner_invalid,
            'media_types': media_types,
            'selected_media_type_id': selected_media_type_id
        }
        
        # DEBUG: Log final context being passed to template
        current_app.logger.info(f"[DEBUG] Final template context - owner_user_id: {context['owner_user_id']}")
        current_app.logger.info(f"[DEBUG] Final template context - owner_summary: {context['owner_summary']}")
        current_app.logger.info(f"[DEBUG] Final template context - owner_invalid: {context['owner_invalid']}")
        
        return {
            'success': True,
            'template': 'admin/media_upload.html',
            'data': context
        }
        
    except Exception as e:
        current_app.logger.error(f"[DEBUG] Error in upload_media GET: {str(e)}")
        return {
            'success': False,
            'message': 'Error loading upload form',
            'message_type': 'error',
            'redirect': url_for('admin.media')
        }


# Modified by Claude Sonnet 4.5 | 2025-10-23
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
        config = MediaFileConfig.from_app_config(current_app.config)
        handler = MediaFileHandler(config)
        
        messages = []
        saved_count = 0
        
        # 5. Process each file individually
        for file in valid_files:
            result = handler.process_file(file, owner.id, media_type.code)
            
            if result.ok:
                try:
                    # Use a nested transaction for each database record
                    with db.session.begin_nested():
                        media_data = prepare_media_record_data(
                            result.data, owner, media_type, current_user
                        )
                        new_media = Media(**media_data)
                        db.session.add(new_media)
                        
                        # Log the specific user action
                        UserAction.log_action(
                            user_id=current_user.id,
                            action_type='admin_upload_media', action_category='admin',
                            details={
                                'owner_user_id': owner.id, 
                                'filename': result.data['filename_original']
                            },
                            ip_address=request.remote_addr,
                            user_agent=request.headers.get('User-Agent', '')
                        )
                    saved_count += 1
                except Exception as e:
                    current_app.logger.error(f"Database save failed for {file.filename}: {str(e)}", exc_info=True)
                    messages.append(('error', f"{file.filename}: Database save failed."))
            else:
                messages.append(('error', f"{file.filename}: {', '.join(result.errors)}"))
        
        # 6. Commit all successful records at once
        if saved_count > 0:
            db.session.commit()
            messages.append(('success', f'Successfully uploaded {saved_count} file(s).'))
        
        # 7. Build appropriate response with flashed messages
        redirect_url = url_for('admin.media_management') if saved_count > 0 and not any(m[0] == 'error' for m in messages) \
                       else url_for('admin.upload_media', owner_user_id=owner.id, media_type_id=media_type.id)
                       
        return build_multi_message_response(messages, redirect_url)
        
    except Exception as e:
        current_app.logger.error(f"Error in upload_media_post_util: {str(e)}", exc_info=True)
        return handle_util_result({
            'success': False, 'message': 'An unexpected error occurred during processing.',
            'redirect': url_for('admin.upload_media')
        })


# Modified by Claude Sonnet 4.5 | 2025-10-23
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


# Modified by openai/gpt-5 | 2025-10-23
def select_owner_search_util():
    """
    Utility function for AJAX endpoint for owner selection search.
    
    This function handles the business logic for owner selection
    with pagination support via AJAX.
    
    Returns:
        dict: Result containing success status and JSON response data
    """
    try:
        # Get query parameters - accept both 'term' and 'q'/'search' for backward compatibility
        search_term = request.args.get('term', '').strip()
        if not search_term:
            search_term = request.args.get('q', '').strip()
        if not search_term:
            search_term = request.args.get('search', '').strip()
            
        active_only = request.args.get('active_only', 'true').lower() in ('true', '1')
        resellers_only = request.args.get('resellers_only', 'false').lower() in ('true', '1')
        limit = request.args.get('limit', 20, type=int)
        page = request.args.get('page', 1, type=int)
        
        # Log effective filters for debugging
        current_app.logger.info(f"[DEBUG] select_owner_search filters - search_term: '{search_term}', active_only: {active_only}, resellers_only: {resellers_only}, limit: {limit}, page: {page}")
        
        # Validate search term
        if not search_term:
            return {
                'success': True,
                'json_response': {
                    'users': [],
                    'pagination': {
                        'page': page,
                        'per_page': limit,
                        'total': 0,
                        'pages': 0,
                        'has_next': False,
                        'has_prev': False
                    }
                }
            }
        
        # Build base query
        query = db.session.query(User)
        
        # Apply active filter
        if active_only:
            query = query.filter(User.is_active == True)
        
        # Apply resellers filter if requested
        if resellers_only:
            # Filter for reseller user type only
            reseller_type = UserType.query.filter_by(code='reseller').first()
            if reseller_type:
                query = query.filter(User.users_type_id == reseller_type.id)
        
        # Apply search filter
        search_pattern = f'%{search_term}%'
        query = query.filter(
            or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )
        
        # Sort by username ascending
        query = query.order_by(User.username.asc())
        
        # Pagination: calculate total and apply offset/limit
        per_page = limit
        total = query.count()
        offset = (page - 1) * per_page
        users = query.offset(offset).limit(per_page).all()
        
        # Calculate pagination info
        pages = (total + per_page - 1) // per_page  # Ceiling division
        has_next = page < pages
        has_prev = page > 1
        
        # Prepare user data with reseller flag
        user_data = []
        for user in users:
            is_reseller = user.user_type and user.user_type.code == 'reseller'
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'is_reseller': is_reseller
            })
        
        # Return paginated response matching data contract
        return {
            'success': True,
            'json_response': {
                'users': user_data,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages,
                    'has_next': has_next,
                    'has_prev': has_prev
                }
            }
        }
        
    except Exception as e:
        current_app.logger.error(f"[DEBUG] Error in select_owner_search: {str(e)}")
        return {
            'success': False,
            'json_response': {'error': 'Search failed'},
            'status_code': 500
        }