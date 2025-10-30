#!/usr/bin/env python3
"""
Compare the actual database schema with the documented schema to identify differences.
"""

import re
import os

def parse_markdown_schema(file_path):
    """Parse a markdown schema file and return structured data"""
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tables = {}
    current_table = None
    current_section = None
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Table header
        if line.startswith('### '):
            table_name = line[4:].strip()
            if table_name.startswith('view: '):
                table_name = table_name[6:]
                table_type = 'view'
            else:
                table_type = 'table'
            
            current_table = table_name
            tables[current_table] = {
                'type': table_type,
                'primary_keys': [],
                'columns': {},
                'foreign_keys': {}
            }
            current_section = None
        
        # Primary key
        elif line.startswith('**Primary Key:**'):
            if current_table:
                pk_info = line[16:].strip()
                if pk_info:
                    tables[current_table]['primary_keys'] = [pk.strip() for pk in pk_info.split(',')]
        
        # Section headers
        elif line == '**Columns:**':
            current_section = 'columns'
        elif line == '**Foreign Keys:**':
            current_section = 'foreign_keys'
        
        # Column or FK entries
        elif line.startswith('- `') and current_table:
            if current_section == 'columns':
                # Parse column: - `column_name`: data_type NULL/NOT NULL
                match = re.match(r'- `([^`]+)`:\s*(.+)', line)
                if match:
                    col_name = match.group(1)
                    col_info = match.group(2)
                    tables[current_table]['columns'][col_name] = col_info
            
            elif current_section == 'foreign_keys':
                # Parse FK: - `column` -> `table.column`
                match = re.match(r'- `([^`]+)`\s*->\s*`([^.]+)\.([^`]+)`', line)
                if match:
                    fk_column = match.group(1)
                    ref_table = match.group(2)
                    ref_column = match.group(3)
                    tables[current_table]['foreign_keys'][fk_column] = f"{ref_table}.{ref_column}"
    
    return tables

def compare_schemas():
    """Compare the actual schema with the documented schema"""
    print("Comparing schemas...")
    
    actual_schema = parse_markdown_schema('database_schema_actual.md')
    documented_schema = parse_markdown_schema('.github/docs/database_schema.md')
    
    print(f"Actual schema has {len(actual_schema)} tables/views")
    print(f"Documented schema has {len(documented_schema)} tables/views")
    print()
    
    # Find missing tables in documentation
    missing_in_docs = set(actual_schema.keys()) - set(documented_schema.keys())
    if missing_in_docs:
        print("MISSING IN DOCUMENTATION:")
        for table in sorted(missing_in_docs):
            print(f"  - {table} ({actual_schema[table]['type']})")
        print()
    
    # Find extra tables in documentation
    extra_in_docs = set(documented_schema.keys()) - set(actual_schema.keys())
    if extra_in_docs:
        print("EXTRA IN DOCUMENTATION (not in database):")
        for table in sorted(extra_in_docs):
            print(f"  - {table}")
        print()
    
    # Compare common tables
    common_tables = set(actual_schema.keys()) & set(documented_schema.keys())
    discrepancies = []
    
    for table in sorted(common_tables):
        actual = actual_schema[table]
        documented = documented_schema[table]
        
        table_issues = []
        
        # Compare primary keys
        if set(actual['primary_keys']) != set(documented['primary_keys']):
            table_issues.append(f"Primary keys differ: actual={actual['primary_keys']}, documented={documented['primary_keys']}")
        
        # Compare columns
        actual_columns = set(actual['columns'].keys())
        documented_columns = set(documented['columns'].keys())
        
        if actual_columns != documented_columns:
            missing_cols = actual_columns - documented_columns
            extra_cols = documented_columns - actual_columns
            
            if missing_cols:
                table_issues.append(f"Missing columns in docs: {sorted(missing_cols)}")
            if extra_cols:
                table_issues.append(f"Extra columns in docs: {sorted(extra_cols)}")
        
        # Compare column types for common columns
        common_columns = actual_columns & documented_columns
        for col in common_columns:
            if actual['columns'][col] != documented['columns'][col]:
                table_issues.append(f"Column '{col}' type differs: actual='{actual['columns'][col]}', documented='{documented['columns'][col]}'")
        
        # Compare foreign keys
        if actual['foreign_keys'] != documented['foreign_keys']:
            actual_fks = set(actual['foreign_keys'].items())
            documented_fks = set(documented['foreign_keys'].items())
            
            missing_fks = actual_fks - documented_fks
            extra_fks = documented_fks - actual_fks
            
            if missing_fks:
                table_issues.append(f"Missing FKs in docs: {dict(missing_fks)}")
            if extra_fks:
                table_issues.append(f"Extra FKs in docs: {dict(extra_fks)}")
        
        if table_issues:
            discrepancies.append((table, table_issues))
    
    if discrepancies:
        print(f"DISCREPANCIES IN {len(discrepancies)} TABLES:")
        for table, issues in discrepancies:
            print(f"\n{table}:")
            for issue in issues:
                print(f"  - {issue}")
    else:
        print("No discrepancies found in common tables!")
    
    print(f"\nSUMMARY:")
    print(f"- Tables missing from docs: {len(missing_in_docs)}")
    print(f"- Extra tables in docs: {len(extra_in_docs)}")
    print(f"- Tables with discrepancies: {len(discrepancies)}")

if __name__ == "__main__":
    compare_schemas()
