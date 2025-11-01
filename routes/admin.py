"""
Admin panel routes.
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from sqlalchemy import func
from app.models import Document, SearchQuery, ModelSubmission, db
from app.core.upload import delete_document, reindex_document, get_upload_statistics

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def index():
    """
    Admin dashboard overview.
    """
    stats = get_upload_statistics()
    
    # Additional stats
    stats['total_searches'] = SearchQuery.query.count()
    stats['total_submissions'] = ModelSubmission.query.count()
    stats['avg_search_time'] = db.session.query(
        func.avg(SearchQuery.execution_time)
    ).scalar() or 0
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/documents')
def documents():
    """
    Document management interface.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    # Filter by category if specified
    category_filter = request.args.get('category', None)
    
    query = Document.query
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    documents = query.order_by(
        Document.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Get categories for filter
    categories = db.session.query(Document.category).distinct().all()
    category_names = [c[0] for c in categories]
    
    return render_template(
        'admin/documents.html',
        documents=documents,
        categories=category_names
    )

@admin_bp.route('/document/<int:doc_id>/delete', methods=['POST'])
def delete_doc(doc_id):
    """
    Delete a document.
    """
    if delete_document(doc_id):
        flash('Document deleted successfully', 'success')
    else:
        flash('Document not found', 'error')
    
    return redirect(url_for('admin.documents'))

@admin_bp.route('/document/<int:doc_id>/reindex', methods=['POST'])
def reindex_doc(doc_id):
    """
    Reindex a document.
    """
    try:
        doc = reindex_document(doc_id)
        flash(f'Reindexed: {doc.title}', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('admin.documents'))

@admin_bp.route('/reindex-all', methods=['POST'])
def reindex_all():
    """
    Reindex all documents.
    """
    documents = Document.query.all()
    success_count = 0
    error_count = 0
    
    for doc in documents:
        try:
            reindex_document(doc.id)
            success_count += 1
        except Exception as e:
            error_count += 1
    
    flash(f'Reindexed {success_count} documents ({error_count} errors)', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/stats')
def stats():
    """
    Detailed statistics page.
    """
    # Document stats
    doc_stats = {
        'total': Document.query.count(),
        'by_category': dict(db.session.query(
            Document.category,
            func.count(Document.id)
        ).group_by(Document.category).all())
    }
    
    # Search stats
    search_stats = {
        'total': SearchQuery.query.count(),
        'avg_time': db.session.query(func.avg(SearchQuery.execution_time)).scalar() or 0,
        'avg_results': db.session.query(func.avg(SearchQuery.results_count)).scalar() or 0
    }
    
    # Submission stats
    submission_stats = {
        'total': ModelSubmission.query.count(),
        'passed': ModelSubmission.query.filter_by(passed=True).count(),
        'avg_score': db.session.query(func.avg(ModelSubmission.score)).scalar() or 0,
        'by_model': dict(db.session.query(
            ModelSubmission.model_name,
            func.count(ModelSubmission.id)
        ).group_by(ModelSubmission.model_name).all())
    }
    
    return render_template(
        'admin/stats.html',
        doc_stats=doc_stats,
        search_stats=search_stats,
        submission_stats=submission_stats
    )

@admin_bp.route('/clear-cache', methods=['POST'])
def clear_cache():
    """
    Clear embeddings cache.
    """
    from app.core.embeddings import clear_embedding_cache
    clear_embedding_cache()
    flash('Embedding cache cleared', 'success')
    return redirect(url_for('admin.index'))