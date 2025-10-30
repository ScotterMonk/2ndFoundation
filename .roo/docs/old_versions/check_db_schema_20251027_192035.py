import psycopg2
from psycopg2 import sql

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="15.204.9.144",
    port="5433",
    database="MediaShare",
    user="postgres",
    password="hG887lh2Kkf83qRE5bh"
)

try:
    cursor = conn.cursor()
    
    # Check if the users table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'users'
        );
    """)
    table_exists = cursor.fetchone()[0]
    print(f"Users table exists: {table_exists}")
    
    if table_exists:
        # Get column information for the users table
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = 'users'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\nUsers table columns:")
        print("--------------------")
        for column in columns:
            print(f"Column: {column[0]}, Type: {column[1]}, Nullable: {column[2]}")
    
    # Check if the users_types table exists (needed for foreign key)
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'users_types'
        );
    """)
    users_types_exists = cursor.fetchone()[0]
    print(f"\nUsers_types table exists: {users_types_exists}")
    
    # Get column information for users_types table
    if users_types_exists:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = 'users_types'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\nUsers_types table columns:")
        print("-------------------------")
        for column in columns:
            print(f"Column: {column[0]}, Type: {column[1]}, Nullable: {column[2]}")
    
    # List all tables in the database
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    print("\nAll tables in database:")
    print("----------------------")
    for table in tables:
        print(table[0])
        
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()