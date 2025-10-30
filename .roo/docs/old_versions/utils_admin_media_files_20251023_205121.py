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


# Modified by openai/gpt-5 | 2025-10-23
def upload_media_post_util():
    """
    Utility function to process media upload form submission.
    
    This function handles the business logic for file uploads, validation,
    storage, and database record creation.
    
    Returns:
        dict: Result containing success status and redirect info
    """
    try:
        
        # Validate CSRF token if enabled
        if current_app.config.get('WTF_CSRF_ENABLED') is True:
            try:
                validate_csrf(request.form.get('csrf_token'))
                current_app.logger.info("[DEBUG] CSRF token validation passed for upload_media_post")
            except Exception as e:
                current_app.logger.error(f"[DEBUG] CSRF token validation failed for upload_media_post: {str(e)}")
                return {
                    'success': False,
                    'message': 'Security token validation failed. Please try again.',
                    'message_type': 'error',
                    'redirect': url_for('admin.upload_media')
                }
        
        # Get form data
        owner_user_id = request.form.get('owner_user_id', type=int)
        media_type_id = request.form.get('media_type_id', type=int)
        
        # Log upload attempt
        current_app.logger.info(f"[DEBUG] Upload attempt - owner_user_id: {owner_user_id}, media_type_id: {media_type_id}")
        
        # Validate required fields
        if not owner_user_id:
            return {
                'success': False,
                'message': 'Please select an owner for the media.',
                'message_type': 'error',
                'redirect': url_for('admin.upload_media')
            }
        
        if not media_type_id:
            return {
                'success': False,
                'message': 'Please select a media type.',
                'message_type': 'error',
                'redirect': url_for('admin.upload_media', owner_user_id=owner_user_id)
            }
        
        # Verify owner exists and is active
        owner = User.query.get(owner_user_id)
        if not owner:
            return {
                'success': False,
                'message': 'Selected owner not found.',
                'message_type': 'error',
                'redirect': url_for('admin.upload_media')
            }
        
        if not owner.is_active:
            return {
                'success': False,
                'message': 'Selected owner is not active.',
                'message_type': 'error',
                'redirect': url_for('admin.upload_media')
            }
        
        # Verify media type exists
        media_type = MediaType.query.get(media_type_id)
        if not media_type:
            return {
                'success': False,
                'message': 'Selected media type not found.',
                'message_type': 'error',
                'redirect': url_for('admin.upload_media', owner_user_id=owner_user_id)
            }
            
        # Get uploaded files
        uploaded_files = request.files.getlist('file')
        
        # Filter out empty file entries (browsers often include empty file slots)
        valid_files = [f for f in uploaded_files if f and f.filename != '']
        
        if not valid_files:
            return {
            'success': False,
            'message': 'Please select at least one file to upload.',
            'message_type': 'error',
            'redirect': url_for('admin.upload_media', owner_user_id=owner_user_id, media_type_id=media_type_id)
        }
        
        # Media processing utilities already imported from media_core at top of file
        # Process uploaded files using media_core function
        successful_uploads, error_messages = process_uploaded_files(
            valid_files,
            owner_user_id,
            media_type.code
        )
        
        # Save successful uploads to database
        saved_count = 0
        for file_info in successful_uploads:
            try:
                # Create new media record
                new_media = Media(
                    users_id=owner_user_id,
                    media_type_id=media_type_id,
                    title=file_info['filename_original'].rsplit('.', 1)[0],  # Use filename without extension as title
                    description=f"Uploaded by admin for {owner.username}",
                    filename_original=file_info['filename_original'],
                    filename_stored=file_info['filename_stored'],
                    file_path=file_info['file_path'],
                    file_size_bytes=file_info['file_size_bytes'],
                    mime_type=file_info['mime_type'],
                    file_hash=file_info['file_hash'],
                    thumbnail_path=file_info.get('thumbnail_path'),
                    media_metadata=file_info.get('media_metadata', {}),
                    tags='',
                    is_public=False,  # Default to private
                    is_featured=False,
                    is_processed=True,  # Mark as processed since we saved it
                    processing_status='completed',
                    download_count=0,
                    view_count=0,
                    like_count=0,
                    credit_cost=media_type.credit_cost,
                    adult=False,
                    min_age=0,
                    created_at=datetime.now(timezone.utc),
                    created_by=current_user.id
                )
                
                db.session.add(new_media)
                saved_count += 1
                
                # Log the upload action
                try:
                    UserAction.log_action(
                        user_id=current_user.id,
                        action_type='admin_upload_media',
                        action_category='admin',
                        details={
                            'owner_user_id': owner_user_id,
                            'owner_username': owner.username,
                            'media_type': media_type.name,
                            'filename': file_info['filename_original'],
                            'file_size_mb': round(file_info['file_size_bytes'] / (1024 * 1024), 2)
                        },
                        ip_address=request.remote_addr,
                        user_agent=request.headers.get('User-Agent', ''),
                        target_type='media',
                        target_id=None  # Will be set after commit
                    )
                except Exception as e:
                    current_app.logger.error(f"[DEBUG] Failed to log UserAction: {str(e)}")
                
            except Exception as e:
                current_app.logger.error(f"[DEBUG] Error saving media to database: {str(e)}")
                error_messages.append(f"{file_info['filename_original']}: Database save failed")
        
        # Commit all database changes
        if saved_count > 0:
            try:
                db.session.commit()
                current_app.logger.info(f"[DEBUG] Successfully saved {saved_count} media files to database")
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"[DEBUG] Database commit failed: {str(e)}")
                return {
                    'success': False,
                    'message': 'Error saving media to database. Files were uploaded but not recorded.',
                    'message_type': 'error',
                    'redirect': url_for('admin.upload_media')
                }
        
        # Determine success/error messages and redirect
        messages = []
        if saved_count > 0:
            messages.append(('success', f'Successfully uploaded {saved_count} file(s).'))
        
        if error_messages:
            for error in error_messages:
                messages.append(('error', f'Error: {error}'))
        
        # Determine redirect based on results
        if saved_count > 0 and not error_messages:
            # All successful, go to media list
            redirect_url = url_for('admin.media')
        else:
            # Some errors, stay on upload page
            redirect_url = url_for('admin.upload_media', owner_user_id=owner_user_id, media_type_id=media_type_id)
        
        return {
            'success': True,
            'messages': messages,
            'redirect': redirect_url
        }
        
    except Exception as e:
        import traceback
        current_app.logger.error(f"[DEBUG] Error in upload_media_post: {str(e)}")
        current_app.logger.error(f"[DEBUG] Full traceback: {traceback.format_exc()}")
        # Return a failure response so the request doesn't hang
        return {
            'success': False,
            'message': 'An unexpected error occurred during processing.',
            'message_type': 'error',
            'redirect': url_for('admin.upload_media')
        }


# Modified by openai/gpt-5 | 2025-10-23
def select_owner_util():
    """
    Utility function to display the owner selection page.
    
    This function handles the business logic for owner selection
    with filtering and pagination.
    
    Returns:
        dict: Result containing success status and template data
    """
    try:
        # Get and validate query parameters
        next_url = request.args.get('next', '/admin/media/upload')
        show_all = request.args.get('show_all', '').lower() in ('true', '1', 'on', 'yes')
        resellers_only = request.args.get('resellers_only', '').lower() in ('true', '1', 'on', 'yes')
        page = request.args.get('page', 1, type=int)
        
        # Accept both 'q' and 'search' parameters for backward compatibility
        search_term = request.args.get('q', '').strip()
        if not search_term:
            search_term = request.args.get('search', '').strip()
        
        # Log effective filters for debugging
        current_app.logger.info(f"[DEBUG] select_owner filters - show_all: {show_all}, resellers_only: {resellers_only}, search_term: '{search_term}', page: {page}")
        
        # Validate and sanitize next parameter - only allow /admin/media/upload
        if not next_url.startswith('/admin/media/upload'):
            next_url = '/admin/media/upload'
        
        # Build base query
        query = db.session.query(User)
        
        # Apply active filter (default: active users only)
        if not show_all:
            query = query.filter(User.is_active == True)
        
        # Apply resellers filter if requested
        if resellers_only:
            # Filter for reseller user type only
            reseller_type = UserType.query.filter_by(code='reseller').first()
            if reseller_type:
                query = query.filter(User.users_type_id == reseller_type.id)
        
        # Apply search filter if provided
        if search_term:
            search_pattern = f'%{search_term}%'
            query = query.filter(
                or_(
                    User.username.ilike(search_pattern),
                    User.email.ilike(search_pattern)
                )
            )
        
        # Sort by username ascending
        query = query.order_by(User.username.asc())
        
        # Pagination: 20 per page
        per_page = 20
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
        
        # Prepare context
        context = {
            'users': user_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages,
                'has_next': has_next,
                'has_prev': has_prev
            },
            'filters': {
                'show_all': show_all,
                'resellers_only': resellers_only,
                'q': search_term,
                'sort_label': 'Username (A-Z)'
            },
            'next': next_url
        }
        
        return {
            'success': True,
            'template': 'admin/select_owner.html',
            'data': context
        }
        
    except Exception as e:
        current_app.logger.error(f"[DEBUG] Error in select_owner: {str(e)}")
        return {
            'success': False,
            'error': 'Error loading owner selection',
            'status_code': 500
        }


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