#!/usr/bin/env python3
"""
Debug script to find all st.set_page_config calls in the main.py file
"""

import re
import os

def find_streamlit_config_calls(file_path):
    """Find all st.set_page_config calls with line numbers"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Analyzing file: {file_path}")
    print(f"Total lines: {len(lines)}")
    print("\nSearching for st.set_page_config calls:")
    
    config_calls = []
    for i, line in enumerate(lines):
        line_num = i + 1
        if 'st.set_page_config' in line:
            config_calls.append((line_num, line.strip()))
            print(f"Line {line_num}: {line.strip()}")
    
    if not config_calls:
        print("No st.set_page_config calls found!")
    else:
        print(f"\nFound {len(config_calls)} st.set_page_config call(s)")
    
    # Also search for any other streamlit calls in the first 50 lines
    print("\nSearching for any 'st.' calls in first 50 lines:")
    for i, line in enumerate(lines[:50]):
        line_num = i + 1
        if re.search(r'\bst\.', line) and 'import' not in line:
            print(f"Line {line_num}: {line.strip()}")

if __name__ == "__main__":
    find_streamlit_config_calls("repo_analyzer/main.py")
