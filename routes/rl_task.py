"""
RL Task routes: Overview, Submit, Results, History
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from datetime import datetime

from app.models import ModelSubmission, TestCase, db
from app.rl_task.task_definition import get_task_prompt
from app.core.grader import grade_submission

rl_task_bp = Blueprint('rl_task', __name__)

@rl_task_bp.route('/')
def overview():
    """
    Task description and overview.
    """
    task_prompt = get_task_prompt()
    
    # Get some statistics
    total_submissions = ModelSubmission.query.count()
    passed_submissions = ModelSubmission.query.filter_by(passed=True).count()
    
    # Get best score
    best_submission = ModelSubmission.query.order_by(
        ModelSubmission.score.desc()
    ).first()
    
    return render_template(
        'rl_task/overview.html',
        task_prompt=task_prompt,
        total_submissions=total_submissions,
        passed_submissions=passed_submissions,
        best_score=best_submission.score if best_submission else 0
    )

@rl_task_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    """
    Code submission interface.
    """
    if request.method == 'POST':
        # Get submission data
        code = request.form.get('code', '').strip()
        model_name = request.form.get('model_name', 'unknown')
        
        if not code:
            flash('Please provide code to submit', 'error')
            return redirect(url_for('rl_task.submit'))
        
        # Check code length
        max_length = current_app.config.get('MAX_CODE_LENGTH', 10000)
        if len(code) > max_length:
            flash(f'Code too long. Maximum {max_length} characters.', 'error')
            return redirect(url_for('rl_task.submit'))
        
        try:
            # Get test cases
            test_cases = TestCase.query.all()
            
            # Grade submission
            result = grade_submission(code, test_cases)
            
            # Save submission
            submission = ModelSubmission(
                model_name=model_name,
                code=code,
                score=result['score'],
                passed=result['passed'],
                test_results=result['test_results'],
                execution_time=result['execution_time']
            )
            
            if 'security_issues' in result:
                submission.security_issues = result['security_issues']
            
            db.session.add(submission)
            db.session.commit()
            
            flash('Submission graded successfully!', 'success')
            return redirect(url_for('rl_task.results', submission_id=submission.id))
        
        except Exception as e:
            flash(f'Grading failed: {str(e)}', 'error')
            return redirect(url_for('rl_task.submit'))
    
    # GET request - show submission form
    task_prompt = get_task_prompt()
    return render_template('rl_task/submit.html', task_prompt=task_prompt)

@rl_task_bp.route('/results/<int:submission_id>')
def results(submission_id):
    """
    View submission results.
    """
    submission = ModelSubmission.query.get_or_404(submission_id)
    
    # Get reference implementation for comparison
    from app.core.search import hybrid_search
    import inspect
    reference_code = inspect.getsource(hybrid_search)
    
    return render_template(
        'rl_task/results.html',
        submission=submission,
        reference_code=reference_code
    )

@rl_task_bp.route('/history')
def history():
    """
    View submission history.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter by model if specified
    model_filter = request.args.get('model', None)
    
    query = ModelSubmission.query
    if model_filter:
        query = query.filter_by(model_name=model_filter)
    
    submissions = query.order_by(
        ModelSubmission.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Get unique model names for filter dropdown
    models = db.session.query(ModelSubmission.model_name).distinct().all()
    model_names = [m[0] for m in models]
    
    # Score progression data for chart
    score_data = db.session.query(
        ModelSubmission.created_at,
        ModelSubmission.score,
        ModelSubmission.model_name
    ).order_by(ModelSubmission.created_at).all()
    
    return render_template(
        'rl_task/history.html',
        submissions=submissions,
        model_names=model_names,
        score_data=score_data
    )

@rl_task_bp.route('/api/run-grader', methods=['POST'])
def api_run_grader():
    """
    API endpoint to run grader (for AJAX submission).
    """
    data = request.get_json()
    code = data.get('code', '')
    model_name = data.get('model_name', 'unknown')
    
    if not code:
        return jsonify({'error': 'Code is required'}), 400
    
    try:
        test_cases = TestCase.query.all()
        result = grade_submission(code, test_cases)
        
        return jsonify({
            'success': True,
            'score': result['score'],
            'passed': result['passed'],
            'test_results': result['test_results'],
            'execution_time': result['execution_time']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500