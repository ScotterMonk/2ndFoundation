#!/usr/bin/env python3
"""
Schema Inspector CLI Tool

Consolidated database schema analysis utility that provides multiple inspection
and comparison functions for the MediaShare application database.

This tool consolidates 8 legacy scripts into one canonical utility for:
- Database schema introspection
- Database vs ORM model comparison
- Model vs documentation comparison
- Documentation generation
- Summary reporting

Usage:
    python utils/schema_inspector.py <subcommand> [options]

Subcommands:
    introspect          Introspect PGDB schema
    compare-db-models  Compare PGDB vs ORM models
    compare-models-doc Compare ORM models vs schema doc
    generate-docs      Generate schema docs from PGDB
    report             Generate human-readable summary report
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from sqlalchemy import inspect as sqlalchemy_inspect

# Handle both direct execution and module imports
if __name__ == "__main__":
    # When run directly, add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import db
from utils.schema_commands import (
    run_compare_db_models,
    run_compare_models_doc,
    run_generate_docs,
    run_report,
)


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_3
def cmd_introspect(args):
    """Introspect PGDB schema and output structure information (delegates to utils.schema_commands)."""
    from utils.schema_commands import run_introspect
    return run_introspect(args)


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_3
# Note: detailed table introspection moved to utils/schema_commands._introspect_table to keep this file small.


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_2
def cmd_compare_db_models(args):
    """Compare PGDB schema vs ORM models and identify discrepancies."""
    return run_compare_db_models(args)


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_2
def cmd_compare_models_doc(args):
    """Compare ORM models vs schema documentation and identify inconsistencies."""
    return run_compare_models_doc(args)


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_2
def cmd_generate_docs(args):
    """Generate schema documentation from PGDB structure."""
    return run_generate_docs(args)


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_2
def cmd_report(args):
    """Generate human-readable summary report of schema analysis."""
    return run_report(args)


def create_parser():
    """Create and configure the argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="Schema Inspector CLI - Database schema analysis and documentation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s introspect --output schema.json
    %(prog)s compare-db-models --verbose --format json
    %(prog)s generate-docs --output docs/schema.md
    %(prog)s report --format table --output report.txt
        """
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available subcommands",
        metavar="COMMAND",
        required=True
    )
    
    # Introspect subcommand
    introspect_parser = subparsers.add_parser(
        "introspect",
        help="Introspect PGDB schema and extract structure information"
    )
    introspect_parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)",
        metavar="FILE"
    )
    introspect_parser.add_argument(
        "--format", "-f",
        choices=["json", "yaml", "table"],
        default="json",
        help="Output format (default: json)"
    )
    introspect_parser.add_argument(
        "--tables",
        nargs="*",
        help="Specific tables to introspect (default: all tables)"
    )
    introspect_parser.set_defaults(func=cmd_introspect)
    
    # Compare DB vs Models subcommand
    compare_db_parser = subparsers.add_parser(
        "compare-db-models",
        help="Compare PGDB schema vs ORM models"
    )
    compare_db_parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)",
        metavar="FILE"
    )
    compare_db_parser.add_argument(
        "--format", "-f",
        choices=["json", "yaml", "table", "summary"],
        default="json",
        help="Output format (default: json)"
    )
    compare_db_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed comparison results"
    )
    compare_db_parser.set_defaults(func=cmd_compare_db_models)
    
    # Compare Models vs Documentation subcommand
    compare_doc_parser = subparsers.add_parser(
        "compare-models-doc",
        help="Compare ORM models vs schema documentation"
    )
    compare_doc_parser.add_argument(
        "--doc-path", "-d",
        default=".roo/docs/database_schema.md",
        help="Path to schema documentation file (default: .roo/docs/database_schema.md)"
    )
    compare_doc_parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)",
        metavar="FILE"
    )
    compare_doc_parser.add_argument(
        "--format", "-f",
        choices=["json", "yaml", "table", "summary"],
        default="json",
        help="Output format (default: json)"
    )
    compare_doc_parser.set_defaults(func=cmd_compare_models_doc)
    
    # Generate Documentation subcommand
    generate_docs_parser = subparsers.add_parser(
        "generate-docs",
        help="Generate schema documentation from PGDB"
    )
    generate_docs_parser.add_argument(
        "--output", "-o",
        default=".roo/docs/database_schema.md",
        help="Output file path (default: .roo/docs/database_schema.md)"
    )
    generate_docs_parser.add_argument(
        "--format", "-f",
        choices=["markdown", "html", "json"],
        default="markdown",
        help="Documentation format (default: markdown)"
    )
    generate_docs_parser.add_argument(
        "--include-samples",
        action="store_true",
        help="Include sample data in documentation"
    )
    generate_docs_parser.set_defaults(func=cmd_generate_docs)
    
    # Report subcommand
    report_parser = subparsers.add_parser(
        "report",
        help="Generate human-readable summary report"
    )
    report_parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)",
        metavar="FILE"
    )
    report_parser.add_argument(
        "--format", "-f",
        choices=["table", "markdown", "html", "json"],
        default="table",
        help="Report format (default: table)"
    )
    report_parser.add_argument(
        "--sections",
        nargs="*",
        choices=["schema", "models", "discrepancies", "statistics"],
        help="Specific report sections to include (default: all)"
    )
    report_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Include detailed information in report"
    )
    report_parser.set_defaults(func=cmd_report)
    
    return parser


def main():
    """Main entry point for the schema inspector CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Import Flask and create a minimal app for database operations
    from flask import Flask
    from config import config_by_name
    
    # Create a fresh Flask app instance
    app = Flask(__name__)
    app.config.from_object(config_by_name['default'])
    
    # Initialize database with this app
    db.init_app(app)
    
    try:
        # Dispatch to the appropriate subcommand function within app context
        with app.app_context():
            result = args.func(args)
        
        # Handle output based on command result
        if result["status"] == "success":
            # For introspect command, output is already written to file
            if args.command == "introspect":
                if args.output and args.output != result["output_file"]:
                    # If custom output specified, copy the file
                    import shutil
                    shutil.copy2(result["output_file"], args.output)
                    print(f"Output also copied to: {args.output}")
                else:
                    print(f"Schema report available at: {result['output_file']}")
            else:
                # For other commands, handle output formatting
                if args.output:
                    print(f"Output would be written to: {args.output}")
                else:
                    print(json.dumps(result, indent=2))
        else:
            # Error occurred
            print(f"Command failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
            return 1
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())