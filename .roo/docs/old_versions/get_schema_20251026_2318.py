#!/usr/bin/env python3
"""
get_schema.py - Extract PostgreSQL database schema and format it as markdown

This script connects to a PostgreSQL database using credentials from a markdown file,
extracts the schema information (tables, columns, data types, constraints), and
formats it into a markdown file.
"""

import os
import re
import sys
import datetime
import psycopg2
from psycopg2 import sql

def read_credentials(file_path):
    """
    Read database credentials from a markdown file.
    
    Args:
        file_path (str): Path to the markdown file containing credentials
        
    Returns:
        dict: Dictionary containing database connection parameters
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Extract credentials using regex
        host_match = re.search(r'Host:\s*([^\n]+)', content)
        port_match = re.search(r'Port:\s*([^\n]+)', content)
        db_match = re.search(r'Database:\s*([^\n]+)', content)
        user_match = re.search(r'Username:\s*([^\n]+)', content)
        pw_match = re.search(r'PW:\s*([^\n]+)', content)
        
        if not all([host_match, port_match, db_match, user_match, pw_match]):
            raise ValueError("Could not extract all required credentials from the file")
        
        credentials = {
            'host': host_match.group(1).strip(),
            'port': port_match.group(1).strip(),
            'database': db_match.group(1).strip(),
            'user': user_match.group(1).strip(),
            'password': pw_match.group(1).strip()
        }
        
        return credentials
    
    except Exception as e:
        print(f"Error reading credentials: {e}")
        sys.exit(1)

def get_tables(cursor):
    """
    Get all tables in the public schema.
    
    Args:
        cursor: Database cursor
        
    Returns:
        list: List of table names
    """
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    return [row[0] for row in cursor.fetchall()]

def get_views(cursor):
    """
    Get all views in the public schema.
    
    Args:
        cursor: Database cursor
        
    Returns:
        list: List of view names
    """
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'VIEW'
        ORDER BY table_name;
    """)
    return [row[0] for row in cursor.fetchall()]

def get_columns(cursor, table_name):
    """
    Get all columns for a specific table.
    
    Args:
        cursor: Database cursor
        table_name (str): Name of the table
        
    Returns:
        list: List of column information dictionaries
    """
    cursor.execute("""
        SELECT column_name, 
               data_type, 
               character_maximum_length,
               is_nullable, 
               column_default,
               numeric_precision,
               numeric_scale
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    
    columns = []
    for row in cursor.fetchall():
        column_name, data_type, char_max_length, is_nullable, default, num_precision, num_scale = row
        
        # Format data type with length/precision if applicable
        if char_max_length is not None:
            data_type = f"{data_type}({char_max_length})"
        elif data_type == 'numeric' and num_precision is not None:
            if num_scale is not None:
                data_type = f"{data_type}({num_precision},{num_scale})"
            else:
                data_type = f"{data_type}({num_precision})"
        
        # Format nullability
        nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
        
        columns.append({
            'name': column_name,
            'type': data_type,
            'nullable': nullable,
            'default': default
        })
    
    return columns

def get_primary_key(cursor, table_name):
    """
    Get the primary key for a specific table.
    
    Args:
        cursor: Database cursor
        table_name (str): Name of the table
        
    Returns:
        list: List of primary key column names
    """
    cursor.execute("""
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = %s::regclass
        AND    i.indisprimary;
    """, (table_name,))
    
    return [row[0] for row in cursor.fetchall()]

def get_foreign_keys(cursor, table_name):
    """
    Get all foreign keys for a specific table.
    
    Args:
        cursor: Database cursor
        table_name (str): Name of the table
        
    Returns:
        list: List of foreign key dictionaries
    """
    cursor.execute("""
        SELECT
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_name = %s;
    """, (table_name,))
    
    foreign_keys = []
    for row in cursor.fetchall():
        column_name, foreign_table, foreign_column = row
        foreign_keys.append({
            'column': column_name,
            'references': {
                'table': foreign_table,
                'column': foreign_column
            }
        })
    
    return foreign_keys

def format_schema_as_markdown(tables_info, views_info):
    """
    Format the schema information as markdown.
    
    Args:
        tables_info (dict): Dictionary containing table information
        views_info (dict): Dictionary containing view information
        
    Returns:
        str: Markdown formatted schema
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown = f"# Database Schema Overview\n\n"
    markdown += f"*Last updated: {current_time}*\n\n"
    markdown += "## Tables\n\n"
    
    # First add views
    for view_name, view_info in views_info.items():
        markdown += f"### view: {view_name}\n\n"
        
        markdown += "**Columns:**\n"
        for column in view_info['columns']:
            markdown += f"- `{column['name']}`: {column['type']} {column['nullable']}\n"
        
        markdown += "\n"
    
    # Then add tables
    for table_name, table_info in tables_info.items():
        markdown += f"### {table_name}\n\n"
        
        if table_info['primary_key']:
            pk_columns = ", ".join(table_info['primary_key'])
            markdown += f"**Primary Key:** {pk_columns}\n\n"
        
        markdown += "**Columns:**\n"
        for column in table_info['columns']:
            markdown += f"- `{column['name']}`: {column['type']} {column['nullable']}\n"
        
        markdown += "\n"
        
        if table_info['foreign_keys']:
            markdown += "**Foreign Keys:**\n"
            for fk in table_info['foreign_keys']:
                markdown += f"- `{fk['column']}` -> `{fk['references']['table']}.{fk['references']['column']}`\n"
            
            markdown += "\n"
    
    return markdown

def main():
    """
    Main function to extract schema and save as markdown.
    """
    try:
        # Read database credentials
        credentials_path = os.path.join('docs', 'database_credentials.md')
        credentials = read_credentials(credentials_path)
        
        # Connect to the database
        conn = psycopg2.connect(
            host=credentials['host'],
            port=credentials['port'],
            database=credentials['database'],
            user=credentials['user'],
            password=credentials['password']
        )
        
        cursor = conn.cursor()
        
        # Get all tables and views
        tables = get_tables(cursor)
        views = get_views(cursor)
        
        # Collect information for each table
        tables_info = {}
        for table_name in tables:
            tables_info[table_name] = {
                'columns': get_columns(cursor, table_name),
                'primary_key': get_primary_key(cursor, table_name),
                'foreign_keys': get_foreign_keys(cursor, table_name)
            }
        
        # Collect information for each view
        views_info = {}
        for view_name in views:
            views_info[view_name] = {
                'columns': get_columns(cursor, view_name)
            }
        
        # Format as markdown
        markdown = format_schema_as_markdown(tables_info, views_info)
        
        # Write to file
        output_path = '.roo/docs/database_schema.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"Schema extracted successfully and saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    main()