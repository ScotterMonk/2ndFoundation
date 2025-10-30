## Requirements Files

**`requirements.txt`**
```txt
# Flask and extensions
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5

# Database
psycopg2-binary==2.9.9
pgvector==0.2.4

# Embeddings
sentence-transformers==2.2.2
torch==2.1.0
transformers==4.35.0

# Document processing
PyPDF2==3.0.1
python-docx==1.1.0

# Utilities
python-dotenv==1.0.0
werkzeug==3.0.1

# Testing (optional for production)
pytest==7.4.3
pytest-flask==1.3.0
```

**`requirements-dev.txt`**
```txt
-r requirements.txt

# Development tools
black==23.12.0
flake8==6.1.0
mypy==1.7.1
ipython==8.18.1

# Testing
pytest-cov==4.1.0
pytest-mock==3.12.0
factory-boy==3.3.0

# Documentation
sphinx==7.2.6
```
