# Created by [model name] | 2025-10-23
import logging
import math
import warnings
from typing import List, Dict, Any, Union
from sqlalchemy.orm import Session, Query
from sqlalchemy import func, or_
from models.models_media import Media, MediaGenre
from models.models_user import User

# Per the plan, this logic is reused from utils/media_core.py to avoid duplication.
def _created_sort_key(item):
    return item.get('created_at_ts', 0)

def _title_sort_key(item):
    title = item.get('title', '').lower()
    # Basic logic for ignoring articles in sorting
    if title.startswith('the '):
        return title[4:]
    if title.startswith('a '):
        return title[2:]
    if title.startswith('an '):
        return title[3:]
    return title

def _rating_sort_key(item):
    return (item.get('rating', 0), item.get('created_at_ts', 0))

def _media_type_sort_key(item):
    return (item.get('media_type', '').lower(), _title_sort_key(item))

logger = logging.getLogger(__name__)

def build_media_search_query(db_session: Session, search_term: str = None, genre_id: int = None) -> Query:
    """
    Builds a SQLAlchemy query for searching media with optional filters.
    
    Args:
        db_session (Session): The database session.
        search_term (str, optional): The term to search for in media titles. Defaults to None.
        genre_id (int, optional): The ID of the genre to filter by. Defaults to None.
        
    Returns:
        Query: The SQLAlchemy query object.
    """
    query = db_session.query(Media).join(User, Media.users_id == User.id, isouter=True)
    
    if search_term:
        search_pattern = f"%{search_term}%"
        query = query.filter(Media.title.ilike(search_pattern))
        
    if genre_id:
        query = query.join(MediaGenre, Media.id == MediaGenre.media_id).filter(MediaGenre.genre_id == genre_id)
        
    return query

def normalize_media_results(media_list: List[Media]) -> List[Dict[str, Any]]:
    """
    Converts a list of Media ORM objects to a list of dictionaries with consistent shape.
    
    Args:
        media_list (List[Media]): A list of Media ORM objects.
        
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a media item.
    """
    normalized = []
    for media in media_list:
        normalized.append({
            'id': media.id,
            'title': media.title,
            'rating': (getattr(media, 'user_rating_100', None) or getattr(media, 'imdb_rating', None) or 0),
            'created_at': media.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at_ts': media.created_at.timestamp(),
            'media_type': media.media_type.name if media.media_type else 'N/A',
            'owner_username': getattr((getattr(media, 'owner', None) or getattr(media, 'user', None)), 'username', 'N/A')
        })
    return normalized

def sort_media_results(results: List[Dict[str, Any]], sort_field: str, direction: str) -> List[Dict[str, Any]]:
    """
    Sorts a list of normalized media results using a specified field and direction.
    
    Args:
        results (List[Dict[str, Any]]): The list of normalized media data.
        sort_field (str): The field to sort by ('rating', 'title', 'type', 'created_at').
        direction (str): The sort direction ('asc' or 'desc').
        
    Returns:
        List[Dict[str, Any]]: The sorted list of media data.
    """
    sort_keys = {
        'rating': _rating_sort_key,
        'title': _title_sort_key,
        'type': _media_type_sort_key,
        'created_at': _created_sort_key
    }
    
    sort_key_func = sort_keys.get(sort_field, _created_sort_key)
    is_reverse = direction.lower() == 'desc'
    
    return sorted(results, key=sort_key_func, reverse=is_reverse)

def paginate_media_query(query: Union[Query, List], page: int, per_page: int = 20, allow_python_fallback: bool = False) -> Dict[str, Any]:
    """
    A unified pagination function for both SQLAlchemy queries and Python lists.
    
    Args:
        query (Union[Query, List]): The SQLAlchemy query or a list of items to paginate.
        page (int): The current page number (1-indexed).
        per_page (int, optional): The number of items per page. Defaults to 20.
        allow_python_fallback (bool, optional): Allow Python-level pagination for lists. Defaults to False.
        
    Returns:
        Dict[str, Any]: A dictionary containing pagination details and the items for the current page.
    """
    page = max(1, page)
    per_page = max(1, per_page)
    
    if isinstance(query, Query):
        # The count is performed on a subquery to ensure it's accurate with joins/groups.
        subquery = query.subquery()
        total = query.session.query(func.count(subquery.c.id)).scalar()
        
        items = query.limit(per_page).offset((page - 1) * per_page).all()

    elif isinstance(query, list):
        if not allow_python_fallback:
            raise TypeError("Received a list for pagination, but 'allow_python_fallback' is False.")
        
        total = len(query)
        if total > 100:
            warnings.warn(f"Python-level pagination used on a large dataset of {total} items.", UserWarning)
            logger.warning(f"Python-level pagination used on a large dataset of {total} items.")
        
        start = (page - 1) * per_page
        end = start + per_page
        items = query[start:end]
    else:
        raise TypeError(f"Unsupported type for pagination: {type(query)}")
        
    has_next = (page * per_page) < total
    has_prev = page > 1
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'has_next': has_next,
        'has_prev': has_prev,
        'pages': math.ceil(total / per_page) if total > 0 else 1
    }