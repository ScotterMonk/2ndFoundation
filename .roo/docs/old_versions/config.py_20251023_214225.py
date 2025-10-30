"""
Configuration settings for the MediaShare Flask application.
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
    
    # TVDB Configuration
    TVDB_API_KEY = os.getenv('TVDB_API_KEY')
    TVDB_BASE_URL = 'https://api4.thetvdb.com/v4'
    TVDB_TIMEOUT = 15
    TVDB_TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'utils', 'api_tvdb', 'tvdb_token.json')
    
    # TMDB Configuration
    TMDB_API_READ_ACCESS_TOKEN = os.getenv('TMDB_API_READ_ACCESS_TOKEN')
    TMDB_API_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_TIMEOUT = 15
    
    # IMDB Configuration
    IMDB_API_KEY = os.getenv('IMDB_RAPIDAPI_KEY')
    IMDB_API_BASE_URL = 'https://imdb8.p.rapidapi.com'
    IMDB_TIMEOUT = 10
    
# Modified by glm-4.6 | 2025-10-22
    # Database Configuration
    # Use DATABASE_URL if provided, otherwise construct from individual components
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # Use the provided DATABASE_URL (could be SQLite for dev or PostgreSQL for prod)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to PostgreSQL configuration using environment variables
        DB_HOST = os.getenv('DB_HOST', '15.204.9.144')
        DB_PORT = os.getenv('DB_PORT', '5433')
        DB_NAME = os.getenv('DB_NAME', 'MediaShare')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'hG887lh2Kkf83qRE5bh')
        
        # Construct PostgreSQL connection URI
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
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
    # Modified by glm-4.6 | 2025-10-22
    UPLOAD_FOLDER = 'static/uploads/media'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
    MAX_FILE_SIZES_MB = {'video': 100, 'image': 10}
    ENABLE_THUMBNAILS = True
    ENABLE_METADATA_EXTRACTION = True
    ENABLE_IMDB = True
    ENABLE_TVDB = False  # Future use
    ENABLE_TMDB = False  # Future use
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    # Modified by glm-4.6 | 2025-10-22
    # Modified by glm-4.6 | 2025-10-22
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
    # Use the existing master database for testing
    DB_HOST = os.getenv('DB_HOST', '15.204.9.144')
    DB_PORT = os.getenv('DB_PORT', '5433')
    DB_NAME = os.getenv('DB_NAME', 'master')  # Use the existing database
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'fooblitsky')
    
    # Use TEST_DATABASE_URL if provided, otherwise construct PostgreSQL URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing

# Dictionary to map config names to config classes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
