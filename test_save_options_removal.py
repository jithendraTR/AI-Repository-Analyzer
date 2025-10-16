#!/usr/bin/env python3

"""
Test to verify that JSON, CSV, and full report save options have been removed
"""

import sys
import os
import inspect

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the base analyzer
from analyzers.base_analyzer import BaseAnalyzer

def test_save_options_removal():
    print("Testing save options removal from BaseAnalyzer...")
    
    # Check the source code of add_save_options method
    source = inspect.getsource(BaseAnalyzer.add_save_options)
    
    print("🔍 Checking add_save_options method...")
    
    # Check that JSON, CSV, and full report references are removed
    removed_items = []
    if "Save as JSON" not in source:
        removed_items.append("JSON save option")
    if "Save as CSV" not in source:
        removed_items.append("CSV save option")
    if "Save Full Report" not in source:
        removed_items.append("Full report save option")
    
    # Check that PDF and DOCX options are still present
    present_items = []
    if "Save as PDF" in source:
        present_items.append("PDF save option")
    if "Save as DOCX" in source:
        present_items.append("DOCX save option")
    
    print(f"✅ Removed items: {removed_items}")
    print(f"✅ Present items: {present_items}")
    
    # Check column layout has been updated
    if "col1, col2 = st.columns(2)" in source:
        print("✅ Column layout updated to 2 columns")
    else:
        print("❌ Column layout not updated")
    
    # Check that removed helper methods are no longer present
    methods = [method for method in dir(BaseAnalyzer) if not method.startswith('_')]
    removed_methods = []
    
    if '_prepare_json_export' not in methods:
        removed_methods.append("_prepare_json_export")
    if '_prepare_csv_export' not in methods:
        removed_methods.append("_prepare_csv_export")
    if '_prepare_full_report' not in methods:
        removed_methods.append("_prepare_full_report")
    if '_add_analysis_to_markdown' not in methods:
        removed_methods.append("_add_analysis_to_markdown")
    
    print(f"✅ Removed helper methods: {removed_methods}")
    
    # Check that required methods are still present
    present_methods = []
    if '_generate_single_analyzer_pdf' in dir(BaseAnalyzer):
        present_methods.append("_generate_single_analyzer_pdf")
    if '_generate_single_analyzer_docx' in dir(BaseAnalyzer):
        present_methods.append("_generate_single_analyzer_docx")
    if '_add_data_to_docx' in dir(BaseAnalyzer):
        present_methods.append("_add_data_to_docx")
    
    print(f"✅ Present methods: {present_methods}")
    
    # Summary
    print("\n📋 SUMMARY:")
    if len(removed_items) == 3:
        print("✅ All save options (JSON, CSV, Full Report) successfully removed")
    else:
        print("❌ Some save options may not have been removed")
    
    if len(present_items) == 2:
        print("✅ PDF and DOCX save options preserved")
    else:
        print("❌ PDF or DOCX save options may be missing")
    
    if len(removed_methods) >= 3:
        print("✅ Unused helper methods successfully removed")
    else:
        print("❌ Some helper methods may not have been removed")
    
    if len(present_methods) == 3:
        print("✅ Required PDF/DOCX methods preserved")
    else:
        print("❌ Some required methods may be missing")
    
    print("\n🎉 Save options removal test completed!")

if __name__ == "__main__":
    test_save_options_removal()
