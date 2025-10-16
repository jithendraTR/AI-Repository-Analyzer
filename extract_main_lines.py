#!/usr/bin/env python3
"""
Extract and display lines around 372 from main.py to find duplicate st.set_page_config
"""

def show_lines_around_372():
    try:
        with open('repo_analyzer/main.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Total lines: {len(lines)}")
        print("\nLines 365-380 (around line 372):")
        print("=" * 80)
        
        for i in range(364, min(381, len(lines))):
            line_num = i + 1
            line = lines[i].rstrip()
            marker = " >>> " if line_num == 372 else "     "
            print(f"{marker}{line_num:3}: {line}")
        
        print("=" * 80)
        
        # Also search for all st.set_page_config occurrences
        print("\nAll st.set_page_config occurrences:")
        for i, line in enumerate(lines):
            if 'st.set_page_config' in line:
                print(f"Line {i+1}: {line.strip()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_lines_around_372()
