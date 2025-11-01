## Unit Tests

**`app/tests/test_search.py`**
```python
import pytest
from app.core.search import hybrid_search, _vector_search, _keyword_search
from app.models import Document, db

def test_vector_search(app, test_documents):
    """Test vector search returns relevant results."""
    with app.app_context():
        results = _vector_search("neural networks", limit=5)
        assert len(results) > 0
        assert all(isinstance(doc, Document) for doc, _ in results)

def test_keyword_search(app, test_documents):
    """Test keyword search returns relevant results."""
    with app.app_context():
        results = _keyword_search("SELECT FROM users", limit=5)
        assert len(results) > 0
        
def test_hybrid_search_basic(app, test_documents):
    """Test hybrid search combines both methods."""
    with app.app_context():
        results = hybrid_search("python function", limit=10)
        assert len(results) > 0
        assert len(results) <= 10

def test_hybrid_search_empty_query(app):
    """Test hybrid search handles empty queries."""
    with app.app_context():
        results = hybrid_search("", limit=10)
        assert results == []
```
