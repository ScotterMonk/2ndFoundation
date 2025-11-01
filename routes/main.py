"""
Main application routes: Home, Search, Upload
"""

from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models import Document, SearchQuery, db
from app.core.search import hybrid_search
from app.core.upload import (
    process_uploaded_file,
    process_batch_upload,
    get_upload_statistics,
    allowed_file
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Home page with overview and quick search.
    """
    # Get quick stats
    total_docs = Document.query.count()
    total_searches = SearchQuery.query.count()
    
    # Recent searches (last 5)
    recent_searches = SearchQuery.query.order_by(
        SearchQuery.created_at.desc()
    ).limit(5).all()
    
    # Recent documents (last 5)
    recent_docs = Document.query.order_by(
        Document.created_at.desc()
    ).limit(5).all()
    
    return render_template(
        'index.html',
        total_docs=total_docs,
        total_searches=total_searches,
        recent_searches=recent_searches,
        recent_docs=recent_docs
    )

@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    """
    Search interface using production hybrid search.
    """
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        limit = int(request.form.get('limit', 10))
        
        if not query:
            flash('Please enter a search query', 'warning')
            return redirect(url_for('main.search'))
        
        # Track execution time
        start_time = datetime.utcnow()
        
        # Perform hybrid search
        results = hybrid_search(query, limit=limit)
        
        # Calculate execution time
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log search query
        search_query = SearchQuery(
            query=query,
            results_count=len(results),
            execution_time=execution_time
        )
        db.session.add(search_query)
        db.session.commit()
        
        return render_template(
            'search/results.html',
            query=query,
            results=results,
            execution_time=execution_time,
            results_count=len(results)
        )
    
    # GET request - show search form
    # Get query history for sidebar
    recent_queries = SearchQuery.query.order_by(
        SearchQuery.created_at.desc()
    ).limit(10).all()
    
    return render_template(
        'search/search.html',
        recent_queries=recent_queries
    )

@main_bp.route('/search/history')
def search_history():
    """
    View search query history.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    queries = SearchQuery.query.order_by(
        SearchQuery.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'search/history.html',
        queries=queries
    )

@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Document upload interface.
    """
    if request.method == 'POST':
        # Check if request is JSON (AJAX) or form submission
        if request.is_json:
            # AJAX upload
            return handle_ajax_upload()
        else:
            # Form upload
            return handle_form_upload()
    
    # GET request - show upload form
    stats = get_upload_statistics()
    return render_template('search/upload.html', stats=stats)

def handle_ajax_upload():
    """Handle AJAX file upload."""
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    upload_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    
    successful, errors = process_batch_upload(files, upload_dir)
    
    return jsonify({
        'success': len(successful),
        'errors': errors,
        'documents': [
            {
                'id': doc.id,
                'title': doc.title,
                'category': doc.category,
                'created_at': doc.created_at.isoformat()
            }
            for doc in successful
        ]
    })

def handle_form_upload():
    """Handle traditional form file upload."""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('main.upload'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('main.upload'))
    
    if not allowed_file(file.filename):
        flash('File type not allowed', 'error')
        return redirect(url_for('main.upload'))
    
    upload_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    title = request.form.get('title', None)
    category = request.form.get('category', None)
    
    try:
        doc = process_uploaded_file(file, upload_dir, title=title, category=category)
        flash(f'Successfully uploaded: {doc.title}', 'success')
        return redirect(url_for('main.document_detail', doc_id=doc.id))
    except ValueError as e:
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('main.upload'))

@main_bp.route('/document/<int:doc_id>')
def document_detail(doc_id):
    """
    View document details.
    """
    doc = Document.query.get_or_404(doc_id)
    
    return render_template(
        'search/document_detail.html',
        document=doc
    )

@main_bp.route('/api/search')
def api_search():
    """
    API endpoint for search (JSON response).
    """
    query = request.args.get('q', '').strip()
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    results = hybrid_search(query, limit=limit)
    
    return jsonify({
        'query': query,
        'results': [
            {
                'id': doc.id,
                'title': doc.title,
                'content': doc.content[:200] + '...' if len(doc.content) > 200 else doc.content,
                'category': doc.category
            }
            for doc in results
        ]
    })