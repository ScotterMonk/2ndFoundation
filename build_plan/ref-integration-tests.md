## Integration Tests

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
