## Application Entry Points

**`run.py`**
```python
"""
Development server entry point.
"""

import os
from app import create_app, db
from app.models import Document, SearchQuery, ModelSubmission, TestCase

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Add models to Flask shell context."""
    return {
        'db': db,
        'Document': Document,
        'SearchQuery': SearchQuery,
        'ModelSubmission': ModelSubmission,
        'TestCase': TestCase
    }

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def load_test_data():
    """Load test data for RL task."""
    from app.rl_task.test_data import load_test_data_to_db
    load_test_data_to_db()
    print("Test data loaded!")

@app.cli.command()
def export_assignment():
    """Export files for assignment submission."""
    import os
    import shutil
    from app.rl_task.task_definition import get_task_prompt
    from app.rl_task.test_data import export_to_sql
    
    # Create submission directory
    os.makedirs('assignment_submission', exist_ok=True)
    
    # Export task.py
    with open('assignment_submission/task.py', 'w') as f:
        f.write('"""\n')
        f.write(get_task_prompt())
        f.write('\n"""\n')
    
    # Copy grader.py
    shutil.copy('app/core/grader.py', 'assignment_submission/grader.py')
    
    # Export test_data.sql
    with open('assignment_submission/test_data.sql', 'w') as f:
        f.write(export_to_sql())
    
    # Create README
    with open('assignment_submission/README.md', 'w') as f:
        f.write('''# Hybrid Search RL Task Submission

## Task Description
Implement hybrid search using Reciprocal Rank Fusion (RRF).

## Files
- `task.py`: Complete task specification for AI models
- `grader.py`: Grading logic to evaluate model-generated implementations
- `test_data.sql`: Test database with 50 documents and 10 test queries

## Usage
The assignment framework will:
1. Load test data from `test_data.sql`
2. Present task from `task.py` to AI models (Claude, GPT, etc.)
3. Evaluate model-generated code using `grader.py`
4. Collect results for reinforcement learning
''')
    
    print("Assignment files exported to assignment_submission/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## Setup Instructions

### 1. Prerequisites

```bash
# Install PostgreSQL with pgvector extension
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE EXTENSION vector;"

# Create database
sudo -u postgres createdb second_foundation
sudo -u postgres createdb second_foundation_test
```

### 2. Project Setup

```bash
# Clone/create project directory
mkdir 2nd-foundation
cd 2nd-foundation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Initialization

```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Load test data
flask load-test-data
```

### 4. Run Development Server

```bash
flask run
# Visit http://localhost:5000
```

### 5. Export Assignment Submission

```bash
flask export-assignment
# Files created in assignment_submission/
```

