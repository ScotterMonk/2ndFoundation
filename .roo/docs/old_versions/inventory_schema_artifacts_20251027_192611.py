# [Created-or-Modified] by glm-4.6 | 2025-10-26_1
"""
Inventory script for legacy schema artifacts.
This script identifies which legacy schema artifacts exist before archival.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def get_file_info(file_path):
    """Get file information including size and last modified timestamp"""
    try:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            return {
                'exists': True,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return {
                'exists': False,
                'size': 0,
                'modified': None
            }
    except Exception as e:
        return {
            'exists': False,
            'size': 0,
            'modified': None,
            'error': str(e)
        }

def main():
    # Define the legacy schema artifacts to check
    artifacts = [
        'database_schema_actual.md',
        'schema_discrepancies.json',
        'model_comparison_results.md',
        'model_discrepancies.md'
    ]
    
    # Get the repository root directory
    repo_root = Path(__file__).parent.parent
    print(f"Scanning for legacy schema artifacts in: {repo_root}")
    
    # Collect information about each artifact
    found_artifacts = []
    for artifact in artifacts:
        artifact_path = repo_root / artifact
        info = get_file_info(artifact_path)
        
        if info['exists']:
            found_artifacts.append({
                'filename': artifact,
                'path': str(artifact_path),
                'size': info['size'],
                'modified': info['modified']
            })
            print(f"Found: {artifact} ({info['size']} bytes, modified: {info['modified']})")
        else:
            print(f"Not found: {artifact}")
    
    # Generate timestamped report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    report_dir = repo_root / '.roo' / 'docs' / 'schema_reports'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f'inventory_{timestamp}.md'
    
    # Write report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Legacy Schema Artifacts Inventory\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"Total artifacts found: {len(found_artifacts)} of {len(artifacts)}\n\n")
        
        if found_artifacts:
            f.write("## Found Artifacts\n\n")
            for artifact in found_artifacts:
                f.write(f"### {artifact['filename']}\n\n")
                f.write(f"- **Path:** `{artifact['path']}`\n")
                f.write(f"- **Size:** {artifact['size']} bytes\n")
                f.write(f"- **Last Modified:** {artifact['modified']}\n\n")
        else:
            f.write("No legacy schema artifacts found.\n")
        
        f.write("## Checked Locations\n\n")
        for artifact in artifacts:
            artifact_path = repo_root / artifact
            f.write(f"- `{artifact_path}`\n")
    
    print(f"\nReport saved to: {report_path}")
    return report_path

if __name__ == "__main__":
    main()