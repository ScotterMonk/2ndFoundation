## Proposed Database Schema
PostgreSQL only (never SQLite) on port 5433
See `.env` file for db credentials.
Source of truth hierarchy: 1) Live PGDB → 2) `models/models_*.py` → 3) `database_schema.md`

```python
# app/models.py

from flask_sqlalchemy import SQLAlchemy
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime

db = SQLAlchemy()

class Document(db.Model):
    """Documents in the RAG system"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(1000))
    
    # For semantic search
    embedding = db.Column(Vector(384))  # sentence-transformers dimension
    
    # For keyword search
    ts_vector = db.Column(TSVECTOR)
    
    # Metadata
    category = db.Column(db.String(100))  # 'code', 'ml_concept', 'general', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Full-text search index
    __table_args__ = (
        db.Index('idx_ts_vector', ts_vector, postgresql_using='gin'),
        db.Index('idx_embedding', embedding, postgresql_using='ivfflat'),
    )

class SearchQuery(db.Model):
    """Track search queries for analytics"""
    __tablename__ = 'search_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(1000), nullable=False)
    results_count = db.Column(db.Integer)
    execution_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ModelSubmission(db.Model):
    """Track model-generated code submissions"""
    __tablename__ = 'model_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100))  # 'claude-sonnet-4', 'gpt-4', etc.
    code = db.Column(db.Text, nullable=False)
    
    # Grading results
    score = db.Column(db.Float)
    passed = db.Column(db.Boolean)
    test_results = db.Column(db.JSON)
    execution_time = db.Column(db.Float)
    
    # Security analysis
    security_issues = db.Column(db.JSON)  # SQL injection attempts, etc.
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestCase(db.Model):
    """Predefined test cases for grading"""
    __tablename__ = 'test_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(1000), nullable=False)
    expected_docs = db.Column(db.JSON)      # List[int] - document IDs
    expected_order = db.Column(db.JSON)     # List[int] - ranked order
    category = db.Column(db.String(100))    # 'keyword_heavy', 'semantic', 'hybrid'
    description = db.Column(db.Text)        # Why this test matters

class User(db.Model):
    """Users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60), nullable=False)
    pw_hashed = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.Text, nullable=False) # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```
