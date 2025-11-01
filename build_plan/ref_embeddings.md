## Embeddings Module

**`app/core/embeddings.py`**

```python
"""
Vector embeddings generation for semantic search.

This module provides functions to generate embeddings from text using
sentence-transformers. Embeddings are cached to avoid redundant computations.
"""

from typing import List, Optional
import numpy as np
from functools import lru_cache
import os

# Global embedding model instance
_model = None

def get_embedding_model():
    """
    Get or create the sentence-transformer model instance.
    
    Returns:
        SentenceTransformer model instance
    """
    global _model
    
    if _model is None:
        from sentence_transformers import SentenceTransformer
        
        # Get model name from environment or use default
        model_name = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
        
        # Load model (will download on first use)
        _model = SentenceTransformer(model_name)
        print(f"Loaded embedding model: {model_name}")
    
    return _model

def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a single text string.
    
    Args:
        text: Input text to embed
        
    Returns:
        List of floats representing the embedding vector (384 dimensions for MiniLM)
        
    Examples:
        >>> embedding = generate_embedding("Hello world")
        >>> len(embedding)
        384
    """
    if not text or not text.strip():
        # Return zero vector for empty text
        return [0.0] * 384
    
    model = get_embedding_model()
    
    # Generate embedding
    embedding = model.encode(text, convert_to_numpy=True)
    
    # Convert to list and return
    return embedding.tolist()

def generate_embeddings_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently.
    
    Args:
        texts: List of text strings to embed
        batch_size: Number of texts to process at once
        
    Returns:
        List of embedding vectors
        
    Examples:
        >>> texts = ["First document", "Second document", "Third document"]
        >>> embeddings = generate_embeddings_batch(texts)
        >>> len(embeddings)
        3
    """
    if not texts:
        return []
    
    model = get_embedding_model()
    
    # Filter out empty texts and track indices
    valid_texts = []
    valid_indices = []
    for i, text in enumerate(texts):
        if text and text.strip():
            valid_texts.append(text)
            valid_indices.append(i)
    
    # Generate embeddings for valid texts
    if valid_texts:
        embeddings = model.encode(
            valid_texts,
            batch_size=batch_size,
            show_progress_bar=len(valid_texts) > 100,
            convert_to_numpy=True
        )
    else:
        embeddings = []
    
    # Build result array with zero vectors for empty texts
    result = []
    zero_vector = [0.0] * 384
    valid_idx = 0
    
    for i in range(len(texts)):
        if i in valid_indices:
            result.append(embeddings[valid_idx].tolist())
            valid_idx += 1
        else:
            result.append(zero_vector)
    
    return result

@lru_cache(maxsize=1000)
def generate_embedding_cached(text: str) -> tuple:
    """
    Generate embedding with LRU caching for frequently used queries.
    
    Args:
        text: Input text to embed
        
    Returns:
        Tuple of floats (hashable for caching)
        
    Note:
        Returns tuple instead of list because cache requires hashable types.
        Convert back to list when needed: list(generate_embedding_cached(text))
    """
    embedding = generate_embedding(text)
    return tuple(embedding)

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First embedding vector
        vec2: Second embedding vector
        
    Returns:
        Similarity score between -1 and 1 (higher is more similar)
        
    Examples:
        >>> vec1 = generate_embedding("machine learning")
        >>> vec2 = generate_embedding("artificial intelligence")
        >>> similarity = cosine_similarity(vec1, vec2)
        >>> 0.5 < similarity < 1.0
        True
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    # Compute cosine similarity
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))

def get_embedding_dimension() -> int:
    """
    Get the dimension of embeddings produced by the model.
    
    Returns:
        Integer dimension (384 for all-MiniLM-L6-v2)
    """
    model = get_embedding_model()
    return model.get_sentence_embedding_dimension()

def clear_embedding_cache():
    """
    Clear the LRU cache of embeddings.
    
    Useful when memory is constrained or for testing.
    """
    generate_embedding_cached.cache_clear()
    print("Embedding cache cleared")

# Warmup: Generate a dummy embedding on module load to initialize model
# This prevents first-query slowness in production
def _warmup():
    """Warm up the model by generating a test embedding."""
    try:
        _ = generate_embedding("warmup text")
    except Exception as e:
        print(f"Warning: Could not warm up embedding model: {e}")

# Comment out warmup in development to speed up app startup
# _warmup()
```

## Usage Examples

### 1. Single Document Embedding
```python
from app.core.embeddings import generate_embedding

text = "Machine learning is a subset of artificial intelligence"
embedding = generate_embedding(text)
print(f"Generated {len(embedding)}-dimensional vector")
```

### 2. Batch Processing for Upload
```python
from app.core.embeddings import generate_embeddings_batch
from app.models import Document, db

# Process multiple documents efficiently
documents = Document.query.filter(Document.embedding.is_(None)).limit(100).all()
texts = [doc.content for doc in documents]

embeddings = generate_embeddings_batch(texts, batch_size=32)

for doc, embedding in zip(documents, embeddings):
    doc.embedding = embedding

db.session.commit()
```

### 3. Query Embedding with Cache
```python
from app.core.embeddings import generate_embedding_cached

# Frequently used queries benefit from caching
query = "SELECT * FROM users"
embedding = list(generate_embedding_cached(query))
```

### 4. Similarity Comparison
```python
from app.core.embeddings import generate_embedding, cosine_similarity

text1 = "Python programming language"
text2 = "Java programming language"
text3 = "Apple fruit nutrition"

emb1 = generate_embedding(text1)
emb2 = generate_embedding(text2)
emb3 = generate_embedding(text3)

print(f"Python vs Java: {cosine_similarity(emb1, emb2):.3f}")     # High similarity
print(f"Python vs Apple: {cosine_similarity(emb1, emb3):.3f}")    # Low similarity
```

## Integration with Document Model

**`app/core/upload.py`** (Example usage)

```python
from app.core.embeddings import generate_embedding
from app.models import Document, db

def process_document(title: str, content: str, category: str = 'general'):
    """
    Process and store a document with its embedding.
    
    Args:
        title: Document title
        content: Document text content
        category: Document category
        
    Returns:
        Created Document instance
    """
    # Generate embedding for semantic search
    embedding = generate_embedding(content)
    
    # Create document
    doc = Document(
        title=title,
        content=content,
        category=category,
        embedding=embedding
    )
    
    db.session.add(doc)
    db.session.commit()
    
    return doc
```

## Model Selection

The default model `all-MiniLM-L6-v2` is chosen because:
- **Small size**: ~80MB, loads quickly
- **Fast inference**: ~100ms per document on CPU
- **Good quality**: Competitive performance for retrieval tasks
- **384 dimensions**: Balances expressiveness and efficiency

Alternative models can be configured via environment variable:
```bash
# Higher quality but slower
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

# Multilingual support
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

## Performance Considerations

1. **Batch Processing**: Always use `generate_embeddings_batch()` for multiple documents
2. **Caching**: Query embeddings are cached with LRU to avoid recomputation
3. **Lazy Loading**: Model loads on first use, not at import time
4. **Memory Management**: Cache can be cleared with `clear_embedding_cache()`

## Dependencies

Required in `requirements.txt`:
```
sentence-transformers>=2.2.0
torch>=2.0.0
numpy>=1.24.0
```
