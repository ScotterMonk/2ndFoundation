"""
Configuration settings for the "2nd Foundation" Flask application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    # Secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    
    # Instance Path
    INSTANCE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    
    # Database Configuration - always sourced from .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before use
        'pool_recycle': 300,    # Recycle connections every 5 minutes
        'echo': False           # Set to True for SQL query logging in development
    }
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Media Pipeline Settings
    MEDIA_UPLOAD_FOLDER = os.path.join('static', 'uploads', 'media')
    MEDIA_ALLOWED_EXTENSIONS = {
        'video': {'mp4', 'mov', 'avi', 'mkv'}, 
        'audio': {'mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg', 'wma', 'aiff', 'ape', 'opus', 'alac'},
        'image': {'png', 'jpg', 'jpeg', 'gif'}, 
        'documents': {'pdf', 'doc', 'docx', 'odt', 'rtf'},
        'spreadsheets': {'xls', 'ods'},
        'ebooks': {'mobi', 'epub', 'opf'},
        'code': {'py', 'js', 'html', 'xml', 'json'},
        'text': {'txt', 'md'}}
    MEDIA_MAX_FILE_SIZES_MB = {'video': 40000, 'image': 10000}
    MEDIA_ENABLE_THUMBNAILS = True
    MEDIA_ENABLE_METADATA = True
    MEDIA_ENABLE_IMDB = True
    MEDIA_ENABLE_TVDB = False  # Future use
    MEDIA_ENABLE_TMDB = False  # Future use
    MAX_CONTENT_LENGTH = 10000 * 1024 * 1024  # 10000MB
    MEDIA_USE_NEW_HANDLER = False  # Feature flag to control media handler

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # Enable SQL query logging in development
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'echo': False  # Show SQL queries in development
    }

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Database configuration inherited from Config class (uses .env values)
    # Use TEST_DATABASE_URL if provided, otherwise inherit from parent Config
    if os.getenv('TEST_DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    # If no TEST_DATABASE_URL, the SQLALCHEMY_DATABASE_URI from Config will be used
    
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing

# Dictionary to map config names to config classes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
