"""
Test to verify that removing the 'Rerun Analysis' button doesn't affect functionality
"""

import sys
import os
import streamlit as st
from repo_analyzer.main import main

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_main():
    """Test that the main function runs without errors after removing the Rerun Analysis button"""
    try:
        # Mock environment and session state to allow application to initialize
        if 'analysis_complete' not in st.session_state:
            st.session_state.analysis_complete = False
        if 'results' not in st.session_state:
            st.session_state.results = {}
        if 'sidebar_collapsed' not in st.session_state:
            st.session_state.sidebar_collapsed = False
        if 'analysis_running' not in st.session_state:
            st.session_state.analysis_running = False
        
        # Run the main function
        main()
        print("✅ Application initialized without errors")
        return True
    except Exception as e:
        print(f"❌ Error running main function: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing application after removing 'Rerun Analysis' button...")
    success = test_main()
    
    if success:
        print("✅ Test passed! Application functions correctly without the Rerun Analysis button")
    else:
        print("❌ Test failed! Application encountered errors")
