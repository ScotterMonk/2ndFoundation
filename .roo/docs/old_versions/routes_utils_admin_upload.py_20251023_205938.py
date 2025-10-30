# Created by Gemini 2.5 Pro | 2025-10-23
import logging
from models.models_user import User
from models.models_media import MediaType

logger = logging.getLogger(__name__)

def validate_upload_requirements(request, db_session, require_owner=True, require_media_type=True):
    """
    Extracts and validates owner and media type from the request for media uploads.

    Args:
        request: The Flask request object.
        db_session: The SQLAlchemy session.
        require_owner (bool): Whether to require a valid owner.
        require_media_type (bool): Whether to require a valid media type.

    Returns:
        A dictionary containing: {valid, owner, media_type, errors}
    """
    errors = []
    owner = None
    media_type = None

    owner_user_id = request.form.get('owner_user_id')
    media_type_id = request.form.get('media_type_id')

    # Validate Owner
    if require_owner:
        if not owner_user_id:
            errors.append('An owner must be selected.')
        else:
            try:
                owner_id = int(owner_user_id)
                owner = db_session.query(User).filter_by(id=owner_id).first()
                if not owner:
                    errors.append('Selected owner does not exist.')
                elif not owner.is_active:
                    errors.append('Selected owner is not an active user.')
            except (ValueError, TypeError):
                errors.append('Invalid owner ID specified.')

    # Validate Media Type
    if require_media_type:
        if not media_type_id:
            errors.append('A media type must be selected.')
        else:
            try:
                mtype_id = int(media_type_id)
                media_type = db_session.query(MediaType).filter_by(id=mtype_id).first()
                if not media_type:
                    errors.append('Selected media type does not exist.')
            except (ValueError, TypeError):
                errors.append('Invalid media type ID specified.')
    
    return {
        'valid': not errors,
        'owner': owner,
        'media_type': media_type,
        'errors': errors
    }

def extract_uploaded_files(request, file_field='file'):
    """
    Extracts valid FileStorage objects from a multi-file upload request.

    Args:
        request: The Flask request object.
        file_field (str): The name of the file input field.

    Returns:
        A list of valid FileStorage objects.
    """
    uploaded_files = request.files.getlist(file_field)
    # Filter out empty file entries that can be submitted
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
    return {
        'title': file_info.get('title_from_filename', 'Untitled'),
        'filename': file_info.get('filename_secure'),
        'filename_original': file_info.get('filename_original'),
        'file_path': file_info.get('relative_path'),
        'file_size': file_info.get('size_bytes'),
        'thumbnail_path': file_info.get('thumbnail_relative_path'),
        'media_type_id': media_type.id,
        'owner_user_id': owner.id,
        'created_by_user_id': admin_user.id,
        'is_public': False,  # Default to private
        'is_featured': False, # Default to not featured
        'processed': True,
        'rating': file_info.get('metadata', {}).get('rating', 0.0),
        'summary': file_info.get('metadata', {}).get('summary', '')
    }