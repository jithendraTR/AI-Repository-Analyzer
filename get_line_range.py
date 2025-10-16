#!/usr/bin/env python3
"""
Extract specific line range from main.py
"""

def extract_lines(file_path, start_line, end_line):
    """Extract lines from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Total lines in file: {len(lines)}")
        print(f"Extracting lines {start_line} to {end_line}:")
        print("=" * 60)
        
        for i in range(start_line - 1, min(end_line, len(lines))):
            line_num = i + 1
            line_content = lines[i].rstrip()
            print(f"{line_num:4d}: {line_content}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Extract lines around 372
    extract_lines("repo_analyzer/main.py", 365, 380)
