## Test Data Generation

**`app/rl_task/test_data.py`** (generates `test_data.sql`)

```python
from typing import List, Dict
import json

def generate_test_documents() -> List[Dict]:
    """
    Generate 50 test documents across categories.
    
    Categories:
    - code_snippets: 15 docs with exact code
    - ml_concepts: 15 docs about ML/AI
    - general_knowledge: 10 docs mixed content
    - edge_cases: 10 docs testing boundaries
    """
    documents = []
    
    # Code snippets (keyword-heavy)
    code_docs = [
        {
            'title': 'SQL User Query',
            'content': 'SELECT * FROM users WHERE id = 1;',
            'category': 'code_snippets'
        },
        {
            'title': 'Python Average Function',
            'content': 'def calculate_average(numbers):\n    return sum(numbers) / len(numbers)',
            'category': 'code_snippets'
        },
        # ... 13 more
    ]
    
    # ML concepts (semantic-heavy)
    ml_docs = [
        {
            'title': 'Neural Network Basics',
            'content': 'Neural networks learn by adjusting weights through backpropagation...',
            'category': 'ml_concepts'
        },
        # ... 14 more
    ]
    
    # Generate with embeddings
    for doc in code_docs + ml_docs:
        doc['embedding'] = generate_embedding(doc['content'])
    
    return documents

def generate_test_queries() -> List[Dict]:
    """
    Generate test queries with expected results.
    """
    return [
        {
            'query': 'SELECT * FROM users WHERE',
            'expected_top_3': [1, 5, 12],
            'category': 'keyword_heavy',
            'description': 'Should find exact SQL syntax matches'
        },
        {
            'query': 'how do neural networks learn',
            'expected_top_3': [16, 23, 31],
            'category': 'semantic_heavy',
            'description': 'Requires conceptual understanding'
        },
        {
            'query': 'python function to calculate average',
            'expected_top_3': [2, 8, 19],
            'category': 'hybrid_strength',
            'description': 'Benefits from both keyword and semantic'
        },
        # ... 7 more test cases
    ]

def export_to_sql() -> str:
    """
    Export test data as SQL INSERT statements for assignment submission.
    """
    docs = generate_test_documents()
    sql_statements = []
    
    for i, doc in enumerate(docs, 1):
        sql = f"""
        INSERT INTO documents (id, title, content, category, embedding) VALUES (
            {i},
            '{doc['title']}',
            '{doc['content']}',
            '{doc['category']}',
            '{doc['embedding']}'
        );
        """
        sql_statements.append(sql)
    
    return '\n'.join(sql_statements)
```
