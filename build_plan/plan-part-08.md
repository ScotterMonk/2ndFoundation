## Flask Application Integration

### App Factory

**`app/__init__.py`**
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.rl_task import rl_task_bp
    from app.routes.testing import testing_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(rl_task_bp, url_prefix='/rl-task')
    app.register_blueprint(testing_bp, url_prefix='/testing')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app
```

### RL Task Routes

**`app/routes/rl_task.py`**
```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import ModelSubmission, TestCase, db
from app.core.grader import grade_submission
from app.rl_task.task_definition import get_task_prompt
import time

rl_task_bp = Blueprint('rl_task', __name__)

@rl_task_bp.route('/')
def overview():
    """Display RL task description and requirements."""
    task_prompt = get_task_prompt()
    test_cases = TestCase.query.limit(3).all()  # Show sample tests
    return render_template('rl_task/overview.html', 
                         task=task_prompt,
                         sample_tests=test_cases)

@rl_task_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    """Submit model-generated code for grading."""
    if request.method == 'POST':
        # Get code from form or file upload
        code = request.form.get('code')
        if not code and 'file' in request.files:
            file = request.files['file']
            code = file.read().decode('utf-8')
        
        if not code:
            flash('No code provided', 'error')
            return redirect(url_for('rl_task.submit'))
        
        # Optional: specify model name
        model_name = request.form.get('model_name', 'unknown')
        
        # Grade the submission
        test_cases = TestCase.query.all()
        start_time = time.time()
        result = grade_submission(code, test_cases)
        
        # Save to database
        submission = ModelSubmission(
            model_name=model_name,
            code=code,
            score=result['score'],
            passed=result['passed'],
            test_results=result['details'],
            execution_time=result['execution_time'],
            security_issues=result['details'].get('security_issues', [])
        )
        db.session.add(submission)
        db.session.commit()
        
        flash(f"Submission graded! Score: {result['score']:.2%}", 
              'success' if result['passed'] else 'warning')
        return redirect(url_for('rl_task.results', id=submission.id))
    
    # GET: Show submission form
    return render_template('rl_task/submit.html')

@rl_task_bp.route('/results/<int:id>')
def results(id):
    """Display grading results for a submission."""
    submission = ModelSubmission.query.get_or_404(id)
    
    # Format test results for display
    test_results = submission.test_results.get('test_cases', [])
    
    # Calculate category-wise scores
    category_scores = {}
    for test in test_results:
        cat = test.get('category', 'unknown')
        if cat not in category_scores:
            category_scores[cat] = {'total': 0, 'passed': 0}
        category_scores[cat]['total'] += 1
        if test.get('passed'):
            category_scores[cat]['passed'] += 1
    
    return render_template('rl_task/results.html',
                         submission=submission,
                         test_results=test_results,
                         category_scores=category_scores)

@rl_task_bp.route('/history')
def history():
    """Show history of all model submissions."""
    submissions = ModelSubmission.query.order_by(
        ModelSubmission.created_at.desc()
    ).all()
    
    # Calculate statistics
    stats = {
        'total_submissions': len(submissions),
        'passed': sum(1 for s in submissions if s.passed),
        'avg_score': sum(s.score for s in submissions) / len(submissions) if submissions else 0,
        'best_score': max((s.score for s in submissions), default=0)
    }
    
    return render_template('rl_task/history.html',
                         submissions=submissions,
                         stats=stats)
```
