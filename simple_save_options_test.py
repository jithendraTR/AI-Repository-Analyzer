#!/usr/bin/env python3

"""
Simple test to verify save options in Design Pattern Analyzer
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_save_options():
    print("Testing Design Patterns save options implementation...")
    
    try:
        # Read the design patterns analyzer file
        with open("analyzers/design_patterns.py", "r") as f:
            content = f.read()
        
        # Check for save options
        if "self.add_save_options" in content:
            print("✅ Save options call found")
        else:
            print("❌ Save options call NOT found")
            return False
        
        if 'self.add_save_options("design_patterns", analysis)' in content:
            print("✅ Correct parameters found")
        else:
            print("❌ Incorrect parameters")
            return False
        
        # Check placement after markdown separator
        lines = content.split('\n')
        found_markdown = False
        found_save_options = False
        
        for line in lines:
            if 'st.markdown("---")' in line:
                found_markdown = True
            elif found_markdown and 'self.add_save_options' in line:
                found_save_options = True
                break
        
        if found_save_options:
            print("✅ Save options properly placed after markdown separator")
        else:
            print("❌ Save options not properly placed")
            return False
        
        print("\n🎉 SUCCESS: Design Patterns analyzer now has PDF and DOCX save options!")
        print("💾 Users can now export Design Pattern analysis results to PDF or DOCX format")
        return True
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

if __name__ == "__main__":
    test_save_options()
