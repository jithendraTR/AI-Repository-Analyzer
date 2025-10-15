#!/usr/bin/env python3
"""
Quick test to verify the current state of the development_patterns.py file
"""

def check_file_content():
    """Check the exact content around line 1160"""
    
    with open('analyzers/development_patterns.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("Checking lines around 1155-1165 in development_patterns.py:")
    print("=" * 60)
    
    start_line = max(0, 1155 - 1)  # Convert to 0-based indexing
    end_line = min(len(lines), 1165)
    
    for i in range(start_line, end_line):
        line_num = i + 1
        line_content = lines[i].rstrip()
        marker = ">>> " if line_num == 1160 else "    "
        print(f"{marker}{line_num:4d}: {line_content}")
    
    print("=" * 60)
    
    # Check for problematic patterns
    file_content = ''.join(lines)
    
    if 'config_patterns["environment_patterns"]' in file_content:
        print("❌ Found direct dictionary access pattern!")
        print("Searching for all instances:")
        
        for i, line in enumerate(lines, 1):
            if 'config_patterns["environment_patterns"]' in line:
                print(f"  Line {i}: {line.strip()}")
    else:
        print("✅ No direct dictionary access patterns found")
    
    # Check for safe .get() patterns
    if 'config_patterns.get("environment_patterns"' in file_content:
        print("✅ Found safe .get() access patterns")
    else:
        print("❌ No safe .get() access patterns found")

if __name__ == "__main__":
    check_file_content()
