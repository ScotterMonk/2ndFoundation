#!/usr/bin/env python3
"""
Simple test script to verify schema inspector implementation.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.schema_inspector import cmd_introspect
from utils.database import db
from datetime import datetime, timezone

# Create mock args for testing
class MockArgs:
    def __init__(self):
        self.command = "introspect"
        self.output = None
        self.format = "json"
        self.tables = None

# Test the implementation
try:
    # Initialize database connection
    with app.app.app_context():
        # Create mock arguments
        args = MockArgs()
        
        # Call the introspect function
        result = cmd_introspect(args)
        
        print(f"Test result: {result}")
        if result["status"] == "success":
            print(f"Output file: {result['output_file']}")
            
except Exception as e:
    print(f"Test failed with error: {e}")
    sys.exit(1)