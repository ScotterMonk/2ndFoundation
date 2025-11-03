#!/usr/bin/env python3
"""
Schema comparison and documentation commands for schema_inspector.py
[Created] by Roo | 2025-10-28_1

This module provides the implementation for database schema comparison,
documentation generation, and validation commands.
"""

import json
import os
from datetime import datetime
from sqlalchemy import inspect as sqlalchemy_inspect
from utils.database import db

# [Created] by Roo | 2025-10-28_1
def get_db_schema():
    """
    Get database schema information from PGDB.
    Returns dict mapping table names to their column/constraint info.
    """
    inspector = sqlalchemy_inspect(db.engine)
    db_schema = {}
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        
        db_schema[table_name] = {
            'columns': [col['name'] for col in columns],
            'column_types': {col['name']: str(col['type']) for col in columns},
            'nullable': {col['name']: col['nullable'] for col in columns},
            'primary_keys': pk_constraint['constrained_columns'] if pk_constraint else [],
            'foreign_keys': [fk['constrained_columns'] for fk in inspector.get_foreign_keys(table_name)]
        }
    
    return db_schema

# [Created] by Roo | 2025-10-28_1
def get_model_schema():
    """
    Get schema information from SQLAlchemy models using db.Model registry.
    This avoids import order issues by using Flask-SQLAlchemy's model registry.
    """
    # Import models to ensure they're registered
    import models
    
    model_schema = {}
    
    # Use db.Model's registry to get all mapped classes
    # This automatically handles import order and FK resolution
    for mapper in db.Model.registry.mappers:
        model_class = mapper.class_
        
        # Skip if no tablename
        if not hasattr(model_class, '__tablename__'):
            continue
            
        table_name = model_class.__tablename__
        table = model_class.__table__
        
        # Extract column information
        columns = []
        for col in table.columns:
            columns.append({
                'name': col.name,
                'type': str(col.type),
                'nullable': col.nullable,
                'primary_key': col.primary_key,
                'foreign_keys': [str(fk.column) for fk in col.foreign_keys] if col.foreign_keys else []
            })
        
        model_schema[table_name] = {
            'columns': [col['name'] for col in columns],
            'column_types': {col['name']: col['type'] for col in columns},
            'nullable': {col['name']: col['nullable'] for col in columns},
            'primary_keys': [col['name'] for col in columns if col['primary_key']],
            'foreign_keys': [col['foreign_keys'] for col in columns if col['foreign_keys']],
            'model_class': model_class.__name__
        }
    
    return model_schema

# [Created] by Roo | 2025-10-28_1
def compare_schemas(db_schema, model_schema):
    """
    Compare database schema with model schema and report differences.
    Returns list of discrepancy dicts.
    """
    discrepancies = []
    
    # Tables in DB but not in models
    db_only_tables = set(db_schema.keys()) - set(model_schema.keys())
    if db_only_tables:
        for table in db_only_tables:
            discrepancies.append({
                'type': 'table_in_db_not_model',
                'table': table,
                'severity': 'high'
            })
    
    # Tables in models but not in DB
    model_only_tables = set(model_schema.keys()) - set(db_schema.keys())
    if model_only_tables:
        for table in model_only_tables:
            discrepancies.append({
                'type': 'table_in_model_not_db',
                'table': table,
                'model_class': model_schema[table].get('model_class', 'Unknown'),
                'severity': 'high'
            })
    
    # Compare common tables
    common_tables = set(db_schema.keys()) & set(model_schema.keys())
    for table in common_tables:
        db_table = db_schema[table]
        model_table = model_schema[table]
        
        # Columns in DB but not in model
        db_only_columns = set(db_table['columns']) - set(model_table['columns'])
        for column in db_only_columns:
            discrepancies.append({
                'type': 'column_in_db_not_model',
                'table': table,
                'column': column,
                'severity': 'medium'
            })
        
        # Columns in model but not in DB
        model_only_columns = set(model_table['columns']) - set(db_table['columns'])
        for column in model_only_columns:
            discrepancies.append({
                'type': 'column_in_model_not_db',
                'table': table,
                'column': column,
                'model_class': model_table.get('model_class', 'Unknown'),
                'severity': 'medium'
            })
        
        # Type/nullable differences in common columns
        common_columns = set(db_table['columns']) & set(model_table['columns'])
        for column in common_columns:
            db_type = str(db_table['column_types'].get(column, ''))
            model_type = model_table['column_types'].get(column, '')
            
            # Normalize types for comparison
            db_type_normalized = db_type.split('(')[0].upper()
            model_type_normalized = model_type.split('(')[0].upper()
            
            if db_type_normalized != model_type_normalized:
                discrepancies.append({
                    'type': 'column_type_mismatch',
                    'table': table,
                    'column': column,
                    'db_type': db_type,
                    'model_type': model_type,
                    'severity': 'low'
                })
            
            # Nullable differences
            db_nullable = db_table['nullable'].get(column, None)
            model_nullable = model_table['nullable'].get(column, None)
            
            if db_nullable != model_nullable:
                discrepancies.append({
                    'type': 'column_nullable_mismatch',
                    'table': table,
                    'column': column,
                    'db_nullable': db_nullable,
                    'model_nullable': model_nullable,
                    'severity': 'low'
                })
    
    return discrepancies

# [Created] by Roo | 2025-10-28_1
def run_compare_db_models(args):
    """
    Compare PGDB schema vs ORM models and identify discrepancies.
    Generates reports in .roo/reports/ directory.
    """
    try:
        print("Extracting database schema...")
        db_schema = get_db_schema()
        
        print("Extracting model schema...")
        model_schema = get_model_schema()
        
        print("Comparing schemas...")
        discrepancies = compare_schemas(db_schema, model_schema)
        
        # Categorize by severity
        critical = [d for d in discrepancies if d.get('severity') == 'high']
        warnings = [d for d in discrepancies if d.get('severity') == 'medium']
        info = [d for d in discrepancies if d.get('severity') == 'low']
        
        # Create reports directory
        os.makedirs('.roo/reports', exist_ok=True)
        
        # Generate JSON report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_discrepancies': len(discrepancies),
                'critical': len(critical),
                'warnings': len(warnings),
                'info': len(info)
            },
            'discrepancies': discrepancies
        }
        
        json_path = '.roo/reports/db_models_discrepancies.json'
        with open(json_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate Markdown summary
        md_lines = [
            "# Database vs Models Comparison Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"- Total Discrepancies: {len(discrepancies)}",
            f"- Critical (High): {len(critical)}",
            f"- Warnings (Medium): {len(warnings)}",
            f"- Info (Low): {len(info)}",
            ""
        ]
        
        if critical:
            md_lines.extend(["## Critical Issues", ""])
            for d in critical:
                md_lines.append(f"- `{d['table']}`: {d['type']}")
            md_lines.append("")
        
        if warnings:
            md_lines.extend(["## Warnings", ""])
            for d in warnings:
                md_lines.append(f"- `{d['table']}.{d.get('column', 'N/A')}`: {d['type']}")
            md_lines.append("")
        
        md_path = '.roo/reports/db_models_discrepancies.md'
        with open(md_path, 'w') as f:
            f.write('\n'.join(md_lines))
        
        # Console output
        print(f"\n✓ Comparison complete")
        print(f"  Total discrepancies: {len(discrepancies)}")
        print(f"  Critical: {len(critical)}, Warnings: {len(warnings)}, Info: {len(info)}")
        print(f"\nReports generated:")
        print(f"  JSON: {json_path}")
        print(f"  Markdown: {md_path}")
        
        return {
            'status': 'success',
            'discrepancies_count': len(discrepancies),
            'json_report': json_path,
            'md_report': md_path
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

# Placeholder stubs for other commands
def run_compare_models_doc(args):
    return {'status': 'error', 'error': 'Not yet implemented'}

def run_generate_docs(args):
    return {'status': 'error', 'error': 'Not yet implemented'}

def run_report(args):
    return {'status': 'error', 'error': 'Not yet implemented'}

def run_introspect(args):
    return {'status': 'error', 'error': 'Not yet implemented'}