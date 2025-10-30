#!/usr/bin/env python3
"""
compare_models.py - Compare SQLAlchemy models with actual database schema

This script reads the actual database schema from .roo/docs/database_schema.md and compares it
with the SQLAlchemy model definitions in the models directory. It identifies
discrepancies such as missing columns, type mismatches, and other inconsistencies.
"""

import os
import re
import sys
import importlib.util
import inspect
import datetime  # Import here for use in the report timestamp
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, INET
# Removed unused markdown import

# Import Flask app creation function
from app import create_app
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
    'varchar': 'Text',
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

def parse_actual_schema(file_path):
    """
    Parse the .roo/docs/database_schema.md file to extract table information.
    
    Args:
        file_path (str): Path to the .roo/docs/database_schema.md file
        
    Returns:
        dict: Dictionary of tables with their columns and properties
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tables = {}
        current_table = None
        in_columns = False
        in_foreign_keys = False
        
        # Skip views
        content = re.sub(r'### view:.*?(?=###|\Z)', '', content, flags=re.DOTALL)
        
        # Extract tables
        table_sections = re.findall(r'### ([^\n]+)(.*?)(?=### |\Z)', content, re.DOTALL)
        
        for table_name, table_content in table_sections:
            table_name = table_name.strip()
            tables[table_name] = {
                'columns': {},
                'primary_key': [],
                'foreign_keys': []
            }
            
            # Extract primary key
            pk_match = re.search(r'\*\*Primary Key:\*\* ([^\n]+)', table_content)
            if pk_match:
                tables[table_name]['primary_key'] = [pk.strip() for pk in pk_match.group(1).split(',')]
            
            # Extract columns
            column_matches = re.findall(r'- `([^`]+)`: ([^`\n]+) (NULL|NOT NULL)', table_content)
            for col_name, col_type, nullable in column_matches:
                # Extract length/precision if present
                length_match = re.search(r'([a-z ]+)\(([^)]+)\)', col_type)
                if length_match:
                    base_type = length_match.group(1).strip()
                    length = length_match.group(2).strip()
                    tables[table_name]['columns'][col_name] = {
                        'type': base_type,
                        'length': length,
                        'nullable': nullable == 'NULL'
                    }
                else:
                    tables[table_name]['columns'][col_name] = {
                        'type': col_type.strip(),
                        'nullable': nullable == 'NULL'
                    }
            
            # Extract foreign keys
            fk_matches = re.findall(r'- `([^`]+)` -> `([^`]+)\.([^`]+)`', table_content)
            for col_name, ref_table, ref_col in fk_matches:
                tables[table_name]['foreign_keys'].append({
                    'column': col_name,
                    'references': {
                        'table': ref_table,
                        'column': ref_col
                    }
                })
        
        return tables
    
    except Exception as e:
        print(f"Error parsing actual schema: {e}")
        sys.exit(1)

def get_sqlalchemy_models(model_files):
    """
    Extract SQLAlchemy model definitions from model files.

    Args:
        model_files (list): List of model file paths

    Returns:
        dict: Dictionary of models with their columns and properties
    """
    # [Modified] by openai/gpt-5 | 2025-10-26_2
    # Root cause: Using spec_from_file_location to exec model files creates duplicate
    # Table objects in the same MetaData when the app has already imported models
    # (via blueprints/initialization). That triggered "Table ... is already defined".
    # Fix: Import modules by package name (importlib.import_module) to respect sys.modules
    # and then enumerate mapped classes via Flask-SQLAlchemy registry.
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

def generate_report(discrepancies, models, output_file):
    """
    Generate a markdown report of discrepancies.
    
    Args:
        discrepancies (dict): Dictionary of discrepancies
        models (dict): Dictionary of SQLAlchemy models
        output_file (str): Path to output file
    """
    report = "# Model Comparison Results\n\n"
    report += f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    # Summary
    report += "## Summary\n\n"
    
    total_tables = len(discrepancies.keys())
    if 'tables_only_in_schema' in discrepancies:
        total_tables -= 1
    if 'tables_only_in_models' in discrepancies:
        total_tables -= 1
    
    report += f"- **Tables with discrepancies:** {total_tables}\n"
    
    if 'tables_only_in_schema' in discrepancies:
        report += f"- **Tables only in database:** {len(discrepancies['tables_only_in_schema'])}\n"
    
    if 'tables_only_in_models' in discrepancies:
        report += f"- **Tables only in models:** {len(discrepancies['tables_only_in_models'])}\n"
    
    # Tables only in schema
    if 'tables_only_in_schema' in discrepancies:
        report += "\n## Tables Only in Database\n\n"
        for table in discrepancies['tables_only_in_schema']:
            report += f"- `{table}`\n"
    
    # Tables only in models
    if 'tables_only_in_models' in discrepancies:
        report += "\n## Tables Only in Models\n\n"
        for table in discrepancies['tables_only_in_models']:
            model_class = models[table]['class_name']
            report += f"- `{table}` (Model class: `{model_class}`)\n"
    
    # Table-specific discrepancies
    for table_name, table_discrepancies in discrepancies.items():
        if table_name in ['tables_only_in_schema', 'tables_only_in_models']:
            continue
        
        report += f"\n## {table_name}\n\n"
        
        if 'columns_only_in_schema' in table_discrepancies:
            report += "### Columns in Database but Missing from Model\n\n"
            for column in table_discrepancies['columns_only_in_schema']:
                report += f"- `{column}`\n"
        
        if 'columns_only_in_models' in table_discrepancies:
            report += "\n### Columns in Model but Missing from Database\n\n"
            for column in table_discrepancies['columns_only_in_models']:
                report += f"- `{column}`\n"
        
        if 'type_mismatches' in table_discrepancies:
            report += "\n### Type Mismatches\n\n"
            report += "| Column | Database Type | Model Type |\n"
            report += "|--------|--------------|------------|\n"
            for mismatch in table_discrepancies['type_mismatches']:
                report += f"| `{mismatch['column']}` | {mismatch['schema_type']} | {mismatch['model_type']} |\n"
        
        if 'nullable_mismatches' in table_discrepancies:
            report += "\n### Nullability Mismatches\n\n"
            report += "| Column | Database | Model |\n"
            report += "|--------|----------|-------|\n"
            for mismatch in table_discrepancies['nullable_mismatches']:
                db_null = "NULL" if mismatch['schema_nullable'] else "NOT NULL"
                model_null = "nullable=True" if mismatch['model_nullable'] else "nullable=False"
                report += f"| `{mismatch['column']}` | {db_null} | {model_null} |\n"
        
        if 'primary_key_mismatch' in table_discrepancies:
            report += "\n### Primary Key Mismatch\n\n"
            schema_pk = ", ".join([f"`{pk}`" for pk in table_discrepancies['primary_key_mismatch']['schema_pk']])
            model_pk = ", ".join([f"`{pk}`" for pk in table_discrepancies['primary_key_mismatch']['model_pk']])
            report += f"- **Database:** {schema_pk}\n"
            report += f"- **Model:** {model_pk}\n"
        
        if 'foreign_keys_only_in_schema' in table_discrepancies:
            report += "\n### Foreign Keys in Database but Missing from Model\n\n"
            for fk in table_discrepancies['foreign_keys_only_in_schema']:
                report += f"- `{fk['column']}` -> `{fk['references']['table']}.{fk['references']['column']}`\n"
        
        if 'foreign_keys_only_in_models' in table_discrepancies:
            report += "\n### Foreign Keys in Model but Missing from Database\n\n"
            for fk in table_discrepancies['foreign_keys_only_in_models']:
                report += f"- `{fk['column']}` -> `{fk['references']['table']}.{fk['references']['column']}`\n"
    
    # Write report to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report generated successfully and saved to {output_file}")

def main():
    """
    Main function to compare models with schema and generate report.
    
    This function creates a Flask application context to ensure that
    SQLAlchemy models can be properly accessed and inspected.
    """
    try:
        # Check if .roo/docs/database_schema.md exists
        if not os.path.exists('.roo/docs/database_schema.md'):
            print("Error: .roo/docs/database_schema.md not found. Please run get_schema.py first.")
            sys.exit(1)
        
        # Define model files to check
        model_files = [
            'models/models_interaction.py',
            'models/models_media.py',
            'models/models_payment.py',
            'models/models_referral.py',
            'models/models_reseller.py',
            'models/models_support.py',
            'models/models_user.py'
        ]
        
        # Check if all model files exist
        for file_path in model_files:
            if not os.path.exists(file_path):
                print(f"Error: Model file {file_path} not found.")
                sys.exit(1)
        
        # Parse actual schema (this doesn't need app context)
        print("Parsing actual database schema...")
        db_schema = parse_actual_schema('.roo/docs/database_schema.md')
        
        # Create Flask app and application context
        print("Creating Flask application context...")
        app = create_app()
        
        # Run model inspection within Flask application context
        with app.app_context():
            try:
                # Extract SQLAlchemy models
                print("Extracting SQLAlchemy models...")
                models = get_sqlalchemy_models(model_files)
                
                # Compare schema with models
                print("Comparing schema with models...")
                discrepancies = compare_schema_with_models(db_schema, models)
                
                # Generate report
                print("Generating report...")
                generate_report(discrepancies, models, 'model_comparison_results.md')
                
            except Exception as e:
                print(f"Error within application context: {e}")
                sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()