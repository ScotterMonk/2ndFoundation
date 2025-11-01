## Flask App Factory Pattern

**`app/__init__.py`**

```python
"""
Flask application factory.
Creates and configures the Flask app instance.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize extensions (but don't bind to app yet)
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """
    Application factory function.
    
    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
        
    Returns:
        Configured Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
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
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    return app

def register_error_handlers(app):
    """Register custom error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle uncaught exceptions."""
        app.logger.error(f'Unhandled exception: {error}')
        db.session.rollback()
        from flask import render_template
        return render_template('errors/500.html'), 500

def register_cli_commands(app):
    """Register custom CLI commands."""
    
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized.')
    
    @app.cli.command()
    def seed_test_data():
        """Seed database with test documents."""
        from app.rl_task.test_data import generate_test_documents
        from app.models import Document
        
        docs = generate_test_documents()
        for doc_data in docs:
            doc = Document(
                title=doc_data['title'],
                content=doc_data['content'],
                category=doc_data['category'],
                embedding=doc_data['embedding']
            )
            db.session.add(doc)
        
        db.session.commit()
        print(f'Seeded {len(docs)} test documents.')
    
    @app.cli.command()
    def clear_submissions():
        """Clear all model submissions."""
        from app.models import ModelSubmission
        ModelSubmission.query.delete()
        db.session.commit()
        print('Cleared all submissions.')
```

**`run.py`** (Development server entry point)

```python
"""
Development server entry point.
Run with: python run.py
"""

import os
from app import create_app

# Create app instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
```

**`wsgi.py`** (Production WSGI entry point)

```python
"""
Production WSGI entry point.
Used by Gunicorn/Waitress: gunicorn wsgi:app
"""

import os
from app import create_app

# Create app instance for production
app = create_app('production')

if __name__ == '__main__':
    app.run()
```

## Key Design Patterns

### 1. Extension Initialization
Extensions are created outside the factory but initialized inside:
```python
# Create extension instances
db = SQLAlchemy()

# Initialize with app later
def create_app():
    app = Flask(__name__)
    db.init_app(app)
```

### 2. Blueprint Registration
Routes are organized in blueprints and registered in the factory:
```python
from app.routes.main import main_bp
app.register_blueprint(main_bp)
app.register_blueprint(rl_task_bp, url_prefix='/rl-task')
```

### 3. Application Context
Database operations require application context:
```python
with app.app_context():
    db.create_all()
```

### 4. Configuration Management
Use config objects for different environments:
```python
from app.config import config
app.config.from_object(config[config_name])
```

## Blueprint Structure

**`app/routes/__init__.py`**
```python
"""Route blueprints."""
# Blueprints are imported in app/__init__.py
```

**`app/routes/main.py`** (Example blueprint)
```python
"""Main application routes."""

from flask import Blueprint, render_template, request, jsonify
from app.models import Document
from app.core.search import hybrid_search

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search page."""
    if request.method == 'POST':
        query = request.form.get('query', '')
        results = hybrid_search(query, limit=10)
        return render_template('search/results.html', 
                             query=query, 
                             results=results)
    return render_template('search/search.html')

@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload page."""
    if request.method == 'POST':
        # Handle file upload
        pass
    return render_template('search/upload.html')
```

## CLI Commands Usage

```bash
# Initialize database
flask init-db

# Seed test data
flask seed-test-data

# Clear submissions
flask clear-submissions

# Run development server
python run.py

# Run with Gunicorn (production)
gunicorn wsgi:app -w 4 -b 0.0.0.0:5000
```
