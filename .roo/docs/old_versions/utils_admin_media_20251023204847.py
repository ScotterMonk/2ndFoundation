"""
Admin utility functions for media management.

This module contains utility functions for admin media operations that are called
from the main admin blueprint routes. Functions here should not have route decorators
as they are imported and used by admin.py.

Note: TVDB integration temporarily disabled; do not re-add imports from utils.utils_tvdb during plan 280925_api_cleanup.
"""

from flask import request, url_for, current_app, jsonify, render_template, flash, redirect
from flask_login import current_user
from flask_wtf.csrf import validate_csrf
from datetime import datetime, timezone
from sqlalchemy import func, and_, or_, distinct
from sqlalchemy.orm import joinedload
from utils.database import db
import re
import json
import logging

# Import required models
from models.models_user import User, UserType, UserAction
from models.models_media import Media, MediaType, Genre, MediaGenre, Director, MediaDirector, Performer, MediaPerformer

# Import utility functions from specialized modules
from routes.utils_admin_api import imdb_search_admin
from utils.imdb_core import imdb_id_normalize, imdb_item_normalize
# Import core media functions
from utils.media_core import merge_and_deduplicate_results
# TVDB utilities temporarily disabled - removed import of attach_tvdb_util, _to_tvdb_item

# Import route helpers and form utilities for refactored media_edit_util
from utils.route_helpers import handle_util_result, is_ajax_request
from utils.media_associations_core import process_media_associations
from routes.utils_admin_forms import extract_media_form_data, extract_search_params
from routes.utils_admin_media_files import search_imdb_for_media_details

logger = logging.getLogger(__name__)

def media_management_util():
    """
    Utility function to get media management data.
    
    This function handles the business logic for displaying and managing
    media items with metrics, search, and sorting.
    
    Returns:
        dict: Template data including media list, search results, and pagination
    """
    try:
        # Extract search term (supports 'q' and 'search')
        search_term = (request.args.get('q', '') or request.args.get('search', '')).strip()

        # Extract genre filter (optional). Do not apply filtering yet; just parse and pass through.
        genre_id_raw = (request.args.get('genre_id', '') or '').strip()
        selected_genre_id = None
        if genre_id_raw:
            try:
                gid = int(genre_id_raw)
                if gid > 0:
                    selected_genre_id = gid
            except (TypeError, ValueError):
                selected_genre_id = None
        
        # Get sorting parameters - default to title ascending
        sort = request.args.get('sort', 'title')
        direction = request.args.get('direction', 'asc')

        # Whitelist sortable columns
        # Support sorting by aggregated user rating (preferred)
        sort_map = {
            'title': Media.title,
            'type': MediaType.name,  # Will need join for media type name
            'rating_user': Media.user_rating_100,
            'rating_tmdb': Media.tmdb_rating,
            'created_at': Media.created_at,
            'director': Director.name
        }
        sort_col = sort_map.get(sort, Media.created_at)
        order_clause = sort_col.asc() if direction == 'asc' else sort_col.desc()

        # Base query for media, joining with User for search capabilities and MediaType for sorting
        # Use joinedload to eagerly load the media_type relationship
        base_query = (
            db.session.query(Media)
            .options(joinedload(Media.media_type))
            .join(User, Media.users_id == User.id)
            .join(MediaType, Media.media_type_id == MediaType.id)
        )

        # Apply search filter
        if search_term:
            pattern = f'%{search_term}%'
            conditions = [
                Media.title.ilike(pattern),
                User.username.ilike(pattern),
                User.email.ilike(pattern)
            ]
            if search_term.isdigit():
                conditions.append(Media.id == int(search_term))
            base_query = base_query.filter(or_(*conditions))

        # Apply genre filter when provided (AND with search)
        if selected_genre_id:
            # Use explicit join to the association table to follow existing query patterns
            base_query = base_query.join(
                MediaGenre, MediaGenre.media_id == Media.id
            ).filter(
                MediaGenre.genre_id == selected_genre_id
            )

        # Apply sorting and execute
        media_list = base_query.order_by(order_clause, Media.id.asc()).all()

        # Load genres for dropdown (do not fail page if this query errors)
        try:
            genres = Genre.query.order_by(Genre.name.asc()).all()
        except Exception as _e:
            current_app.logger.error(f"[DEBUG] Failed to load genres for admin.media: {_e}")
            genres = []

        # ===== IMDb SEARCH (title and/or genre) =====
        # Uses imdb_search_admin which calls utils.imdb_core functions
        imdb_results = imdb_search_admin(search_term, selected_genre_id)

        # Merge DB and IMDb search results using helper
        try:
            merged_results = merge_and_deduplicate_results(media_list, imdb_results)
        except Exception as _e:
            current_app.logger.error(f"[DEBUG] Failed to merge DB and IMDb results in admin.media: {_e}")
            merged_results = list(media_list or [])
        
        # Normalize merged results for sorting and template compatibility
        try:
            # Map DB ids to created_at to enrich merged items
            id_to_created = {}
            for m in (media_list or []):
                try:
                    if getattr(m, 'id', None) is not None:
                        id_to_created[m.id] = getattr(m, 'created_at', None)
                except Exception:
                    continue

            for item in merged_results:
                if not isinstance(item, dict):
                    # Safety: convert ORM objects to lightweight dict if any slipped through
                    try:
                        item = {
                            'id': getattr(item, 'id', None),
                            'title': getattr(item, 'title', '') or getattr(item, 'name', '') or '',
                            'type': (getattr(getattr(item, 'media_type', None), 'code', None) or getattr(getattr(item, 'media_type', None), 'name', None) or '').strip().lower(),
                            'user_rating_100': getattr(item, 'user_rating_100', None),
                            'source': 'DB'
                        }
                    except Exception:
                        continue
                # Provide user_rating_100 from rating_user if available (template expects this key)
                try:
                    if 'user_rating_100' not in item and item.get('rating_user') not in (None, '', 'N/A'):
                        item['user_rating_100'] = item.get('rating_user')
                except Exception:
                    pass
                # Attach created_at for DB-backed items to support created_at sort
                try:
                    if 'created_at' not in item and item.get('id') in id_to_created:
                        item['created_at'] = id_to_created.get(item.get('id'))
                except Exception:
                    pass
        except Exception as _norm_e:
            current_app.logger.error(f"[DEBUG] Merged results normalization error: {_norm_e}")

        # Sorting across merged results
        sort_field = (sort or 'created_at').strip().lower()
        reverse_order = (direction == 'desc')

        # Import helper functions from media_core for sorting
        from utils.media_core import _rating_value, _title_tuple, _type_tuple, _rating_tuple
        
        def _created_sort_tuple(i):
            dt = i.get('created_at') if isinstance(i, dict) else None
            if dt is None:
                # missing created_at always last
                return (1, 0.0)
            try:
                ts = dt.timestamp()
            except Exception:
                ts = 0.0
            # invert timestamp for desc while keeping missing last
            return (0, (-ts if reverse_order else ts))
        
        def _rating_tuple_with_direction(i):
            from utils.media_core import _rating_value
            v = _rating_value(i)
            if v is None:
                return (1, 0.0)  # missing last
            return (0, (-v if reverse_order else v))

        try:
            if sort_field == 'title':
                merged_results.sort(key=_title_tuple)
            elif sort_field == 'type':
                merged_results.sort(key=_type_tuple)
            elif sort_field == 'rating_user':
                merged_results.sort(key=_rating_tuple)
            elif sort_field == 'created_at':
                merged_results.sort(key=_created_sort_tuple)
            else:
                # Fallback to title sort
                merged_results.sort(key=_title_tuple)
        except Exception as _sort_e:
            current_app.logger.error(f"[DEBUG] Sorting merged results error: {_sort_e}")

        # Pagination (server-side) over merged results
        try:
            per_page = request.args.get('per_page', type=int) or 20
            if per_page <= 0:
                per_page = 20
            page = request.args.get('page', 1, type=int) or 1
            if page < 1:
                page = 1
            total = len(merged_results)
            pages = (total + per_page - 1) // per_page if per_page else 1
            if pages == 0:
                pages = 1
            if page > pages:
                page = pages
            start = (page - 1) * per_page
            end = start + per_page
            paged_results = merged_results[start:end] if per_page else merged_results
            pagination = {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages,
                'has_next': page < pages,
                'has_prev': page > 1
            }
        except Exception as _page_e:
            current_app.logger.error(f"[DEBUG] Pagination build error: {_page_e}")
            paged_results = merged_results
            pagination = {
                'page': 1,
                'per_page': len(merged_results),
                'total': len(merged_results),
                'pages': 1,
                'has_next': False,
                'has_prev': False
            }

        return {
            'success': True,
            'template': 'admin/media.html',
            'data': {
                'media': paged_results,
                'q': search_term,
                'sort': sort,
                'direction': direction,
                # Genre dropdown data and current selection
                'genres': genres,
                'genre_id': selected_genre_id,
                'selected_genre_id': selected_genre_id,
                # Pagination context for template (if/when rendered)
                'pagination': pagination,
                'page': pagination.get('page'),
                'per_page': pagination.get('per_page'),
                'results_count': pagination.get('total')
            }
        }

    except Exception as e:
        current_app.logger.error(f"[DEBUG] Error in media_management_util: {str(e)}")
        return {
            'success': False,
            'error': f'Error loading media management: {str(e)}',
            'status_code': 500
        }


# Modified by Sonnet 4.5 | 2025-10-23
def media_edit_util(media_id):
    """
    Handles both displaying and processing the media edit form.
    This function has been refactored to use modular helpers.
    """
    media_item = db.session.query(Media).options(
        joinedload(Media.media_type),
        joinedload(Media.genres),
        joinedload(Media.directors),
        joinedload(Media.performers)
    ).filter_by(id=media_id).first_or_404()

    media_types = MediaType.query.order_by(MediaType.name).all()

    if request.method == 'GET':
        return {
            'success': True,
            'template': 'admin/media_edit.html',
            'data': {'media': media_item, 'media_types': media_types}
        }

    # --- POST Request Processing ---
    try:
        data, errors = extract_media_form_data(request)
        if errors:
            flash('. '.join(errors), 'error')
            return handle_util_result({
                'success': False, 
                'template': 'admin/media_edit.html',
                'data': {'media': media_item, 'media_types': media_types}
            })

        # Update basic fields
        media_item.title = data['title']
        media_item.summary = data['summary']
        media_item.rating = data['rating']
        media_item.media_type_id = data['media_type_id']
        media_item.is_public = data['is_public']
        media_item.is_featured = data['is_featured']
        db.session.commit()

        # Process associations in a single transaction block for atomicity
        association_errors = []
        try:
            with db.session.begin_nested():
                # Process Genres
                if data['imdb_genres_str']:
                    genre_result = process_media_associations(
                        db.session, media_item.id, data['imdb_genres_str'], 
                        MediaGenre, Genre, create_if_missing=True
                    )
                    if not genre_result.ok:
                        association_errors.extend(genre_result.errors)
                
                # Process Directors
                if data['imdb_directors_str']:
                    director_result = process_media_associations(
                        db.session, media_item.id, data['imdb_directors_str'],
                        MediaDirector, Director, create_if_missing=True
                    )
                    if not director_result.ok:
                        association_errors.extend(director_result.errors)

                # Process Performers
                if data['imdb_performers_str']:
                    performer_result = process_media_associations(
                        db.session, media_item.id, data['imdb_performers_str'],
                        MediaPerformer, Performer, create_if_missing=True
                    )
                    if not performer_result.ok:
                        association_errors.extend(performer_result.errors)
            
            if association_errors:
                 raise Exception("Error processing associations.")

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error processing associations for media {media_id}: {e}", exc_info=True)
            flash(f"Failed to update associations: {', '.join(association_errors) or str(e)}", "error")
            return handle_util_result({
                'success': False,
                'template': 'admin/media_edit.html',
                'data': {'media': media_item, 'media_types': media_types}
            })

        UserAction.log_action(
            user_id=current_user.id,
            action_type='admin_edit_media',
            action_category='admin',
            details={'media_id': media_item.id, 'title': media_item.title},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )

        flash(f'Successfully updated "{media_item.title}".', 'success')
        return handle_util_result({
            'success': True,
            'redirect': url_for('admin.media_management')
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in media_edit_util for media_id {media_id}: {e}", exc_info=True)
        flash('An unexpected error occurred. Please try again.', 'error')
        return handle_util_result({
            'success': False,
            'template': 'admin/media_edit.html',
            'data': {'media': media_item, 'media_types': media_types},
            'status_code': 500
        })
