#!/usr/bin/env python3
"""
Schema Inspector command implementations (extracted to keep CLI under 400 LOC).

Implements:
- run_compare_db_models(args)
- run_compare_models_doc(args)
- run_generate_docs(args)
- run_report(args)
"""

import os
import glob
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

from sqlalchemy import inspect as sqlalchemy_inspect

from app import create_app
from utils.database import db
from utils.schema_compare_core import get_sqlalchemy_models, compare_schema_with_models
from utils.schema_doc_parser import parse_markdown_schema, to_compare_format, markdown_from_introspect
from utils.schema_compare_core import (
    timestamp_str,
    ensure_reports_dir,
    load_latest_file,
    load_json,
    write_json,
    build_compare_schema_from_introspect,
    categorize_discrepancies,
    generate_summary_markdown,
)


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def _fallback_live_introspect() -> Dict[str, Any]:
    """
    Minimal live introspection when no cached introspect report is available.
    Returns an 'introspect-like' dictionary matching utils/schema_inspector.py output.
    """
    # [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
    inspector = sqlalchemy_inspect(db.engine)
    table_names = inspector.get_table_names()
    schema = {}
    for table_name in table_names:
        # Columns
        cols = inspector.get_columns(table_name)
        processed_columns = []
        for column in cols:
            processed_columns.append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "default": column.get("default"),
                "autoincrement": column.get("autoincrement", False)
            })

        # PK
        pk = inspector.get_pk_constraint(table_name) or {}
        pk_columns = pk.get("constrained_columns", []) if pk else []

        # FKs
        fks_raw = inspector.get_foreign_keys(table_name)
        fks = []
        for fk in fks_raw:
            fks.append({
                "name": fk.get("name"),
                "constrained_columns": fk.get("constrained_columns", []),
                "referred_table": fk.get("referred_table"),
                "referred_columns": fk.get("referred_columns", []),
            })

        # Indexes
        idxs_raw = inspector.get_indexes(table_name)
        idxs = []
        for idx in idxs_raw:
            idxs.append({
                "name": idx.get("name"),
                "unique": idx.get("unique"),
                "column_names": idx.get("column_names", []),
            })

        # Unique constraints
        uniques_raw = inspector.get_unique_constraints(table_name)
        uniques = []
        for uc in uniques_raw:
            uniques.append({
                "name": uc.get("name"),
                "column_names": uc.get("column_names", []),
            })

        schema[table_name] = {
            "columns": processed_columns,
            "primary_keys": pk_columns,
            "foreign_keys": fks,
            "indexes": idxs,
            "unique_constraints": uniques,
        }

    return {
        "metadata": {
            "generator": "Schema Inspector CLI",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": "introspect",
            "database": db.engine.url.database
        },
        "schema": schema
    }


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def run_compare_db_models(args) -> Dict[str, Any]:
    """Task 2.4: Compare PGDB introspect vs ORM models and emit categorized JSON."""
    try:
        reports_dir = ensure_reports_dir()

        # Load latest introspect JSON; fallback to live
        latest_introspect = load_latest_file(os.path.join(reports_dir, "sok_introspect_*.json"))
        if latest_introspect:
            introspect_data = load_json(latest_introspect)
            introspect_source = latest_introspect
        else:
            introspect_data = _fallback_live_introspect()
            introspect_source = "live"

        db_schema_map = build_compare_schema_from_introspect(introspect_data)

        # Extract models under app context
        model_files = sorted(glob.glob("models/models_*.py"))
        app = create_app()
        with app.app_context():
            models = get_sqlalchemy_models(model_files)

        discrepancies = compare_schema_with_models(db_schema_map, models)
        categories = categorize_discrepancies(discrepancies)

        result = {
            "metadata": {
                "generator": "Schema Inspector CLI",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "command": "compare-db-models",
                "sources": {"introspect": introspect_source, "models": model_files}
            },
            "discrepancies": discrepancies,
            "categories": categories
        }

        out_path = os.path.join(reports_dir, f"sok_compare_db_models_{timestamp_str()}.json")
        write_json(out_path, result)
        print(f"DB vs Models comparison completed. Output: {out_path}")

        return {"status": "success", "command": "compare-db-models", "output_file": out_path}
    except Exception as e:
        error_msg = f"Error during compare-db-models: {str(e)}"
        print(error_msg)
        return {"status": "error", "command": "compare-db-models", "error": error_msg}


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def run_compare_models_doc(args) -> Dict[str, Any]:
    """Task 2.5: Compare ORM models vs parsed database_schema.md and emit categorized JSON."""
    try:
        reports_dir = ensure_reports_dir()

        doc_path = args.doc_path or ".roo/docs/database_schema.md"
        md_introspect_like = parse_markdown_schema(doc_path)
        doc_schema_map = to_compare_format(md_introspect_like)

        model_files = sorted(glob.glob("models/models_*.py"))
        app = create_app()
        with app.app_context():
            models = get_sqlalchemy_models(model_files)

        discrepancies = compare_schema_with_models(doc_schema_map, models)
        categories = categorize_discrepancies(discrepancies)

        result = {
            "metadata": {
                "generator": "Schema Inspector CLI",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "command": "compare-models-doc",
                "sources": {"doc": doc_path, "models": model_files}
            },
            "discrepancies": discrepancies,
            "categories": categories
        }

        out_path = os.path.join(reports_dir, f"sok_compare_models_doc_{timestamp_str()}.json")
        write_json(out_path, result)
        print(f"Models vs Doc comparison completed. Output: {out_path}")

        return {"status": "success", "command": "compare-models-doc", "output_file": out_path}
    except Exception as e:
        error_msg = f"Error during compare-models-doc: {str(e)}"
        print(error_msg)
        return {"status": "error", "command": "compare-models-doc", "error": error_msg}


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def run_generate_docs(args) -> Dict[str, Any]:
    """Task 2.6: Generate database_schema.md from cached introspect or live PGDB."""
    try:
        reports_dir = ensure_reports_dir()

        latest_introspect = load_latest_file(os.path.join(reports_dir, "sok_introspect_*.json"))
        if latest_introspect:
            introspect_like = load_json(latest_introspect)
        else:
            introspect_like = _fallback_live_introspect()

        md = markdown_from_introspect(introspect_like)
        output = args.output or ".roo/docs/database_schema.md"
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"Schema documentation generated at: {output}")
        return {"status": "success", "command": "generate-docs", "output_file": output}
    except Exception as e:
        error_msg = f"Error during generate-docs: {str(e)}"
        print(error_msg)
        return {"status": "error", "command": "generate-docs", "error": error_msg}


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def run_report(args) -> Dict[str, Any]:
    """Task 2.7: Summarize compare outputs into a human-readable markdown report."""
    try:
        reports_dir = ensure_reports_dir()
        paths: List[str] = []
        paths.extend(glob.glob(os.path.join(reports_dir, "sok_compare_db_models_*.json")))
        paths.extend(glob.glob(os.path.join(reports_dir, "sok_compare_models_doc_*.json")))
        if not paths:
            msg = "No comparison reports found to summarize."
            print(msg)
            return {"status": "error", "command": "report", "error": msg}

        summary_md = generate_summary_markdown(paths)
        out_path = os.path.join(reports_dir, f"sok_summary_{timestamp_str()}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(summary_md)

        print(f"Summary report generated: {out_path}")
        return {"status": "success", "command": "report", "output_file": out_path}
    except Exception as e:
        error_msg = f"Error during report generation: {str(e)}"
        print(error_msg)
        return {"status": "error", "command": "report", "error": error_msg}

# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_2
def _introspect_table(inspector, table_name):
    """Introspect a single table and return comprehensive schema information."""
    try:
        columns = inspector.get_columns(table_name)
        primary_keys = inspector.get_pk_constraint(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)
        unique_constraints = inspector.get_unique_constraints(table_name)

        processed_columns = []
        for column in columns:
            processed_columns.append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "default": column.get("default"),
                "autoincrement": column.get("autoincrement", False)
            })

        pk_columns = primary_keys.get("constrained_columns", []) if primary_keys else []

        processed_foreign_keys = []
        for fk in foreign_keys:
            processed_foreign_keys.append({
                "name": fk.get("name"),
                "constrained_columns": fk.get("constrained_columns", []),
                "referred_table": fk.get("referred_table"),
                "referred_columns": fk.get("referred_columns", [])
            })

        processed_indexes = []
        for index in indexes:
            processed_indexes.append({
                "name": index.get("name"),
                "unique": index.get("unique"),
                "column_names": index.get("column_names", [])
            })

        processed_unique_constraints = []
        for constraint in unique_constraints:
            processed_unique_constraints.append({
                "name": constraint.get("name"),
                "column_names": constraint.get("column_names", [])
            })

        return {
            "columns": processed_columns,
            "primary_keys": pk_columns,
            "foreign_keys": processed_foreign_keys,
            "indexes": processed_indexes,
            "unique_constraints": processed_unique_constraints
        }
    except Exception as e:
        return {
            "error": f"Failed to introspect table: {str(e)}",
            "columns": [],
            "primary_keys": [],
            "foreign_keys": [],
            "indexes": [],
            "unique_constraints": []
        }


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_2
def run_introspect(args):
    """Task 2.2 foundation: Introspect PGDB schema and output structure information (kept here to keep CLI thin)."""
    try:
        inspector = sqlalchemy_inspect(db.engine)

        if getattr(args, "tables", None):
            table_names = args.tables
        else:
            table_names = inspector.get_table_names()

        schema_data = {
            "metadata": {
                "generator": "Schema Inspector CLI",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "command": "introspect",
                "database": db.engine.url.database
            },
            "schema": {}
        }

        # Preserve natural inspector order
        for table_name in table_names:
            table_info = _introspect_table(inspector, table_name)
            schema_data["schema"][table_name] = table_info

        reports_dir = ensure_reports_dir()
        output_file = os.path.join(reports_dir, f"sok_introspect_{timestamp_str()}.json")
        write_json(output_file, schema_data)

        print(f"Schema introspection completed successfully.")
        print(f"Output written to: {output_file}")
        print(f"Processed {len(table_names)} tables.")
        return {
            "status": "success",
            "command": "introspect",
            "output_file": output_file,
            "tables_processed": len(table_names)
        }
    except Exception as e:
        return {"status": "error", "command": "introspect", "error": f"Error during schema introspection: {str(e)}"}