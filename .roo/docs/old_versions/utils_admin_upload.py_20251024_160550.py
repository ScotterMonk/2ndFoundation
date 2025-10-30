# Created by Gemini 2.5 Pro | 2025-10-23
import logging
from flask import request  # dependency import as requested
from werkzeug.datastructures import FileStorage
from utils.database import db  # dependency import as requested
from models.models_user import User
from models.models_media import MediaType

logger = logging.getLogger(__name__)

def validate_upload_requirements(request, db_session, require_owner=True, require_media_type=True):
    """
    Validates essential requirements for media file uploads.

    Args:
        request: The Flask request object.
        db_session: The SQLAlchemy database session.
        require_owner (bool): If True, validates presence and existence of owner_user_id.
        require_media_type (bool): If True, validates presence and existence of media_type_id.

    Returns:
        dict: A dictionary containing:
              - 'valid' (bool): True if all validations pass, False otherwise.
              - 'owner' (User|None): The User object if valid and required, else None.
              - 'media_type' (MediaType|None): The MediaType object if valid and required, else None.
              - 'errors' (list): A list of error strings if validation fails.
    """
    # Created by GPT-5 | 2025-10-24
    valid = True
    owner = None
    media_type = None
    errors = []

    # Prefer querystring args, then form values
    owner_user_id_raw = request.args.get('owner_user_id') or request.form.get('owner_user_id')
    media_type_id_raw = request.args.get('media_type_id') or request.form.get('media_type_id')

    # Owner Validation
    if require_owner:
        if not owner_user_id_raw:
            errors.append('Missing required parameter: owner_user_id')
            valid = False
        else:
            try:
                owner_id = int(owner_user_id_raw)
                owner = db_session.query(User).filter_by(id=owner_id).first()
                if not owner:
                    errors.append('Owner not found')
                    valid = False
                elif getattr(owner, 'is_active', True) is False:
                    errors.append('Owner is inactive')
                    valid = False
            except (ValueError, TypeError):
                errors.append('Invalid owner_user_id')
                valid = False

    # Media Type Validation
    if require_media_type:
        if not media_type_id_raw:
            errors.append('Missing required parameter: media_type_id')
            valid = False
        else:
            try:
                mtype_id = int(media_type_id_raw)
                media_type = db_session.query(MediaType).filter_by(id=mtype_id).first()
                if not media_type:
                    errors.append('Media type not found')
                    valid = False
            except (ValueError, TypeError):
                errors.append('Invalid media_type_id')
                valid = False

    return {
        'valid': valid,
        'owner': owner,
        'media_type': media_type,
        'errors': errors
    }

def extract_uploaded_files(request, file_field='file') -> list[FileStorage]:
    # Created by gpt-5-2025-08-07 | 2025-10-24
    """
    Extracts valid uploaded files from the Flask request object.

    Args:
        request: The Flask request object.
        file_field (str): The name of the file input field in the form.

    Returns:
        list[FileStorage]: A list of valid FileStorage objects that were uploaded.
    """
    uploaded_files = request.files.getlist(file_field)
    return [f for f in uploaded_files if f and f.filename]

def prepare_media_record_data(file_info, owner, media_type, admin_user):
    """
    Builds a dictionary of Media model fields from the result of MediaFileHandler.

    Args:
        file_info (dict): The data dictionary from a successful CoreResult.
        owner (User): The owner of the media.
        media_type (MediaType): The media type.
        admin_user (User): The admin performing the upload.

    Returns:
        A dictionary of data ready for the Media model constructor.
    """
    # Modified by Claude Sonnet 4.5 | 2025-10-23
    # Fixed field names to match Media model database columns
    return {
        'title': file_info.get('title_from_filename', 'Untitled'),
        'filename_stored': file_info.get('filename_secure'),  # Fixed: was 'filename'
        'filename_original': file_info.get('filename_original'),
        'file_path': file_info.get('relative_path'),
        'file_size_bytes': file_info.get('size_bytes'),  # Fixed: was 'file_size'
        'mime_type': file_info.get('mime_type', 'application/octet-stream'),  # Added: required field
        'thumbnail_path': file_info.get('thumbnail_relative_path'),
        'media_type_id': media_type.id,
        'users_id': owner.id,  # Fixed: was 'owner_user_id'
        'created_by': admin_user.id,  # Fixed: was 'created_by_user_id'
        'is_public': False,  # Default to private
        'is_featured': False,  # Default to not featured
        'is_processed': True,  # Fixed: was 'processed'
        'processing_status': 'completed',  # Added: for consistency
        'download_count': 0,  # Added: required field
        'view_count': 0,  # Added: required field
        'like_count': 0,  # Added: required field
        'credit_cost': 0,  # Added: required field
        'adult': False,  # Added: required field
        'min_age': 0  # Added: required field
    }