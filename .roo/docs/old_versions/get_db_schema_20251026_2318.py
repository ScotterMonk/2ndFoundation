import psycopg2
import json
import os

# Database credentials from docs/database_credentials.md
DB_HOST = "15.204.9.144"
DB_PORT = "5433"
DB_NAME = "MediaShare"
DB_USER = "postgres"
DB_PASSWORD = "hG887lh2Kkf83qRE5bh"

def get_db_schema():
    schema = {}
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        # Query information_schema.columns for tables in the public schema
        cur.execute("""
            SELECT table_name, column_name, udt_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)

        for row in cur:
            table_name, column_name, udt_name = row
            if table_name not in schema:
                schema[table_name] = {"columns": {}}
            schema[table_name]["columns"][column_name] = udt_name
        
        return json.dumps(schema, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    print(get_db_schema())