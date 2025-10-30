## Testing Strategy

### Unit Tests

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

### Integration Tests

**`app/tests/test_grader.py`**
```python
import pytest
from app.core.grader import grade_submission, run_test_case
from app.models import TestCase

def test_grade_correct_submission(app, test_cases):
    """Test grading a correct implementation."""
    correct_code = """
def hybrid_search(query: str, limit: int = 10) -> List[Document]:
    vector_results = _vector_search(query, limit=50)
    keyword_results = _keyword_search(query, limit=50)
    
    k = 60
    rrf_scores = {}
    
    for rank, (doc, _) in enumerate(vector_results, start=1):
        rrf_scores[doc.id] = rrf_scores.get(doc.id, 0.0) + (1.0 / (k + rank))
    
    for rank, (doc, _) in enumerate(keyword_results, start=1):
        rrf_scores[doc.id] = rrf_scores.get(doc.id, 0.0) + (1.0 / (k + rank))
    
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    doc_map = {doc.id: doc for doc, _ in vector_results}
    doc_map.update({doc.id: doc for doc, _ in keyword_results})
    
    return [doc_map[doc_id] for doc_id in sorted_ids[:limit]]
"""
    
    with app.app_context():
        result = grade_submission(correct_code, test_cases)
        assert result['passed'] == True
        assert result['score'] >= 0.7

def test_grade_incorrect_k_value(app, test_cases):
    """Test grading detects wrong k value."""
    incorrect_code = """
def hybrid_search(query: str, limit: int = 10) -> List[Document]:
    k = 100  # Wrong k value!
    # ... rest of implementation
"""
    
    with app.app_context():
        result = grade_submission(incorrect_code, test_cases)
        assert result['score'] < 0.7
```
