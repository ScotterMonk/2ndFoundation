## Code Execution Sandbox (for Grading)

**Security Requirements:**
```python
# app/core/grader.py

import ast
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    """Timeout context manager"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Execution exceeded {seconds}s")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def execute_model_code(code: str, test_query: str) -> List[Document]:
    """
    Safely execute model-generated hybrid_search implementation.
    
    Security measures:
    - AST parsing to detect malicious code
    - No file system access
    - No network access
    - Timeout enforcement
    - Limited imports
    """
    # Parse AST to check for dangerous operations
    tree = ast.parse(code)
    validator = CodeValidator()
    validator.visit(tree)
    
    if validator.security_issues:
        raise SecurityError(validator.security_issues)
    
    # Create restricted globals
    safe_globals = {
        '__builtins__': {
            'len': len,
            'sorted': sorted,
            'enumerate': enumerate,
            'zip': zip,
            'range': range,
            'sum': sum,
            'min': min,
            'max': max,
        },
        'List': List,
        'Tuple': Tuple,
        'Document': Document,
        '_vector_search': mock_vector_search,
        '_keyword_search': mock_keyword_search,
    }
    
    # Execute with timeout
    with timeout(30):
        exec(code, safe_globals)
        hybrid_search = safe_globals.get('hybrid_search')
        
        if not callable(hybrid_search):
            raise ValueError("hybrid_search function not found")
        
        return hybrid_search(test_query, limit=10)
```
