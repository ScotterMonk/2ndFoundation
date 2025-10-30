#!/usr/bin/env python3
"""
Schema comparison core utilities.
Extracted from legacy compare_models.py to support the Schema Inspector utility.

Provides core functions for:
- Discovering and loading SQLAlchemy models
- Comparing database schema with model definitions
- Categorizing and reporting discrepancies
"""
# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1

import os
import sys
import glob
import json
import importlib
from datetime import datetime, timezone
from typing import Dict, Any, List

from utils.database import db

# Type mapping between SQLAlchemy types and PostgreSQL types
TYPE_MAPPING = {
    'Integer': 'int4',
    'String': 'varchar',
    'Text': 'text',
    'Boolean': 'boolean',
    'DateTime': 'timestamp with time zone',
    'Float': 'real',
    'Numeric': 'numeric',
    'JSONB': 'jsonb',
    'JSON': 'json',
    'ARRAY': 'ARRAY',
    'INET': 'inet',
    'BigInteger': 'bigint',
}

# Reverse mapping for PostgreSQL to SQLAlchemy
PG_TO_SQLALCHEMY = {
    'int4': 'Integer',
    'varchar': 'String',
    'text': 'Text',
    'boolean': 'Boolean',
    'timestamptz': 'DateTime',
    'timestamp without time zone': 'DateTime',
    'real': 'Float',
    'numeric': 'Numeric',
    'jsonb': 'JSONB',
    'json': 'JSON',
    'ARRAY': 'ARRAY',
    'inet': 'INET',
    'bigint': 'BigInteger',
    'double precision': 'Float',
}


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def get_sqlalchemy_models(model_files):
    """
    Extract SQLAlchemy model definitions from model files.
    
    Uses Flask-SQLAlchemy registry to enumerate mapped classes, avoiding
    duplicate Table object issues.

    Args:
        model_files (list): List of model file paths

    Returns:
        dict: Dictionary of models with their columns and properties
    """
    models = {}

    # Import all model modules safely by module name
    module_names = []
    for file_path in model_files:
        # Convert 'models/models_user.py' -> 'models.models_user'
        module_name = file_path.replace("/", ".").replace("\\", ".")
        if module_name.endswith(".py"):
            module_name = module_name[:-3]
        # Ensure it starts with 'models.'
        if not module_name.startswith("models."):
            # Best effort normalization
            base = os.path.splitext(os.path.basename(file_path))[0]
            module_name = f"models.{base}"
        module_names.append(module_name)

    for mod in module_names:
        try:
            if mod in sys.modules:
                importlib.import_module(mod)  # ensures it's initialized
            else:
                importlib.import_module(mod)
        except Exception as e:
            print(f"Warning: could not import module {mod}: {e}")

    # Now iterate all mapped classes from the registry
    try:
        registry = getattr(db.Model, "registry", None)
        if not registry:
            print("Warning: SQLAlchemy registry not available; no models discovered")
            return models

        for mapper in registry.mappers:
            cls = mapper.class_
            table = getattr(cls, "__table__", None)
            if table is None or not hasattr(cls, "__tablename__"):
                continue

            table_name = table.name
            models[table_name] = {
                "class_name": cls.__name__,
                "columns": {},
                "primary_key": [],
                "foreign_keys": [],
            }

            for col in table.columns:
                col_name = col.name
                column_type = type(col.type).__name__ if hasattr(col, "type") else None

                length = None
                if hasattr(col.type, "length") and col.type.length:
                    length = str(col.type.length)
                elif hasattr(col.type, "precision") and col.type.precision is not None:
                    if hasattr(col.type, "scale") and col.type.scale is not None:
                        length = f"{col.type.precision},{col.type.scale}"
                    else:
                        length = str(col.type.precision)

                if getattr(col, "primary_key", False):
                    models[table_name]["primary_key"].append(col_name)

                if getattr(col, "foreign_keys", None):
                    for fk in col.foreign_keys:
                        target = str(fk.target_fullname)
                        ref_table, ref_col = target.split(".", 1)
                        models[table_name]["foreign_keys"].append(
                            {"column": col_name, "references": {"table": ref_table, "column": ref_col}}
                        )

                models[table_name]["columns"][col_name] = {
                    "type": column_type,
                    "length": length,
                    "nullable": bool(getattr(col, "nullable", True)),
                    "primary_key": bool(getattr(col, "primary_key", False)),
                    "foreign_key": bool(getattr(col, "foreign_keys", None)),
                }

    except Exception as e:
        print(f"Error while enumerating mapped classes: {e}")

    # Diagnostics
    sample = list(models.keys())[:5]
    print(f"Discovered {len(models)} model tables via registry. Sample: {sample}")

    return models


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def compare_schema_with_models(db_schema, models):
    """
    Compare database schema with SQLAlchemy models.
    
    Args:
        db_schema (dict): Dictionary of database tables
        models (dict): Dictionary of SQLAlchemy models
        
    Returns:
        dict: Dictionary of discrepancies
    """
    discrepancies = {}
    
    # Check for tables in schema but not in models
    schema_tables = set(db_schema.keys())
    model_tables = set(models.keys())
    
    tables_only_in_schema = schema_tables - model_tables
    tables_only_in_models = model_tables - schema_tables
    
    if tables_only_in_schema:
        discrepancies['tables_only_in_schema'] = list(tables_only_in_schema)
    
    if tables_only_in_models:
        discrepancies['tables_only_in_models'] = list(tables_only_in_models)
    
    # Compare tables that exist in both
    common_tables = schema_tables.intersection(model_tables)
    
    for table_name in common_tables:
        table_discrepancies = {}
        
        # Compare columns
        schema_columns = set(db_schema[table_name]['columns'].keys())
        model_columns = set(models[table_name]['columns'].keys())
        
        columns_only_in_schema = schema_columns - model_columns
        columns_only_in_models = model_columns - schema_columns
        
        if columns_only_in_schema:
            table_discrepancies['columns_only_in_schema'] = list(columns_only_in_schema)
        
        if columns_only_in_models:
            table_discrepancies['columns_only_in_models'] = list(columns_only_in_models)
        
        # Compare column types and properties for common columns
        common_columns = schema_columns.intersection(model_columns)
        type_mismatches = []
        nullable_mismatches = []
        
        for column_name in common_columns:
            schema_column = db_schema[table_name]['columns'][column_name]
            model_column = models[table_name]['columns'][column_name]
            
            # Compare types
            # Normalize both sides and account for common PostgreSQL synonyms
            schema_type = (schema_column.get('type') or '').lower()
            model_type = (model_column.get('type') or '')
            # Map SQLAlchemy type name to a representative PostgreSQL type name
            mapped_model_type = TYPE_MAPPING.get(model_type, model_type).lower()

            # Normalize synonyms
            if schema_type == 'character varying':
                schema_type = 'varchar'
            if mapped_model_type == 'character varying':
                mapped_model_type = 'varchar'
            if schema_type == 'timestamptz':
                schema_type = 'timestamp with time zone'
            if mapped_model_type in ('datetime', 'timestamp'):
                # Treat these as timestamp types to reduce false positives
                mapped_model_type = 'timestamp with time zone' if schema_type == 'timestamp with time zone' else mapped_model_type

            # Only record a mismatch when clearly different after normalization
            if schema_type != mapped_model_type and not (
                (schema_type in ('varchar',) and mapped_model_type in ('varchar', 'string')) or
                (schema_type.startswith('timestamp') and mapped_model_type in ('datetime', 'timestamp with time zone', 'timestamp')) or
                (schema_type == 'double precision' and mapped_model_type == 'float')
            ):
                type_mismatches.append({
                    'column': column_name,
                    'schema_type': schema_column.get('type'),
                    'model_type': model_type
                })
            
            # Compare nullability
            schema_nullable = schema_column['nullable']
            model_nullable = model_column['nullable']
            
            if schema_nullable != model_nullable:
                nullable_mismatches.append({
                    'column': column_name,
                    'schema_nullable': schema_nullable,
                    'model_nullable': model_nullable
                })
        
        if type_mismatches:
            table_discrepancies['type_mismatches'] = type_mismatches
        
        if nullable_mismatches:
            table_discrepancies['nullable_mismatches'] = nullable_mismatches
        
        # Compare primary keys
        schema_pk = set(db_schema[table_name]['primary_key'])
        model_pk = set(models[table_name]['primary_key'])
        
        if schema_pk != model_pk:
            table_discrepancies['primary_key_mismatch'] = {
                'schema_pk': list(schema_pk),
                'model_pk': list(model_pk)
            }
        
        # Compare foreign keys
        schema_fks = db_schema[table_name]['foreign_keys']
        model_fks = models[table_name]['foreign_keys']
        
        # Convert to sets for comparison
        schema_fk_set = {(fk['column'], fk['references']['table'], fk['references']['column']) for fk in schema_fks}
        model_fk_set = {(fk['column'], fk['references']['table'], fk['references']['column']) for fk in model_fks}
        
        fks_only_in_schema = schema_fk_set - model_fk_set
        fks_only_in_models = model_fk_set - schema_fk_set
        
        if fks_only_in_schema:
            table_discrepancies['foreign_keys_only_in_schema'] = [
                {'column': col, 'references': {'table': table, 'column': ref_col}}
                for col, table, ref_col in fks_only_in_schema
            ]
        
        if fks_only_in_models:
            table_discrepancies['foreign_keys_only_in_models'] = [
                {'column': col, 'references': {'table': table, 'column': ref_col}}
                for col, table, ref_col in fks_only_in_models
            ]
        
        # Add table discrepancies to overall discrepancies
        if table_discrepancies:
            discrepancies[table_name] = table_discrepancies
    
    return discrepancies


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def timestamp_str():
    """Generate timestamp string for file naming."""
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def ensure_reports_dir():
    """Ensure the schema reports directory exists."""
    reports_dir = ".roo/docs/schema_reports"
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def load_latest_file(pattern):
    """Load the most recent file matching the pattern."""
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def load_json(filepath):
    """Load JSON from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def write_json(filepath, data):
    """Write JSON to file with proper formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def build_compare_schema_from_introspect(introspect_data):
    """
    Convert introspect JSON format to the comparison format expected by compare_schema_with_models.
    
    Args:
        introspect_data: Dict with 'metadata' and 'schema' keys
        
    Returns:
        Dict in comparison format with table->columns/primary_key/foreign_keys structure
    """
    schema_map = {}
    raw_schema = introspect_data.get("schema", {})
    
    for table_name, table_info in raw_schema.items():
        columns_dict = {}
        for col in table_info.get("columns", []):
            columns_dict[col["name"]] = {
                "type": col["type"],
                "nullable": col["nullable"],
                "length": None  # Can be extracted from type string if needed
            }
        
        # Build foreign keys list
        fks = []
        for fk in table_info.get("foreign_keys", []):
            constrained = fk.get("constrained_columns", [])
            referred_table = fk.get("referred_table")
            referred_cols = fk.get("referred_columns", [])
            # Pair up columns (assume 1:1 for simplicity)
            for i, col in enumerate(constrained):
                ref_col = referred_cols[i] if i < len(referred_cols) else referred_cols[0]
                fks.append({
                    "column": col,
                    "references": {
                        "table": referred_table,
                        "column": ref_col
                    }
                })
        
        schema_map[table_name] = {
            "columns": columns_dict,
            "primary_key": table_info.get("primary_keys", []),
            "foreign_keys": fks
        }
    
    return schema_map


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def categorize_discrepancies(discrepancies):
    """
    Categorize discrepancies into severity levels.
    
    Returns dict with 'critical', 'warning', 'info' lists.
    """
    categories = {
        "critical": [],
        "warning": [],
        "info": []
    }
    
    # Tables only in schema or models are critical
    if "tables_only_in_schema" in discrepancies:
        for table in discrepancies["tables_only_in_schema"]:
            categories["critical"].append(f"Table '{table}' exists in DB but missing from models")
    
    if "tables_only_in_models" in discrepancies:
        for table in discrepancies["tables_only_in_models"]:
            categories["critical"].append(f"Table '{table}' defined in models but missing from DB")
    
    # Per-table discrepancies
    for table_name, issues in discrepancies.items():
        if table_name in ["tables_only_in_schema", "tables_only_in_models"]:
            continue
        
        # Missing columns are critical
        if "columns_only_in_schema" in issues:
            for col in issues["columns_only_in_schema"]:
                categories["critical"].append(f"Table '{table_name}': Column '{col}' in DB but not in model")
        
        if "columns_only_in_models" in issues:
            for col in issues["columns_only_in_models"]:
                categories["critical"].append(f"Table '{table_name}': Column '{col}' in model but not in DB")
        
        # Type mismatches are warnings
        if "type_mismatches" in issues:
            for mismatch in issues["type_mismatches"]:
                categories["warning"].append(
                    f"Table '{table_name}': Column '{mismatch['column']}' type mismatch "
                    f"(DB: {mismatch['schema_type']}, Model: {mismatch['model_type']})"
                )
        
        # Nullable mismatches are warnings
        if "nullable_mismatches" in issues:
            for mismatch in issues["nullable_mismatches"]:
                categories["warning"].append(
                    f"Table '{table_name}': Column '{mismatch['column']}' nullable mismatch "
                    f"(DB: {mismatch['schema_nullable']}, Model: {mismatch['model_nullable']})"
                )
        
        # PK and FK mismatches are critical
        if "primary_key_mismatch" in issues:
            categories["critical"].append(
                f"Table '{table_name}': Primary key mismatch "
                f"(DB: {issues['primary_key_mismatch']['schema_pk']}, "
                f"Model: {issues['primary_key_mismatch']['model_pk']})"
            )
        
        if "foreign_keys_only_in_schema" in issues:
            for fk in issues["foreign_keys_only_in_schema"]:
                categories["info"].append(
                    f"Table '{table_name}': FK '{fk['column']}' in DB but not in model"
                )
        
        if "foreign_keys_only_in_models" in issues:
            for fk in issues["foreign_keys_only_in_models"]:
                categories["info"].append(
                    f"Table '{table_name}': FK '{fk['column']}' in model but not in DB"
                )
    
    return categories


# [Created] by anthropic/claude-sonnet-4.5 | 2025-10-26_1
def generate_summary_markdown(comparison_files):
    """
    Generate a human-readable markdown summary from comparison JSON files.
    
    Args:
        comparison_files: List of paths to comparison JSON files
        
    Returns:
        str: Markdown formatted summary
    """
    md = "# Schema Comparison Summary\n\n"
    md += f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n"
    
    for filepath in comparison_files:
        data = load_json(filepath)
        metadata = data.get("metadata", {})
        command = metadata.get("command", "unknown")
        timestamp = metadata.get("timestamp", "unknown")
        
        md += f"## {command}\n\n"
        md += f"- Timestamp: {timestamp}\n"
        md += f"- Sources: {metadata.get('sources', {})}\n\n"
        
        categories = data.get("categories", {})
        
        if categories.get("critical"):
            md += "### Critical Issues\n\n"
            for issue in categories["critical"]:
                md += f"- {issue}\n"
            md += "\n"
        
        if categories.get("warning"):
            md += "### Warnings\n\n"
            for issue in categories["warning"]:
                md += f"- {issue}\n"
            md += "\n"
        
        if categories.get("info"):
            md += "### Info\n\n"
            for issue in categories["info"]:
                md += f"- {issue}\n"
            md += "\n"
        
        if not any(categories.values()):
            md += "*No discrepancies found*\n\n"
    
    return md