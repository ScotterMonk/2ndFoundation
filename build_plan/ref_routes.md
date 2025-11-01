## Routes Module

This document provides reference implementations for all Flask route blueprints in the application.

## Route Registration

All blueprints are registered in `app/__init__.py`:

```python
from app.routes.main import main_bp
from app.routes.rl_task import rl_task_bp
from app.routes.testing import testing_bp
from app.routes.admin import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(rl_task_bp, url_prefix='/rl-task')
app.register_blueprint(testing_bp, url_prefix='/testing')
app.register_blueprint(admin_bp, url_prefix='/admin')
```

## URL Structure

```
/                           - Home page
/search                     - Search interface
/search/history             - Search history
/upload                     - File upload
/document/<id>              - Document details
/api/search                 - Search API endpoint

/rl-task/                   - Task overview
/rl-task/submit             - Submit code
/rl-task/results/<id>       - View results
/rl-task/history            - Submission history
/rl-task/api/run-grader     - Run grader API

/testing/                   - Testing dashboard
/testing/test-case/<id>     - Test case detail
/testing/run-all            - Run all tests
/testing/benchmark          - Performance benchmarks

/admin/                     - Admin dashboard
/admin/documents            - Document management
/admin/stats                - Detailed statistics
/admin/document/<id>/delete - Delete document
/admin/document/<id>/reindex - Reindex document
/admin/reindex-all          - Reindex all
/admin/clear-cache          - Clear cache
```

## Main Routes (`app/routes/main.py`)
```python
@main_bp.route('/')
def index():
@main_bp.route('/search', methods=['GET', 'POST'])
def search():
@main_bp.route('/search/history')
def search_history():
@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
def handle_ajax_upload():
def handle_form_upload():
@main_bp.route('/document/<int:doc_id>')
@main_bp.route('/api/search')
def api_search():
```

## RL Task Routes (`app/routes/rl_task.py`)
```python
@rl_task_bp.route('/')
def overview():
@rl_task_bp.route('/submit', methods=['GET', 'POST'])
def submit():
@rl_task_bp.route('/results/<int:submission_id>')
def results(submission_id):
@rl_task_bp.route('/history')
def history():
@rl_task_bp.route('/api/run-grader', methods=['POST'])
def api_run_grader():
```

## Testing Routes (`app/routes/testing.py`)
```python
@testing_bp.route('/')
def dashboard():
@testing_bp.route('/test-case/<int:test_id>')
def test_case_detail(test_id):
@testing_bp.route('/run-all', methods=['POST'])
def run_all_tests():
@testing_bp.route('/benchmark')
def benchmark():
```

## Admin Routes (`app/routes/admin.py`)
```python
@admin_bp.route('/')
def index():
@admin_bp.route('/documents')
def documents():
@admin_bp.route('/document/<int:doc_id>/delete', methods=['POST'])
def delete_doc(doc_id):
@admin_bp.route('/document/<int:doc_id>/reindex', methods=['POST'])
def reindex_doc(doc_id):
@admin_bp.route('/reindex-all', methods=['POST'])
def reindex_all():
@admin_bp.route('/stats')
def stats():
@admin_bp.route('/clear-cache', methods=['POST'])
def clear_cache():
    """
    Clear embeddings cache.
    """
    from app.core.embeddings import clear_embedding_cache
    clear_embedding_cache()
    flash('Embedding cache cleared', 'success')
    return redirect(url_for('admin.index'))
```

