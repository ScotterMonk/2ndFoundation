#!/usr/bin/env python3
"""
Schema documentation parsing and formatting utilities.

Parses database_schema.md into a structured schema, converts to comparison-friendly
format, and renders markdown from introspection data.
"""

import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def parse_markdown_schema(doc_path: str) -> Dict[str, Any]:
    """
    Parse .roo/docs/database_schema.md into an 'introspect-like' structure:
    {
      "metadata": {...},
      "schema": {
        "table_name": {
          "columns": [{"name","type","nullable","default","autoincrement"}],
          "primary_keys": [..],
          "foreign_keys": [{"name","constrained_columns","referred_table","referred_columns"}],
          "indexes": [],
          "unique_constraints": []
        },
        ...
      },
      "views": {
        "view_name": {
          "columns": [{"name","type","nullable"}]
        }
      }
    }
    """
    # [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    schema: Dict[str, Any] = {}
    views: Dict[str, Any] = {}

    # Split into sections beginning with ### ...
    # Capture heading "view: name" or "table_name"
    sections = re.findall(r"^###[ ]+([^\n]+)\n(.*?)(?=^###[ ]+|\Z)", content, flags=re.DOTALL | re.MULTILINE)

    for heading, body in sections:
        heading = heading.strip()
        is_view = False
        name = heading
        if heading.lower().startswith("view:"):
            is_view = True
            name = heading.split(":", 1)[1].strip()

        # Primary Key
        pk: List[str] = []
        m = re.search(r"\*\*Primary Key:\*\*[ ]+([^\n]+)", body)
        if m:
            pk = [x.strip() for x in m.group(1).split(",") if x.strip()]

        # Columns: lines like - `col`: type NULL/NOT NULL
        columns: List[Dict[str, Any]] = []
        for col_name, col_type, null_flag in re.findall(r"-[ ]+`([^`]+)`: ([^`\n]+) (NULL|NOT NULL)", body):
            columns.append({
                "name": col_name,
                "type": col_type.strip(),
                "nullable": (null_flag == "NULL"),
                "default": None,
                "autoincrement": False
            })

        if is_view:
            # Views: keep simpler structure
            vcols = [{"name": c["name"], "type": c["type"], "nullable": c["nullable"]} for c in columns]
            views[name] = {"columns": vcols}
            continue

        # Foreign Keys: - `col` -> `table.column`
        fks: List[Dict[str, Any]] = []
        for col, ref_table, ref_col in re.findall(r"-[ ]+`([^`]+)`[ ]+->[ ]+`([^`]+)\.([^`]+)`", body):
            fks.append({
                "name": f"fk_{name}_{col}",
                "constrained_columns": [col],
                "referred_table": ref_table,
                "referred_columns": [ref_col]
            })

        schema[name] = {
            "columns": columns,
            "primary_keys": pk,
            "foreign_keys": fks,
            "indexes": [],
            "unique_constraints": []
        }

    return {
        "metadata": {
            "source": "markdown",
            "path": doc_path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        "schema": schema,
        "views": views
    }


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def to_compare_format(introspect_like: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert 'introspect-like' structure to the comparison shape expected by
    compare_models.compare_schema_with_models():
    {
      "table": {
        "columns": { "col": {"type": "...","nullable": bool, "length": optional} },
        "primary_key": [..],
        "foreign_keys": [{"column": "col", "references": {"table": "...","column":"..."}}]
      }
    }
    Views are ignored for comparison.
    """
    out: Dict[str, Any] = {}
    schema = introspect_like.get("schema", {})
    for table, info in schema.items():
        cols_map: Dict[str, Any] = {}
        for c in info.get("columns", []):
            typ = (c.get("type") or "").strip()
            # Extract optional (precision, scale) or (len)
            length = None
            m = re.search(r"\(([^)]+)\)", typ)
            if m:
                length = m.group(1).strip()
                typ = typ[:typ.index("(")].strip()
            cols_map[c["name"]] = {"type": typ, "length": length, "nullable": bool(c.get("nullable", True))}
        fk_list = []
        for fk in info.get("foreign_keys", []):
            col = fk.get("constrained_columns", [None])[0]
            rt = fk.get("referred_table")
            rc = fk.get("referred_columns", [None])[0]
            if col and rt and rc:
                fk_list.append({"column": col, "references": {"table": rt, "column": rc}})
        out[table] = {
            "columns": cols_map,
            "primary_key": list(info.get("primary_keys", [])),
            "foreign_keys": fk_list
        }
    return out


# [Created-or-Modified] by openai/gpt-5 | 2025-10-26_1
def markdown_from_introspect(introspect_like: Dict[str, Any]) -> str:
    """
    Render markdown documentation from 'introspect-like' structure.
    Includes optional views if present.
    """
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = []
    # Standardized header with generator notice
    lines.append("# Database Schema Overview")
    lines.append("")
    lines.append(f"*Last updated (UTC): {ts}*")
    lines.append("")
    lines.append("> Generated by unified Schema Inspector. Source of Truth (SoT): Live PGDB.")
    lines.append("> Regenerate with: python utils/schema_inspector.py generate-docs")
    lines.append("")
    lines.append("## Tables")
    lines.append("")

    views = introspect_like.get("views") or {}
    if views:
        # Keep views at top similar to existing doc
        for vname, vinfo in views.items():
            lines.append(f"### view: {vname}")
            lines.append("")
            lines.append("**Columns:**")
            for c in vinfo.get("columns", []):
                nulltxt = "NULL" if c.get("nullable", True) else "NOT NULL"
                lines.append(f"- `{c.get('name')}`: {c.get('type','unknown')} {nulltxt}")
            lines.append("")

    schema = introspect_like.get("schema", {})
    # Preserve natural-ish order; do not sort, but if dict, sort by name for determinism
    for tname in sorted(schema.keys()):
        tinfo = schema[tname]
        lines.append(f"### {tname}")
        lines.append("")
        if tinfo.get("primary_keys"):
            lines.append(f"**Primary Key:** {', '.join(tinfo['primary_keys'])}")
            lines.append("")
        lines.append("**Columns:**")
        for c in tinfo.get("columns", []):
            nulltxt = "NULL" if c.get("nullable", True) else "NOT NULL"
            lines.append(f"- `{c.get('name')}`: {c.get('type','unknown')} {nulltxt}")
        if tinfo.get("foreign_keys"):
            lines.append("")
            lines.append("**Foreign Keys:**")
            for fk in tinfo["foreign_keys"]:
                col = (fk.get("constrained_columns") or [None])[0]
                rt = fk.get("referred_table")
                rc = (fk.get("referred_columns") or [None])[0]
                if col and rt and rc:
                    lines.append(f"- `{col}` -> `{rt}.{rc}`")
        lines.append("")

    return "\n".join(lines)