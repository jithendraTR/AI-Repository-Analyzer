#!/usr/bin/env python3
"""
Find the exact duplicate st.set_page_config call mentioned in the error
"""

def find_duplicate_config():
    try:
        with open('repo_analyzer/main.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Total lines: {len(lines)}")
        print("\n=== All st.set_page_config occurrences ===")
        
        for i, line in enumerate(lines):
            if 'st.set_page_config' in line:
                line_num = i + 1
                print(f"Found at line {line_num}: {line.strip()}")
                
                # Show context around each occurrence
                start = max(0, i - 3)
                end = min(len(lines), i + 8)  # Show more context after
                print(f"\nContext around line {line_num}:")
                print("-" * 50)
                for j in range(start, end):
                    context_line_num = j + 1
                    prefix = " >>> " if context_line_num == line_num else "     "
                    print(f"{prefix}{context_line_num:3}: {lines[j].rstrip()}")
                print("-" * 50)
        
        # Also specifically check around line 372
        if len(lines) >= 372:
            print(f"\n=== Specific check around line 372 ===")
            start = max(0, 367)
            end = min(len(lines), 377)
            for i in range(start, end):
                line_num = i + 1
                prefix = " >>> " if line_num == 372 else "     "
                print(f"{prefix}{line_num:3}: {lines[i].rstrip()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_duplicate_config()
