import json

def compare_schemas(model_schema, doc_schema):
    """
    Compare SQLAlchemy model schema with documentation schema to identify discrepancies.
    
    Args:
        model_schema: Dictionary containing SQLAlchemy model definitions
        doc_schema: Dictionary containing documentation schema definitions
        
    Returns:
        Dictionary containing all discrepancies found
    """
    # Extract all table names from model schema
    model_tables = {}
    for file_name, models in model_schema.items():
        for model_name, model_info in models.items():
            table_name = model_info["table_name"]
            model_tables[table_name] = {
                "source_file": file_name,
                "model_name": model_name,
                "columns": model_info["columns"]
            }
    
    # Find tables in model schema but not in doc schema
    model_only_tables = set(model_tables.keys()) - set(doc_schema.keys())
    
    # Find tables in doc schema but not in model schema
    doc_only_tables = set(doc_schema.keys()) - set(model_tables.keys())
    
    # Compare columns and data types for tables present in both schemas
    column_discrepancies = {}
    data_type_discrepancies = {}
    
    for table_name in set(model_tables.keys()).intersection(set(doc_schema.keys())):
        model_columns = model_tables[table_name]["columns"]
        doc_columns = doc_schema[table_name]["columns"]
        
        # Find columns in model schema but not in doc schema
        model_only_columns = set(model_columns.keys()) - set(doc_columns.keys())
        
        # Find columns in doc schema but not in model schema
        doc_only_columns = set(doc_columns.keys()) - set(model_columns.keys())
        
        if model_only_columns or doc_only_columns:
            column_discrepancies[table_name] = {
                "model_only": list(model_only_columns),
                "doc_only": list(doc_only_columns)
            }
        
        # Compare data types for columns present in both schemas
        type_mismatches = {}
        for column_name in set(model_columns.keys()).intersection(set(doc_columns.keys())):
            model_type = model_columns[column_name]
            doc_type = doc_columns[column_name]
            
            # Check if data types match
            if not data_types_match(model_type, doc_type):
                type_mismatches[column_name] = {
                    "model_type": model_type,
                    "doc_type": doc_type
                }
        
        if type_mismatches:
            data_type_discrepancies[table_name] = type_mismatches
    
    # Compile all discrepancies into a single report
    discrepancies = {
        "tables": {
            "model_only": list(model_only_tables),
            "doc_only": list(doc_only_tables)
        },
        "columns": column_discrepancies,
        "data_types": data_type_discrepancies
    }
    
    return discrepancies

def data_types_match(model_type, doc_type):
    """
    Check if SQLAlchemy data type matches PostgreSQL data type.
    
    Args:
        model_type: SQLAlchemy data type
        doc_type: PostgreSQL data type
        
    Returns:
        Boolean indicating whether the data types match
    """
    # Map SQLAlchemy data types to PostgreSQL data types
    sqlalchemy_to_postgres = {
        "Integer": ["integer", "int", "int4"],
        "BigInteger": ["bigint", "int8"],
        "Float": ["real", "float4", "double precision", "float8"],
        "Numeric": ["numeric", "decimal"],
        "String": ["character varying", "varchar", "character", "char", "text"],
        "Text": ["text"],
        "Boolean": ["boolean", "bool"],
        "DateTime": ["timestamp", "timestamp with time zone", "timestamp without time zone"],
        "Date": ["date"],
        "Time": ["time", "time with time zone", "time without time zone"],
        "JSON": ["json", "jsonb"],
        "ARRAY": ["ARRAY"]
    }
    
    # Extract base type from SQLAlchemy type (eg, "String(255)" -> "String")
    model_base_type = model_type.split("(")[0] if "(" in model_type else model_type
    
    # Check if PostgreSQL type matches any of the mapped SQLAlchemy types
    for sa_type, pg_types in sqlalchemy_to_postgres.items():
        if model_base_type == sa_type:
            for pg_type in pg_types:
                if pg_type in doc_type.lower():
                    return True
    
    return False

def main():
    # Load model schema
    with open('model_schema.json', 'r') as f:
        model_schema = json.load(f)
    
    # Load documentation schema
    with open('doc_schema.json', 'r') as f:
        doc_schema = json.load(f)
    
    # Compare schemas
    discrepancies = compare_schemas(model_schema, doc_schema)
    
    # Output discrepancies as JSON
    with open('schema_discrepancies.json', 'w') as f:
        json.dump(discrepancies, f, indent=2)
    
    print("Schema comparison complete. Results saved to 'schema_discrepancies.json'.")

if __name__ == "__main__":
    main()