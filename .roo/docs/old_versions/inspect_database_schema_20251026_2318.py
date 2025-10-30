"""
Database schema inspection script to generate documentation for the MediaShare application.
This script connects to the PostgreSQL database and extracts comprehensive schema information.
"""

import psycopg2
import logging
from datetime import datetime
from collections import defaultdict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Database connection parameters
DB_HOST = "15.204.9.144"
DB_PORT = "5433"
DB_NAME = "MediaShare"
DB_USER = "postgres"
DB_PASSWORD = "hG887lh2Kkf83qRE5bh"

def connect_to_db():
    """Establish connection to the database."""
    try:
        logging.info("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logging.info("Database connection successful.")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error connecting to the database: {error}")
        raise

def get_tables_info(cursor):
    """Get all tables and their basic information."""
    cursor.execute("""
        SELECT 
            table_name,
            table_type
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    return cursor.fetchall()

def get_columns_info(cursor, table_name):
    """Get detailed column information for a specific table."""
    cursor.execute("""
        SELECT 
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default,
            ordinal_position
        FROM information_schema.columns 
        WHERE table_name = %s AND table_schema = 'public'
        ORDER BY ordinal_position;
    """, (table_name,))
    return cursor.fetchall()

def get_primary_keys(cursor, table_name):
    """Get primary key information for a specific table."""
    cursor.execute("""
        SELECT 
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu 
            ON tc.constraint_name = kcu.constraint_name
        WHERE tc.table_name = %s 
            AND tc.constraint_type = 'PRIMARY KEY'
            AND tc.table_schema = 'public'
        ORDER BY kcu.ordinal_position;
    """, (table_name,))
    return [row[0] for row in cursor.fetchall()]

def get_foreign_keys(cursor, table_name):
    """Get foreign key information for a specific table."""
    cursor.execute("""
        SELECT 
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name,
            tc.constraint_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu 
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu 
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.table_name = %s 
            AND tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public';
    """, (table_name,))
    return cursor.fetchall()

def get_indexes(cursor, table_name):
    """Get index information for a specific table."""
    cursor.execute("""
        SELECT 
            indexname,
            indexdef
        FROM pg_indexes 
        WHERE tablename = %s 
            AND schemaname = 'public'
        ORDER BY indexname;
    """, (table_name,))
    return cursor.fetchall()

def get_constraints(cursor, table_name):
    """Get constraint information for a specific table."""
    cursor.execute("""
        SELECT 
            constraint_name,
            constraint_type
        FROM information_schema.table_constraints
        WHERE table_name = %s 
            AND table_schema = 'public'
            AND constraint_type IN ('CHECK', 'UNIQUE')
        ORDER BY constraint_name;
    """, (table_name,))
    return cursor.fetchall()

def generate_compressed_schema(schema_data):
    """Generate a compressed overview of the database schema."""
    content = []
    content.append("# Database Schema Overview")
    content.append("")
    content.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    content.append("")
    content.append("## Tables")
    content.append("")
    
    for table_name, table_info in schema_data.items():
        content.append(f"### {table_name}")
        content.append("")
        
        # Primary keys
        if table_info['primary_keys']:
            content.append(f"**Primary Key:** {', '.join(table_info['primary_keys'])}")
            content.append("")
        
        # Column summary
        content.append("**Columns:**")
        for col in table_info['columns']:
            col_name, data_type, max_length, is_nullable, default, _ = col
            type_info = data_type
            if max_length:
                type_info += f"({max_length})"
            nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
            content.append(f"- `{col_name}`: {type_info} {nullable}")
        content.append("")
        
        # Foreign keys summary
        if table_info['foreign_keys']:
            content.append("**Foreign Keys:**")
            for fk in table_info['foreign_keys']:
                col_name, ref_table, ref_col, constraint_name = fk
                content.append(f"- `{col_name}` → `{ref_table}.{ref_col}`")
            content.append("")
    
    return "\n".join(content)

def generate_detailed_schema(schema_data):
    """Generate detailed schema documentation."""
    content = []
    content.append("# Detailed Database Schema Structure")
    content.append("")
    content.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    content.append("")
    content.append("This document provides comprehensive details about the database schema including column types, constraints, indexes, and relationships.")
    content.append("")
    
    for table_name, table_info in schema_data.items():
        content.append(f"## Table: {table_name}")
        content.append("")
        
        # Table description
        content.append(f"**Table Type:** {table_info['table_type']}")
        content.append("")
        
        # Primary keys
        if table_info['primary_keys']:
            content.append("### Primary Keys")
            content.append("")
            for pk in table_info['primary_keys']:
                content.append(f"- `{pk}`")
            content.append("")
        
        # Columns detailed info
        content.append("### Columns")
        content.append("")
        content.append("| Column | Type | Length | Nullable | Default | Position |")
        content.append("|--------|------|--------|----------|---------|----------|")
        
        for col in table_info['columns']:
            col_name, data_type, max_length, is_nullable, default, position = col
            length_str = str(max_length) if max_length else "-"
            nullable_str = "Yes" if is_nullable == "YES" else "No"
            default_str = str(default) if default else "-"
            content.append(f"| `{col_name}` | {data_type} | {length_str} | {nullable_str} | {default_str} | {position} |")
        content.append("")
        
        # Foreign keys detailed info
        if table_info['foreign_keys']:
            content.append("### Foreign Keys")
            content.append("")
            content.append("| Column | References | Constraint Name |")
            content.append("|--------|------------|-----------------|")
            for fk in table_info['foreign_keys']:
                col_name, ref_table, ref_col, constraint_name = fk
                content.append(f"| `{col_name}` | `{ref_table}.{ref_col}` | {constraint_name} |")
            content.append("")
        
        # Indexes
        if table_info['indexes']:
            content.append("### Indexes")
            content.append("")
            for idx_name, idx_def in table_info['indexes']:
                content.append(f"**{idx_name}:**")
                content.append(f"```sql")
                content.append(f"{idx_def}")
                content.append(f"```")
                content.append("")
        
        # Constraints
        if table_info['constraints']:
            content.append("### Constraints")
            content.append("")
            for constraint_name, constraint_type in table_info['constraints']:
                content.append(f"- **{constraint_name}** ({constraint_type})")
            content.append("")
        
        content.append("---")
        content.append("")
    
    return "\n".join(content)

def inspect_database():
    """Main function to inspect database and generate schema documentation."""
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Get all tables
        tables = get_tables_info(cursor)
        logging.info(f"Found {len(tables)} tables in the database.")
        
        schema_data = {}
        
        for table_name, table_type in tables:
            logging.info(f"Processing table: {table_name}")
            
            # Get detailed information for each table
            columns = get_columns_info(cursor, table_name)
            primary_keys = get_primary_keys(cursor, table_name)
            foreign_keys = get_foreign_keys(cursor, table_name)
            indexes = get_indexes(cursor, table_name)
            constraints = get_constraints(cursor, table_name)
            
            schema_data[table_name] = {
                'table_type': table_type,
                'columns': columns,
                'primary_keys': primary_keys,
                'foreign_keys': foreign_keys,
                'indexes': indexes,
                'constraints': constraints
            }
        
        # Generate documentation
        compressed_schema = generate_compressed_schema(schema_data)
        detailed_schema = generate_detailed_schema(schema_data)
        
        # Write to files
        with open('docs/database_schema.md', 'w', encoding='utf-8') as f:
            f.write(compressed_schema)
        logging.info("Generated docs/database_schema.md")
        
        with open('docs/database_detailed_structure.md', 'w', encoding='utf-8') as f:
            f.write(detailed_schema)
        logging.info("Generated docs/database_detailed_structure.md")
        
        return schema_data
        
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error inspecting database: {error}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    try:
        logging.info("Starting database schema inspection...")
        schema_data = inspect_database()
        logging.info("Schema inspection completed successfully.")
        logging.info(f"Processed {len(schema_data)} tables.")
    except Exception as e:
        logging.error(f"Schema inspection failed: {e}")
        exit(1)