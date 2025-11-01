## Task Definition Module

**`app/rl_task/task_definition.py`** (extracted to `task.py` for assignment)

```python
"""
RL Task Definition: Hybrid Search with Reciprocal Rank Fusion

This module defines the task that AI models will attempt to solve.
It should be extractable as a standalone file for the assignment framework.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TaskDefinition:
    """Complete task specification for AI models."""
    
    name: str = "Hybrid Search with RRF"
    version: str = "1.0"
    difficulty: str = "intermediate"
    
    description: str = """
    Application: "2nd Foundation" - A document retrieval system using pgVector for semantic search.
    
    Problem: Pure vector search sometimes misses exact keyword matches that users expect.
    For example, searching for "SELECT * FROM users" should find SQL code snippets,
    but semantic search might return conceptual database articles instead.
    
    Task: Implement a hybrid search function that combines semantic and keyword search
    using Reciprocal Rank Fusion (RRF).
    """
    
    requirements: str = """
    Function signature:
        def hybrid_search(query: str, limit: int = 10) -> List[Document]
    
    Available helper functions (pre-implemented):
        - _vector_search(query: str, limit: int) -> List[Tuple[Document, float]]
          Returns: [(doc, similarity_score), ...] ordered by similarity DESC
          
        - _keyword_search(query: str, limit: int) -> List[Tuple[Document, float]]
          Returns: [(doc, relevance_score), ...] ordered by relevance DESC
    
    Implementation requirements:
        1. Call both helper functions to get candidate results
        2. Apply RRF formula: score(d) = Σ(1 / (k + rank_i)) where k=60
           - rank_i is the 1-indexed position in each result list
           - Sum across all lists where document appears
        3. Merge results, handling duplicates correctly
        4. Return top 'limit' documents ordered by RRF score DESC
    
    Edge cases to handle:
        - Documents appearing in both result sets (merge RRF scores)
        - Documents appearing in only one result set
        - Empty results from one or both searches
        - Queries with no results at all
    """

def get_task_prompt() -> str:
    """
    Generate the complete task prompt that AI models will receive.
    """
    task = TaskDefinition()
    
    prompt = f"""
# {task.name} (Version {task.version})

## Description
{task.description}

## Requirements
{task.requirements}

## Evaluation Criteria

Your implementation will be tested on:

1. **Correctness (60%)**: Do the expected documents appear in the top-K results?
2. **Ranking Quality (30%)**: Is the RRF score calculated correctly?
3. **Edge Cases (10%)**: Does it handle unusual inputs gracefully?

## Common Failure Modes to Avoid

- Using wrong k value (e.g., k=1 or k=100)
- 0-indexed instead of 1-indexed ranks
- Not summing RRF scores for duplicates
- Crashes on empty results
- SQL injection vulnerabilities
"""
    
    return prompt
```
