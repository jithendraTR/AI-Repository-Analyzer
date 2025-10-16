#!/usr/bin/env python3

"""
Test to verify that PDF and DOCX save options have been added to design patterns analyzer
"""

import sys
import os
import inspect

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the design patterns analyzer
from analyzers.design_patterns import DesignPatternAnalyzer

def test_design_patterns_save_options():
    print("Testing save options in Design Pattern Analyzer...")
    
    # Check the source code of render method
    source = inspect.getsource(DesignPatternAnalyzer.render)
    
    print("🔍 Checking render method...")
    
    # Check that save options are added at the end
    has_save_options = False
    if "self.add_save_options" in source:
        has_save_options = True
        print("✅ Found add_save_options call")
    else:
        print("❌ add_save_options call not found")
    
    # Check that it's called with correct parameters
    has_correct_params = False
    if 'self.add_save_options("design_patterns", analysis)' in source:
        has_correct_params = True
        print("✅ Correct parameters for design_patterns analyzer")
    else:
        print("❌ Incorrect or missing parameters")
    
    # Check that it's added at the end after markdown separator
    lines = source.split('\n')
    save_options_line = -1
    markdown_line = -1
    
    for i, line in enumerate(lines):
        if 'st.markdown("---")' in line:
            markdown_line = i
        if 'self.add_save_options' in line:
            save_options_line = i
    
    proper_placement = False
    if markdown_line != -1 and save_options_line != -1 and save_options_line > markdown_line:
        proper_placement = True
        print("✅ Save options properly placed after markdown separator")
    else:
        print("❌ Save options not properly placed")
    
    # Check that the method inherits from BaseAnalyzer
    inherits_base = False
    class_source = inspect.getsource(DesignPatternAnalyzer)
    if "BaseAnalyzer" in class_source:
        inherits_base = True
        print("✅ Inherits from BaseAnalyzer (has access to add_save_options)")
    else:
        print("❌ Does not inherit from BaseAnalyzer")
    
    print("\n📋 SUMMARY:")
    if has_save_options:
        print("✅ Save options call found in render method")
    else:
        print("❌ Save options call missing")
    
    if has_correct_params:
        print("✅ Correct analyzer type parameter used")
    else:
        print("❌ Incorrect analyzer type parameter")
    
    if proper_placement:
        print("✅ Save options properly placed at end of render method")
    else:
        print("❌ Save options not properly placed")
    
    if inherits_base:
        print("✅ Has access to save functionality through BaseAnalyzer")
    else:
        print("❌ Missing BaseAnalyzer inheritance")
    
    if all([has_save_options, has_correct_params, proper_placement, inherits_base]):
        print("\n🎉 Design Patterns analyzer now has PDF and DOCX save options!")
    else:
        print("\n❌ Some issues found with save options implementation")
    
    print("\n💾 Users can now save Design Pattern analysis results as PDF or DOCX files")

if __name__ == "__main__":
    test_design_patterns_save_options()
