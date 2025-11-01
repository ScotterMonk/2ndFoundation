"""
Testing dashboard routes.
"""

from flask import Blueprint, render_template, request, jsonify
from app.models import TestCase, Document
from app.core.search import hybrid_search, _vector_search, _keyword_search
from app.core.grader import grade_submission
import time

testing_bp = Blueprint('testing', __name__)

@testing_bp.route('/')
def dashboard():
    """
    Testing dashboard overview.
    """
    # Get all test cases
    test_cases = TestCase.query.all()
    
    # Group by category
    categories = {}
    for tc in test_cases:
        if tc.category not in categories:
            categories[tc.category] = []
        categories[tc.category].append(tc)
    
    return render_template(
        'testing/dashboard.html',
        test_cases=test_cases,
        categories=categories
    )

@testing_bp.route('/test-case/<int:test_id>')
def test_case_detail(test_id):
    """
    View individual test case details.
    """
    test_case = TestCase.query.get_or_404(test_id)
    
    # Run the test case with reference implementation
    start_time = time.time()
    results = hybrid_search(test_case.query, limit=10)
    execution_time = time.time() - start_time
    
    # Get expected documents
    expected_docs = Document.query.filter(
        Document.id.in_(test_case.expected_docs)
    ).all()
    
    return render_template(
        'testing/test_case_detail.html',
        test_case=test_case,
        results=results,
        expected_docs=expected_docs,
        execution_time=execution_time
    )

@testing_bp.route('/run-all', methods=['POST'])
def run_all_tests():
    """
    Run all test cases with reference implementation.
    """
    test_cases = TestCase.query.all()
    results = []
    
    for tc in test_cases:
        start_time = time.time()
        search_results = hybrid_search(tc.query, limit=10)
        execution_time = time.time() - start_time
        
        # Check if expected docs are in results
        result_ids = [doc.id for doc in search_results]
        expected_found = sum(1 for exp_id in tc.expected_docs if exp_id in result_ids)
        
        results.append({
            'test_id': tc.id,
            'query': tc.query,
            'category': tc.category,
            'expected_count': len(tc.expected_docs),
            'found_count': expected_found,
            'execution_time': execution_time,
            'passed': expected_found >= len(tc.expected_docs) * 0.7  # 70% threshold
        })
    
    return jsonify({
        'total_tests': len(results),
        'passed': sum(1 for r in results if r['passed']),
        'results': results
    })

@testing_bp.route('/benchmark')
def benchmark():
    """
    Performance benchmarking interface.
    """
    # Run benchmarks for different search types
    test_queries = [
        "SELECT * FROM users",
        "neural network training",
        "python function average"
    ]
    
    benchmarks = {}
    
    for query in test_queries:
        # Vector search
        start = time.time()
        vector_results = _vector_search(query, limit=50)
        vector_time = time.time() - start
        
        # Keyword search
        start = time.time()
        keyword_results = _keyword_search(query, limit=50)
        keyword_time = time.time() - start
        
        # Hybrid search
        start = time.time()
        hybrid_results = hybrid_search(query, limit=10)
        hybrid_time = time.time() - start
        
        benchmarks[query] = {
            'vector_time': vector_time,
            'keyword_time': keyword_time,
            'hybrid_time': hybrid_time,
            'vector_count': len(vector_results),
            'keyword_count': len(keyword_results),
            'hybrid_count': len(hybrid_results)
        }
    
    return render_template(
        'testing/benchmark.html',
        benchmarks=benchmarks
    )