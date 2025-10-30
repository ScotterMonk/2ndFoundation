## Integration with Assignment Framework

### Dual Purpose Architecture

This Flask app serves two roles:

1. **Development Environment:** Build and test the RL task locally
2. **Demo Platform:** Show how the task works in a real application

### Extractable Components for Assignment Submission

The assignment framework needs these standalone files:

```
assignment_submission/
├── task.py              # Task definition (what models see)
├── grader.py            # Grading logic (evaluates model output)
├── test_data.sql        # Test database setup
└── README.md            # Documentation
```

**Critical Requirements:**
- Total: Under 300 lines combined
- No Flask dependencies in extracted files
- Runnable outside the web app
- Compatible with assignment's task runner

**Extraction Strategy:**
```python
# app/rl_task/task_definition.py → task.py
# - Contains task prompt text
# - Function signature
# - Requirements specification
# - NO Flask imports

# app/core/grader.py → grader.py  
# - Pure Python grading logic
# - Imports only: typing, json, dataclasses
# - No database connections (uses in-memory test data)

# app/rl_task/test_data.py → test_data.sql
# - SQL INSERT statements for 50 test documents
# - Pre-computed embeddings
# - Test query definitions
```
