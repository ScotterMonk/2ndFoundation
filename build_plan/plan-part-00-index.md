# Project Plan: "2nd Foundation" + RL Task

## Core Concept
Build a **RAG (Retrieval Augmented Generation) system** with pgVector with features outlined in this index and summarized from a user perspective in `build_plan/plan-part-05.md`.

Note: make the RL task focus on **implementing a novel re-ranking and retrieval optimization techniques** that would challenge an AI model to demonstrate real-world ML engineering capabilities.

## Spec Overview
Python, Flask, Postgres with pgVector, HTML, CSS, JS

## Index
`build_plan/plan-part-00-index.md`
- Core Concept
`build_plan/plan-part-01.md`
- Understanding the RL Task Flow
- The RL Task: Hybrid Search with RRF
    - What the Model Receives (Task Prompt)
    - Verification Approach
    - Expected Model Failure Modes
    - Grading Criteria
`build_plan/plan-part-02.md`
- Integration with Assignment Framework
    - Dual Purpose Architecture
    - Extractable Components for Assignment Submission
`build_plan/plan-part-03.md`
- Application Architecture
    - Directory Structure
`build_plan/plan-part-04.md`
- Database Schema
    - Document Model (with embeddings and ts_vector)
    - SearchQuery Model (analytics)
    - ModelSubmission Model (RL task tracking)
    - TestCase Model (grading test cases)
`build_plan/plan-part-05.md`
- Application Pages & Flow
    - Navigation Menu
    - Page Descriptions
    - Home (/)
    - Search (/search)
    - Upload (/upload)
    - RL Task (/rl-task/*) - Core Assignment Interface
    - Overview
    - Submit
    - Results
    - History
    - Testing (/testing)
    - Admin (/admin)
`build_plan/plan-part-06.md`
- Key Implementation Details
    - Environment Configuration (.env.example, config.py)
    - Embeddings Strategy (model choice, generation timing)
    - Code Execution Sandbox (security measures for grading)
`build_plan/plan-part-07.md`
- Test Data Generation
    - Test Documents (50 docs across categories)
    - Test Queries (with expected results)
    - SQL Export for Assignment Submission
`build_plan/plan-part-08.md`
- Flask Application Integration
    - App Factory (create_app, blueprints)
    - RL Task Routes
    - Overview route
    - Submit route (POST/GET)
    - Results route
    - History route
`build_plan/plan-part-09.md`
- Reference Implementation
    - Production Hybrid Search (app/core/search.py)
    - _vector_search function (pgvector cosine similarity)
    - _keyword_search function (PostgreSQL full-text search)
    - hybrid_search function (RRF algorithm implementation)
`build_plan/plan-part-10.md`
- Task Definition Module
    - app/rl_task/task_definition.py (extracted to task.py for assignment)
    - TaskDefinition dataclass (name, version, difficulty, description, requirements)
    - get_task_prompt function (generates complete task prompt for AI models)
    - Evaluation criteria (correctness, ranking quality, edge cases)
    - Common failure modes to avoid
`build_plan/plan-part-11.md`
- Requirements Files
    - requirements.txt (Flask, SQLAlchemy, pgvector, sentence-transformers, etc.)
    - requirements-dev.txt (development tools, testing, documentation)
`build_plan/plan-part-12.md`
- Application Entry Points
    - run.py (development server entry point)
    - Flask shell context processor
    - CLI commands (init_db, load_test_data, export_assignment)
    - Setup Instructions
        - Prerequisites (PostgreSQL with pgvector)
        - Project setup (virtual environment, dependencies)
        - Database initialization (migrations, test data)
        - Run development server
        - Export assignment submission
`build_plan/plan-part-13.md`
- Testing Strategy
    - Unit Tests (app/tests/test_search.py)
        - test_vector_search
        - test_keyword_search
        - test_hybrid_search_basic
        - test_hybrid_search_empty_query
    - Integration Tests (app/tests/test_grader.py)
        - test_grade_correct_submission
        - test_grade_incorrect_k_value
`build_plan/plan-part-14.md`
- Deployment Considerations
    - Production Setup
        - Non-Docker deployment options (choose one):
            - Linux: Gunicorn behind Nginx as a systemd service
            - Windows: Waitress or Gunicorn via NSSM as a Windows service
            - macOS: launchd service for development
            - PaaS: Render, Fly.io, Railway, or Heroku-like platforms
        - PostgreSQL with pgVector installed (managed service or self-hosted)
        - Environment config via .env and system secrets
    - Security Checklist
        - Environment variables for secrets
        - CSRF protection
        - Input sanitization
        - Rate limiting
        - HTTPS in production
        - Code execution sandboxing
        - SQL injection monitoring
        - Authentication/authorization
        - Dependency updates
