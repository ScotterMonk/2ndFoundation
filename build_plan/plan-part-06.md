## Key Implementation Details

### Environment Configuration

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

### Embeddings Strategy

**Model Choice:**
- **Default:** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
  - Fast, runs locally, good balance
- **Alternative:** OpenAI `text-embedding-3-small` (1536 dimensions)
  - Better quality, requires API key, costs money

**Generation Timing:**
- On document upload (async processing)
- Cached in database `embedding` column
- Regenerate option in admin panel

### Code Execution Sandbox (for Grading)

**Security Requirements:**
```python
# app/core/grader.py

import ast
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    """Timeout context manager"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Execution exceeded {seconds}s")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def execute_model_code(code: str, test_query: str) -> List[Document]:
    """
    Safely execute model-generated hybrid_search implementation.
    
    Security measures:
    - AST parsing to detect malicious code
    - No file system access
    - No network access
    - Timeout enforcement
    - Limited imports
    """
    # Parse AST to check for dangerous operations
    tree = ast.parse(code)
    validator = CodeValidator()
    validator.visit(tree)
    
    if validator.security_issues:
        raise SecurityError(validator.security_issues)
    
    # Create restricted globals
    safe_globals = {
        '__builtins__': {
            'len': len,
            'sorted': sorted,
            'enumerate': enumerate,
            'zip': zip,
            'range': range,
            'sum': sum,
            'min': min,
            'max': max,
        },
        'List': List,
        'Tuple': Tuple,
        'Document': Document,
        '_vector_search': mock_vector_search,
        '_keyword_search': mock_keyword_search,
    }
    
    # Execute with timeout
    with timeout(30):
        exec(code, safe_globals)
        hybrid_search = safe_globals.get('hybrid_search')
        
        if not callable(hybrid_search):
            raise ValueError("hybrid_search function not found")
        
        return hybrid_search(test_query, limit=10)
```
