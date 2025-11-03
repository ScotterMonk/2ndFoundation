# Application

## Summary
A searchable knowledge oracle: drag-and-drop your documents, let the app index them with embeddings and keywords, then ask natural-language questions to retrieve the best passages and files in seconds. The app runs locally or on a web server, stores data in PostgreSQL with pgVector, and uses a production-grade hybrid search that blends semantic and keyword relevance for precise, trustworthy results.

Highlights for non-ML users
- Upload PDFs, Word docs, Markdown, and text files
- Automatic embeddings + keyword indexing for fast, accurate retrieval
- Powerful hybrid search (semantic + exact keywords) with fair scoring
- Clean web UI for Search, Uploads, Results history, Testing, Admin
- Works offline (local models) or with cloud embeddings if desired
- Secure by design: sandboxed execution, input sanitization, and best-practice deployment

## Stack
Python, Flask, Postgres with pgVector, HTML, CSS, JS

## Current Status
Scaffolding partially built.

## Navigation Menu / Pages / Flow

```
┌─────────────────────────────────────────────────────────┐
│  🔮 2nd Foundation                                      │
│  ───────────────────────────────────────────────────────│
│  [Home] [Search] [Upload] [RL Task] [Testing] [Admin]  │
└─────────────────────────────────────────────────────────┘
```

## Page Descriptions

### 1. Home (`/`)
- Project overview and purpose
- Quick stats: documents indexed, searches performed, model submissions
- Quick search bar
- Recent activity feed

### 2. Search (`/search`)
- Main search interface using production hybrid search
- Real-time results display
- Relevance scores shown
- Click to view full document
- Query history sidebar

### 3. Upload (`/upload`)
- Drag-and-drop document upload
- Supported formats: PDF, TXT, MD, DOCX
- Batch processing progress
- Upload history with status

### 4. RL Task (`/rl-task/*`)
Note: the RL task focuses on **implementing a novel re-ranking and retrieval optimization techniques** that would challenge an AI model to demonstrate real-world ML engineering capabilities.

**a) Overview (`/rl-task`)**
- Complete task description (what models receive)
- RRF algorithm explanation
- Expected function signature
- Example test cases
- Download starter template

**b) Submit (`/rl-task/submit`)**
- Code editor (Monaco or textarea)
- File upload option for `search.py`
- "Run Grader" button
- Real-time execution feedback

**c) Results (`/rl-task/results/<submission_id>`)**
- Overall pass/fail status
- Score breakdown by test category
- Per-test-case details:
  - Expected vs actual documents
  - Ranking comparison
  - Error messages
- Performance metrics
- Code diff viewer (vs reference implementation)
- "Submit Again" button

**d) History (`/rl-task/history`)**
- Table of all model submissions
- Columns: Model, Score, Time, Status
- Score progression chart
- Filter by model type

### 5. Testing (`/testing`)
- Run full test suite manually
- Individual test case explorer
- Performance benchmarks
- Coverage reports
- Compare reference impl vs model attempts

### 6. Admin (`/admin`)
- Document management (view, edit, delete)
- Database statistics
- Re-index documents
- Clear embeddings cache
- Export test data

## Application Architecture

### Directory Structure

```
2nd-foundation/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── .roo		# Folder for all Roo Code instruction files and reference docs
│   ├── .gitignore
│   ├── .roomodes
│   ├── activate.ps1
│   ├── config.py             # Configuration classes
│   ├── models.py             # SQLAlchemy models (Document, TaskSubmission, etc.)
│   ├── README.md
│   ├── requirements.txt
│   │
│   ├── venv
│   │
│   ├── build_plan		# Reference files for building this application
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Home, upload, search routes
│   │   ├── rl_task.py           # RL task interface routes
│   │   ├── testing.py           # Testing dashboard routes
│   │   └── admin.py             # Admin panel routes
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── search.py            # Production hybrid_search (reference impl)
│   │   ├── embeddings.py        # Vector generation
│   │   ├── upload.py            # Document processing
│   │   └── grader.py            # RL task grading logic ⭐
│   │
│   ├── rl_task/
│   │   ├── __init__.py
│   │   ├── task_definition.py   # Task prompt for models ⭐
│   │   ├── test_data.py         # Generate test documents ⭐
│   │   └── test_queries.json    # Test cases with expected results ⭐
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   └── components.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── search.js
│   │   │   └── task-runner.js
│   │   └── img/
│   │
│   ├── templates/
│   │   ├── base.html            # Base template with navigation
│   │   ├── index.html           # Landing page
│   │   │
│   │   ├── search/
│   │   │   ├── upload.html
│   │   │   ├── search.html
│   │   │   └── results.html
│   │   │
│   │   ├── rl_task/
│   │   │   ├── overview.html    # Task description
│   │   │   ├── submit.html      # Code submission form
│   │   │   ├── results.html     # Grading results
│   │   │   └── history.html     # Previous attempts
│   │   │
│   │   ├── testing/
│   │   │   ├── dashboard.html
│   │   │   └── details.html
│   │   │
│   │   └── admin/
│   │       ├── documents.html
│   │       └── stats.html
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_search.py
│       ├── test_grader.py
│       └── test_routes.py
│
├── run.py                       # Development server entry
└── wsgi.py                      # Production WSGI entry
⭐ = Files that get extracted for assignment submission
```

**⭐ = Files that get extracted for assignment submission**

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
