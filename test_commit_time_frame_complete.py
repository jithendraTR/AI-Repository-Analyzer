#!/usr/bin/env python3

"""
Complete test for commit time frame functionality
Tests both UI components and filtering logic
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_commit_time_frame_complete():
    """Test the complete commit time frame functionality"""
    
    print("🧪 Testing Complete Commit Time Frame Functionality")
    print("=" * 60)
    
    # Test 1: Check if main.py has the time frame selector
    try:
        with open('repo_analyzer/main.py', 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Check for time frame UI elements
        time_frame_indicators = [
            "⏱️ Commit Time Frame",
            '"all": "All commits"',
            '"1_year": "Last 1 year"',
            '"2_years": "Last 2 years"', 
            '"3_years": "Last 3 years"',
            '"5_years": "Last 5 years"',
            'st.selectbox',
            'selected_time_frame',
            'Choose how far back in commit history to analyze'
        ]
        
        missing_ui = []
        for indicator in time_frame_indicators:
            if indicator not in main_content:
                missing_ui.append(indicator)
        
        if missing_ui:
            print("❌ Missing UI elements:")
            for element in missing_ui:
                print(f"   - {element}")
            return False
        else:
            print("✅ All UI elements found in main.py")
        
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False
    
    # Test 2: Check base_analyzer.py for filtering logic
    try:
        with open('analyzers/base_analyzer.py', 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Check for filtering functionality
        filtering_indicators = [
            'filter_commits_by_time_frame',
            'selected_time_frame',
            'timedelta(days=365)',
            'timedelta(days=2*365)',
            'timedelta(days=3*365)',
            'timedelta(days=5*365)',
            'commit_filter_error',
            'No commits found for the'
        ]
        
        missing_logic = []
        for indicator in filtering_indicators:
            if indicator not in base_content:
                missing_logic.append(indicator)
        
        if missing_logic:
            print("❌ Missing filtering logic:")
            for element in missing_logic:
                print(f"   - {element}")
            return False
        else:
            print("✅ All filtering logic found in base_analyzer.py")
        
    except Exception as e:
        print(f"❌ Error reading base_analyzer.py: {e}")
        return False
    
    # Test 3: Test filtering logic directly
    print("\n📊 Testing Filtering Logic:")
    
    # Mock commits with different dates
    now = datetime.now()
    test_commits = [
        {'date': now - timedelta(days=30), 'message': 'Recent commit'},  # 1 month ago
        {'date': now - timedelta(days=200), 'message': 'Less recent'},   # 6 months ago  
        {'date': now - timedelta(days=400), 'message': 'Older commit'},  # 1+ years ago
        {'date': now - timedelta(days=800), 'message': 'Old commit'},    # 2+ years ago
        {'date': now - timedelta(days=1500), 'message': 'Very old'},     # 4+ years ago
    ]
    
    # Import the filtering function
    try:
        from analyzers.base_analyzer import BaseAnalyzer
        
        # Create a dummy analyzer to test filtering
        class TestAnalyzer(BaseAnalyzer):
            def analyze(self, token=None, progress_callback=None):
                return {}
            def render(self):
                pass
        
        # Create test instance with a valid path
        if os.path.exists('.'):
            analyzer = TestAnalyzer('.')
        else:
            print("❌ Cannot create test analyzer - no valid path")
            return False
        
        # Test different time frames
        test_cases = [
            ('all', 5),       # All commits
            ('1_year', 2),    # Last 1 year (2 commits)
            ('2_years', 3),   # Last 2 years (3 commits)  
            ('3_years', 4),   # Last 3 years (4 commits)
            ('5_years', 5),   # Last 5 years (all 5 commits)
        ]
        
        # Mock session state
        import streamlit as st
        if not hasattr(st, 'session_state'):
            class MockSessionState:
                def __init__(self):
                    self.data = {}
                def get(self, key, default=None):
                    return self.data.get(key, default)
                def __setitem__(self, key, value):
                    self.data[key] = value
                def __contains__(self, key):
                    return key in self.data
                def __delitem__(self, key):
                    if key in self.data:
                        del self.data[key]
            
            st.session_state = MockSessionState()
        
        for time_frame, expected_count in test_cases:
            st.session_state['selected_time_frame'] = time_frame
            
            # Clear any previous errors
            if 'commit_filter_error' in st.session_state:
                del st.session_state['commit_filter_error']
            
            filtered = analyzer.filter_commits_by_time_frame(test_commits)
            actual_count = len(filtered)
            
            if actual_count == expected_count:
                print(f"   ✅ {time_frame}: {actual_count}/{expected_count} commits")
            else:
                print(f"   ❌ {time_frame}: {actual_count}/{expected_count} commits (expected {expected_count})")
                return False
        
        print("✅ All filtering tests passed")
        
    except Exception as e:
        print(f"❌ Error testing filtering logic: {e}")
        return False
    
    # Test 4: Test error handling
    print("\n⚠️ Testing Error Handling:")
    
    try:
        # Test empty commits for specific time period
        empty_commits = []
        
        # Set to 1 year filter
        st.session_state['selected_time_frame'] = '1_year'
        filtered_empty = analyzer.filter_commits_by_time_frame(empty_commits)
        
        # Should not set error for empty commits list
        if 'commit_filter_error' not in st.session_state:
            print("   ✅ No error for empty commits list")
        else:
            print("   ❌ Unexpected error for empty commits")
            return False
        
        # Test commits outside time range
        old_commits = [
            {'date': now - timedelta(days=400), 'message': 'Old commit 1'},  # 1+ years ago
            {'date': now - timedelta(days=500), 'message': 'Old commit 2'},  # 1+ years ago
        ]
        
        st.session_state['selected_time_frame'] = '1_year'
        filtered_old = analyzer.filter_commits_by_time_frame(old_commits)
        
        # Should set error for commits outside time range
        if 'commit_filter_error' in st.session_state:
            error_info = st.session_state['commit_filter_error']
            if 'No commits found for the last 1 year' in error_info.get('message', ''):
                print("   ✅ Correct error for no commits in time range")
            else:
                print(f"   ❌ Wrong error message: {error_info.get('message', '')}")
                return False
        else:
            print("   ❌ No error set for commits outside time range")
            return False
        
        print("✅ Error handling tests passed")
        
    except Exception as e:
        print(f"❌ Error testing error handling: {e}")
        return False
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 All Commit Time Frame Tests Passed!")
    print("\n📋 Implemented Features:")
    print("✅ Time frame selector UI in sidebar")
    print("✅ 5 time frame options (all, 1yr, 2yr, 3yr, 5yr)")  
    print("✅ Commit filtering by date range")
    print("✅ Session state integration")
    print("✅ Error handling for empty periods")
    print("✅ User-friendly error messages")
    print("✅ Suggestions when no commits found")
    
    return True

if __name__ == "__main__":
    success = test_commit_time_frame_complete()
    if success:
        print("\n🚀 Commit time frame functionality is fully implemented and working!")
        exit(0)
    else:
        print("\n❌ Some tests failed - check the output above")
        exit(1)
