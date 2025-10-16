#!/usr/bin/env python3
"""
Script to fix the syntax error in development_patterns.py
"""

def fix_syntax_error():
    """Remove the problematic </content> tag from the file"""
    
    # Read the file
    with open('analyzers/development_patterns.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the problematic tag
    content = content.replace('</content>', '')
    content = content.replace('<content>', '')
    
    # Remove any trailing whitespace and ensure proper ending
    content = content.rstrip()
    if not content.endswith('\n'):
        content += '\n'
    
    # Write back the fixed content
    with open('analyzers/development_patterns.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed syntax error in development_patterns.py")

if __name__ == "__main__":
    fix_syntax_error()
