# Project Plan: "2nd Foundation" + RL Task

## Understanding the RL Task Flow

**The Actual Workflow:**
1. **User** → Create RL task definition + grading function
2. **Assignment Framework** → Runs Claude/GPT against your task (10+ times)
3. **AI Models (LLMs)** → Attempt to implement `hybrid_search()`
4. **Grader** → Evaluates each model-generated implementation
5. **Results** → Used to train future AI models via reinforcement learning

**Key Point:** This guide is NOT for human students. AI models will read the task prompt, generate code, and be graded automatically. Your job is to create a challenging but fair task that tests real capabilities.

## The RL Task: Hybrid Search with RRF

### What the Model Receives (Task Prompt)

```
Application: "2nd Foundation" - A document retrieval system using pgVector for semantic search.

Problem: Pure vector search sometimes misses exact keyword matches that users expect.

Task: Implement a hybrid search function that combines semantic and keyword search using Reciprocal Rank Fusion (RRF).

Function signature:
def hybrid_search(query: str, limit: int = 10) -> List[Document]

Available helper functions (pre-implemented):
- _vector_search(query: str, limit: int) -> List[Tuple[Document, float]]
  Returns: [(doc, similarity_score), ...] ordered by similarity DESC
  
- _keyword_search(query: str, limit: int) -> List[Tuple[Document, float]]
  Returns: [(doc, relevance_score), ...] ordered by relevance DESC

Requirements:
1. Call both helper functions to get candidate results
2. Apply RRF formula: score(d) = Σ(1 / (k + rank_i)) where k=60
   - rank_i is 1-indexed position in each result list
   - Sum across all lists where document appears
3. Merge results, handling duplicates correctly
4. Return top 'limit' documents ordered by RRF score DESC

Edge cases to handle:
- Documents appearing in both result sets (merge RRF scores)
- Documents appearing in only one result set
- Empty results from one or both searches
- Queries with no results at all
```

### Verification Approach

**Test Database:** ~50 carefully chosen documents across categories:
- **Code Snippets (15):** Exact matches needed (SQL queries, Python functions)
- **ML/AI Concepts (15):** Semantic understanding required (research summaries)
- **General Knowledge (10):** Mixed retrieval strategies work best
- **Edge Cases (10):** Short/long documents, special characters

**Test Queries:** Each designed to expose specific failure modes
```json
[
  {
    "query": "SELECT * FROM users WHERE",
    "category": "keyword_heavy",
    "expected_top_3": [5, 12, 23],
    "why": "Pure semantic search fails on exact syntax"
  },
  {
    "query": "how do neural networks learn",
    "category": "semantic_heavy", 
    "expected_top_3": [8, 15, 31],
    "why": "Pure keyword search misses conceptual similarity"
  },
  {
    "query": "python function to calculate average",
    "category": "hybrid_strength",
    "expected_top_3": [3, 19, 27],
    "why": "Needs both keywords and semantic understanding"
  }
]
```

### Expected Model Failure Modes

The grader should catch these common LLM mistakes:
1. **Incorrect RRF math** - Wrong k value, off-by-one rank errors
2. **Duplicate handling bugs** - Same document counted multiple times
3. **Formula misunderstanding** - Inverting scores, wrong aggregation
4. **Edge case failures** - Crashes on empty results
5. **Security issues** - SQL injection vulnerabilities (bonus penalty)
6. **Type errors** - Returning wrong data structure

### Grading Criteria

**Scoring Breakdown:**
- **Correctness (60%):** Expected documents appear in top-K results
- **Ranking Quality (30%):** Proper RRF scores maintain correct order
- **Edge Cases (10%):** Handles empty results, duplicates, single docs

**Grader Output Format:**
```python
{
    'passed': bool,           # True if score >= 0.7
    'score': float,           # 0.0 to 1.0
    'details': {
        'test_cases': [
            {
                'query': str,
                'passed': bool,
                'expected_docs': List[int],
                'actual_docs': List[int],
                'expected_order': List[int],
                'actual_order': List[int],
                'error': str or None
            }
        ],
        'execution_error': str or None,
        'security_issues': List[str]  # SQL injection attempts, etc.
    },
    'execution_time': float
}
```
