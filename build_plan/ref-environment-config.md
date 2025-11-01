## Environment Configuration

**`.env.example`**
```bash
# Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/second_foundation
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/second_foundation_test

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
# Optional: OPENAI_API_KEY=sk-... for OpenAI embeddings

# RL Task Assignment
ANTHROPIC_API_KEY=sk-ant-...  # For testing with Claude models
GRADER_TIMEOUT=30             # Seconds per test case
MAX_CODE_LENGTH=10000         # Characters
```

**`app/config.py`**
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # RL Task settings
    GRADER_TIMEOUT = int(os.environ.get('GRADER_TIMEOUT', 30))
    MAX_CODE_LENGTH = int(os.environ.get('MAX_CODE_LENGTH', 10000))

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```
