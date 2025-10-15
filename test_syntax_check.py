#!/usr/bin/env python3

import ast
import sys

def check_syntax(filename):
    """Check if a Python file has valid syntax"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Try to parse the source code
        ast.parse(source)
        print(f"✅ {filename} - Syntax is valid!")
        return True
        
    except SyntaxError as e:
        print(f"❌ {filename} - Syntax Error:")
        print(f"  Line {e.lineno}: {e.text}")
        print(f"  Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filename} - Error: {e}")
        return False

if __name__ == "__main__":
    check_syntax("analyzers/development_patterns.py")
