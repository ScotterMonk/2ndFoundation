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
