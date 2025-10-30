#!/usr/bin/env python3
"""
Script to generate accurate database schema documentation by querying PostgreSQL directly.
This will help identify discrepancies with the current database_schema.md file.
"""

import os
import sys
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor

# Add the app directory to sys.path to import config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from urllib.parse import urlparse

def get_database_connection():
    """Get database connection using app config"""
    try:
        # Use DATABASE_URL if available, otherwise construct from individual components
        if hasattr(Config, 'DATABASE_URL') and Config.DATABASE_URL:
            database_url = Config.DATABASE_URL
        else:
            # Construct from individual components
            db_host = os.getenv('DB_HOST', '15.204.9.144')
            db_port = os.getenv('DB_PORT', '5433')
            db_name = os.getenv('DB_NAME', 'master')
            db_user = os.getenv('DB_USER', 'postgres')
            db_password = os.getenv('DB_PASSWORD', 'fooblitsky')
            database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        
        # Parse the database URL
        parsed = urlparse(database_url)
        
        conn = psycopg2.connect(
            host=parsed.hostname,
            database=parsed.path.lstrip('/'),
            user=parsed.username,
            password=parsed.password,
            port=parsed.port or 5433
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print(f"Database URL: {database_url if 'database_url' in locals() else 'Not set'}")
        return None

def get_all_tables(cursor):
    """Get all tables and views from the database"""
    query = """
    SELECT 
        schemaname,
        tablename as name,
        'table' as type
    FROM pg_tables 
    WHERE schemaname = 'public'
    
    UNION ALL
    
    SELECT 
        schemaname,
        viewname as name,
        'view' as type
    FROM pg_views 
    WHERE schemaname = 'public'
    
    ORDER BY name;
    """
    cursor.execute(query)
    return cursor.fetchall()

def get_table_columns(cursor, table_name):
    """Get detailed column information for a table"""
    query = """
    SELECT 
        c.column_name,
        c.data_type,
        c.character_maximum_length,
        c.numeric_precision,
        c.numeric_scale,
        c.is_nullable,
        c.column_default,
        c.udt_name,
        CASE 
            WHEN c.data_type = 'ARRAY' THEN c.udt_name
            WHEN c.data_type = 'USER-DEFINED' THEN c.udt_name
            ELSE c.data_type
        END as full_type
    FROM information_schema.columns c
    WHERE c.table_schema = 'public' 
    AND c.table_name = %s
    ORDER BY c.ordinal_position;
    """
    cursor.execute(query, (table_name,))
    return cursor.fetchall()

def get_primary_keys(cursor, table_name):
    """Get primary key information for a table"""
    query = """
    SELECT kcu.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
    WHERE tc.table_schema = 'public'
    AND tc.table_name = %s
    AND tc.constraint_type = 'PRIMARY KEY'
    ORDER BY kcu.ordinal_position;
    """
    cursor.execute(query, (table_name,))
    return [row['column_name'] for row in cursor.fetchall()]

def get_foreign_keys(cursor, table_name):
    """Get foreign key information for a table"""
    query = """
    SELECT
        kcu.column_name,
        ccu.table_name AS referenced_table,
        ccu.column_name AS referenced_column
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu 
        ON ccu.constraint_name = tc.constraint_name
    WHERE tc.table_schema = 'public'
    AND tc.table_name = %s
    AND tc.constraint_type = 'FOREIGN KEY'
    ORDER BY kcu.column_name;
    """
    cursor.execute(query, (table_name,))
    return cursor.fetchall()

def format_data_type(column):
    """Format the data type string for display"""
    data_type = column['data_type']
    full_type = column['full_type']
    
    # Handle specific PostgreSQL types
    if data_type == 'character varying':
        if column['character_maximum_length']:
            return f"character varying({column['character_maximum_length']})"
        else:
            return "character varying"
    elif data_type == 'character':
        if column['character_maximum_length']:
            return f"character({column['character_maximum_length']})"
        else:
            return "character"
    elif data_type == 'numeric':
        if column['numeric_precision'] and column['numeric_scale']:
            return f"numeric({column['numeric_precision']},{column['numeric_scale']})"
        elif column['numeric_precision']:
            return f"numeric({column['numeric_precision']})"
        else:
            return "numeric"
    elif data_type == 'timestamp with time zone':
        return "timestamp with time zone"
    elif data_type == 'timestamp without time zone':
        return "timestamp without time zone"
    elif data_type == 'ARRAY':
        return f"{full_type}[]"
    elif data_type == 'USER-DEFINED':
        return full_type
    elif full_type in ['int4', 'integer']:
        return "integer"
    elif full_type == 'int8':
        return "bigint"
    elif full_type == 'float4':
        return "real"
    elif full_type == 'float8':
        return "double precision"
    elif full_type == 'bool':
        return "boolean"
    elif full_type == 'varchar':
        return "character varying"
    elif full_type == 'timestamptz':
        return "timestamp with time zone"
    else:
        return data_type

def generate_schema_markdown(cursor):
    """Generate the complete schema documentation in markdown format"""
    tables = get_all_tables(cursor)
    
    # Generate markdown content
    content = f"# Database Schema Overview\n\n"
    content += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    content += "## Tables\n\n"
    
    for table in tables:
        table_name = table['name']
        table_type = table['type']
        
        # Add table header
        if table_type == 'view':
            content += f"### view: {table_name}\n\n"
        else:
            content += f"### {table_name}\n\n"
        
        # Get primary keys
        primary_keys = get_primary_keys(cursor, table_name)
        if primary_keys:
            if len(primary_keys) == 1:
                content += f"**Primary Key:** {primary_keys[0]}\n\n"
            else:
                content += f"**Primary Key:** {', '.join(primary_keys)}\n\n"
        
        # Get columns
        columns = get_table_columns(cursor, table_name)
        content += "**Columns:**\n"
        for column in columns:
            column_name = column['column_name']
            data_type = format_data_type(column)
            is_nullable = "NULL" if column['is_nullable'] == 'YES' else "NOT NULL"
            content += f"- `{column_name}`: {data_type} {is_nullable}\n"
        
        content += "\n"
        
        # Get foreign keys
        foreign_keys = get_foreign_keys(cursor, table_name)
        if foreign_keys:
            content += "**Foreign Keys:**\n"
            for fk in foreign_keys:
                content += f"- `{fk['column_name']}` -> `{fk['referenced_table']}.{fk['referenced_column']}`\n"
            content += "\n"
    
    return content

def main():
    print("Connecting to PostgreSQL database...")
    conn = get_database_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("Generating schema documentation...")
        schema_content = generate_schema_markdown(cursor)
        
        # Write to file
        output_file = "database_schema_actual.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(schema_content)
        
        print(f"Schema documentation generated successfully: {output_file}")
        
        # Get basic stats
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
        table_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public'")
        view_count = cursor.fetchone()['count']
        
        print(f"Database contains {table_count} tables and {view_count} views")
        
    except Exception as e:
        print(f"Error generating schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
