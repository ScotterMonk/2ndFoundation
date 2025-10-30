"""
Media & Content models.
"""

from datetime import datetime
from utils.database import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case, cast, Integer, Numeric, and_, func

class MediaType(db.Model):
    __tablename__ = 'media_types'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    allowed_extensions = db.Column(db.ARRAY(db.String), nullable=True)
    max_file_size_mb = db.Column(db.Integer, nullable=True)
    requires_processing = db.Column(db.Boolean, nullable=False)
    credit_cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # All media items of this type
    media_items = db.relationship('Media', back_populates='media_type')

class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True, index=True)
    name = db.Column(db.String(50), nullable=False)
    native_name = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Subtitles in this language
    subtitles = db.relationship('MediaSubtitle', back_populates='language')

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Association to media items
    media_genres = db.relationship('MediaGenre', back_populates='genre')

class MediaCategory(db.Model):
    __tablename__ = 'media_categories'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('media_categories.id'), nullable=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False)
    sort_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Self-referential for hierarchical categories
    parent_category = db.relationship('MediaCategory', remote_side=[id], backref='sub_categories', foreign_keys=[parent_id])
    # Assigned media items
    assignments = db.relationship('MediaCategoryAssignment', back_populates='category')

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    media_type_id = db.Column(db.Integer, db.ForeignKey('media_types.id'), nullable=False, index=True)
    title = db.Column(db.String, nullable=False)
    title_alternate = db.Column(db.String, nullable=True)
    title_for_sorting = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    imdb_id = db.Column(db.String, nullable=True)
    imdb_rating = db.Column(db.Numeric, nullable=True)
    tmdb_id = db.Column(db.Integer, nullable=True)
    tmdb_rating = db.Column(db.Numeric, nullable=True)
    tmdb_media_type = db.Column(db.String, nullable=True)
    tvdb_id = db.Column(db.Integer, nullable=True)
    tvdb_rating = db.Column(db.Numeric, nullable=True)
    other_id = db.Column(db.Integer, nullable=True)
    other_rating = db.Column(db.Numeric, nullable=True)
    user_score = db.Column(db.Numeric, nullable=True)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=True, index=True)
    resolution = db.Column(db.String, nullable=True)
    filename_original = db.Column(db.String, nullable=False)
    filename_stored = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    file_size_bytes = db.Column(db.BigInteger, nullable=False)
    mime_type = db.Column(db.String, nullable=False)
    file_hash = db.Column(db.String, nullable=True)
    thumbnail_path = db.Column(db.String, nullable=True)
    preview_path = db.Column(db.String, nullable=True)
    media_metadata = db.Column('metadata', db.JSON, nullable=True)
    tags = db.Column(db.String, nullable=True)
    is_public = db.Column(db.Boolean, nullable=False)
    is_featured = db.Column(db.Boolean, nullable=False)
    is_processed = db.Column(db.Boolean, nullable=False)
    processing_status = db.Column(db.String, nullable=False)
    download_count = db.Column(db.Integer, nullable=False)
    view_count = db.Column(db.Integer, nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
    credit_cost = db.Column(db.Integer, nullable=False)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    added_date = db.Column(db.DateTime(timezone=True), nullable=True)
    backdrop_path = db.Column(db.String, nullable=True)
    content_id = db.Column(db.Integer, nullable=True)
    content_type = db.Column(db.String, nullable=True)
    last_episode_air_date = db.Column(db.DateTime(timezone=True), nullable=True)
    name = db.Column(db.String, nullable=True)
    original_language = db.Column(db.String, nullable=True)
    original_name = db.Column(db.String, nullable=True)
    overview = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime(timezone=True), nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String, nullable=True)
    still_path = db.Column(db.String, nullable=True)
    tagline = db.Column(db.String, nullable=True)
    total_episodes = db.Column(db.Integer, nullable=True)
    total_seasons = db.Column(db.Integer, nullable=True)
    trailer_id = db.Column(db.String, nullable=True)
    vote_average = db.Column(db.Float, nullable=True)
    vote_count = db.Column(db.Integer, nullable=True)
    trailer_url = db.Column(db.String, nullable=True)
    video_trailer_file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=True)
    genre = db.Column(db.String, nullable=True)
    adult = db.Column(db.Boolean, nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships to other content models
    media_type = db.relationship('MediaType', back_populates='media_items')
    episodes = db.relationship('Episode', back_populates='media', cascade='all, delete-orphan')
    files = db.relationship('File', back_populates='media', foreign_keys='File.media_id', cascade='all, delete-orphan')
    subtitles = db.relationship('MediaSubtitle', back_populates='media', cascade='all, delete-orphan')
    categories = db.relationship('MediaCategoryAssignment', back_populates='media', cascade='all, delete-orphan')
    genres = db.relationship('MediaGenre', back_populates='media', cascade='all, delete-orphan')
    director = db.relationship('Director', back_populates='media_items')
    @hybrid_property
    def user_rating_100(self):
        """
        Aggregated average rating across available sources normalized to 0-100.
        Sources: imdb_rating (0-100), user_score (0-100).
        Ignores null/empty values. Returns integer 0-100 or None.
        """
        values = []
        # IMDb already 0-100
        if self.imdb_rating is not None:
            try:
                values.append(float(self.imdb_rating))
            except (TypeError, ValueError):
                pass
        # User score (0-100) stored as string in this model
        if self.user_score is not None and self.user_score != '':
            try:
                values.append(float(self.user_score))
            except (TypeError, ValueError):
                pass
        if not values:
            return None
        avg = sum(values) / len(values)
        try:
            return int(round(avg))
        except Exception:
            return None

    @user_rating_100.expression
    def user_rating_100(cls):
        imdb_scaled = case((cls.imdb_rating != None, cast(cls.imdb_rating, Numeric)), else_=None)
        user = case((cls.user_score != None, cast(cls.user_score, Numeric)), else_=None)

        count_non_null = (
            case((cls.imdb_rating != None, 1), else_=0) +
            case((cls.user_score != None, 1), else_=0)
        )

        sum_vals = func.coalesce(imdb_scaled, 0) + func.coalesce(user, 0)

        avg_numeric = case(
            (count_non_null != 0, sum_vals / cast(count_non_null, Numeric)),
            else_=None
        )

        return cast(func.round(avg_numeric), Integer)
    content_reports = db.relationship('ContentReport', back_populates='media', cascade='all, delete-orphan')

class Episode(db.Model):
    __tablename__ = 'episodes'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False, index=True)
    episode_number = db.Column(db.Integer, nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime(timezone=True), nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    thumbnail_url = db.Column(db.String, nullable=True)
    video_url = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)

    # Back to parent media
    media = db.relationship('Media', back_populates='episodes')

class MediaQualityLevel(db.Model):
    __tablename__ = 'media_quality_levels'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False, index=True)
    quality_level = db.Column(db.String, nullable=False)
    video_url = db.Column(db.String, nullable=True)
    file_size_mb = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)

    # Files available at this quality
    media = db.relationship('Media', backref=db.backref('quality_levels', cascade='all, delete-orphan'))

class MediaGenre(db.Model):
    __tablename__ = 'media_genres'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False, index=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, nullable=True)

    # Association relationships
    media = db.relationship('Media', back_populates='genres')
    genre = db.relationship('Genre', back_populates='media_genres')

class MediaSubtitle(db.Model):
    __tablename__ = 'media_subtitles'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False, index=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False, index=True)
    subtitle_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)

    # Back to media and language
    media = db.relationship('Media', back_populates='subtitles')
    language = db.relationship('Language', back_populates='subtitles')

class MediaCategoryAssignment(db.Model):
    __tablename__ = 'media_categories_assignments'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('media_categories.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, nullable=True)

    # Assignment relationships
    media = db.relationship('Media', back_populates='categories')
    category = db.relationship('MediaCategory', back_populates='assignments')

class ContentReport(db.Model):
    __tablename__ = 'content_reports'
    id = db.Column(db.Integer, primary_key=True)
    reported_by_users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False, index=True)
    report_type = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String, nullable=False, default='pending', index=True)
    admin_notes = db.Column(db.Text, nullable=True)
    resolved_by_users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    resolved_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)

    # Relationship back to media and reporting user
    media = db.relationship('Media', back_populates='content_reports')
    reported_by_user = db.relationship('User', foreign_keys=[reported_by_users_id], backref='reported_content')
    resolved_by_user = db.relationship('User', foreign_keys=[resolved_by_users_id], backref='resolved_content_reports')


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    file_size_bytes = db.Column(db.BigInteger, nullable=False)
    file_type = db.Column(db.String, nullable=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True, index=True)
    uploaded_by_users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    uploaded_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    checksum = db.Column(db.String, nullable=True)
    file_metadata = db.Column(db.JSON, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)

    # Back to media and quality level
    media = db.relationship('Media', back_populates='files', foreign_keys='File.media_id')
    uploaded_by_user = db.relationship('User', backref=db.backref('uploaded_files', cascade='all, delete-orphan'))

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)
    profile_path = db.Column(db.String, nullable=True)
    tmdb_id = db.Column(db.Integer, nullable=True)
    imdb_id = db.Column(db.String, nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)

    # Back-reference to media items
    media_items = db.relationship('Media', back_populates='director')

class MediaPerformer(db.Model):
    __tablename__ = 'media_performers'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False, index=True)
    performer_id = db.Column(db.Integer, db.ForeignKey('performers.id'), nullable=False, index=True)
    character_name = db.Column(db.String, nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)

class Performer(db.Model):
    __tablename__ = 'performers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    imdb_cast_id = db.Column(db.String, nullable=True)
    profile_path = db.Column(db.String, nullable=True)
    tmdb_id = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
