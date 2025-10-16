#!/usr/bin/env python3
"""
Check specific lines around 372 in main.py
"""

def check_lines_around(file_path, target_line, context=5):
    """Check lines around a specific line number"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_line = max(0, target_line - context - 1)
        end_line = min(len(lines), target_line + context)
        
        print(f"Total lines in file: {len(lines)}")
        print(f"Checking lines {start_line + 1} to {end_line}:")
        print("-" * 50)
        
        for i in range(start_line, end_line):
            line_num = i + 1
            prefix = ">>> " if line_num == target_line else "    "
            print(f"{prefix}{line_num:3d}: {lines[i].rstrip()}")
            
        print("-" * 50)
        
        # Also search for any st.set_page_config in the entire file
        print("\nAll occurrences of 'st.set_page_config':")
        for i, line in enumerate(lines):
            if 'st.set_page_config' in line:
                print(f"Line {i + 1}: {line.strip()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_lines_around("repo_analyzer/main.py", 372, 10)
