## Reference Implementation

**`app/core/search.py`** (Production implementation)

```python
"""
Production hybrid search implementation.
This serves as the reference implementation for grading.
"""

from typing import List, Tuple, Dict
from sqlalchemy import func, text
from app.models import Document, db
import numpy as np

def _vector_search(query: str, limit: int = 50) -> List[Tuple[Document, float]]:
    """
    Perform vector similarity search using pgvector.
    
    Args:
        query: Search query string
        limit: Maximum number of results
        
    Returns:
        List of (Document, similarity_score) tuples, ordered by similarity DESC
    """
    from app.core.embeddings import generate_embedding
    
    # Generate query embedding
    query_embedding = generate_embedding(query)
    
    # Perform cosine similarity search
    results = db.session.query(
        Document,
        (1 - Document.embedding.cosine_distance(query_embedding)).label('similarity')
    ).filter(
        Document.embedding.isnot(None)
    ).order_by(
        text('similarity DESC')
    ).limit(limit).all()
    
    return [(doc, float(sim)) for doc, sim in results]

def _keyword_search(query: str, limit: int = 50) -> List[Tuple[Document, float]]:
    """
    Perform PostgreSQL full-text search.
    
    Args:
        query: Search query string
        limit: Maximum number of results
        
    Returns:
        List of (Document, relevance_score) tuples, ordered by relevance DESC
    """
    # Create tsquery from input
    tsquery = func.plainto_tsquery('english', query)
    
    # Perform full-text search
    results = db.session.query(
        Document,
        func.ts_rank(Document.ts_vector, tsquery).label('rank')
    ).filter(
        Document.ts_vector.op('@@')(tsquery)
    ).order_by(
        text('rank DESC')
    ).limit(limit).all()
    
    return [(doc, float(rank)) for doc, rank in results]

def hybrid_search(query: str, limit: int = 10) -> List[Document]:
    """
    Hybrid search using Reciprocal Rank Fusion (RRF).
    
    This is the reference implementation that models must replicate.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        
    Returns:
        List of Document objects, ordered by RRF score DESC
    """
    # Get results from both search methods
    vector_results = _vector_search(query, limit=50)
    keyword_results = _keyword_search(query, limit=50)
    
    # Calculate RRF scores
    k = 60  # Standard RRF constant
    rrf_scores: Dict[int, float] = {}
    
    # Process vector search results
    for rank, (doc, _) in enumerate(vector_results, start=1):
        rrf_scores[doc.id] = rrf_scores.get(doc.id, 0.0) + (1.0 / (k + rank))
    
    # Process keyword search results
    for rank, (doc, _) in enumerate(keyword_results, start=1):
        rrf_scores[doc.id] = rrf_scores.get(doc.id, 0.0) + (1.0 / (k + rank))
    
    # Sort by RRF score
    sorted_doc_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    
    # Fetch documents in order
    if not sorted_doc_ids:
        return []
    
    # Get documents maintaining order
    doc_map = {doc.id: doc for doc, _ in vector_results}
    doc_map.update({doc.id: doc for doc, _ in keyword_results})
    
    results = [doc_map[doc_id] for doc_id in sorted_doc_ids[:limit]]
    
    return results
```
