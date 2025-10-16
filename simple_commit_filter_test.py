#!/usr/bin/env python3

"""
Simple test for commit filtering functionality
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock streamlit
class MockSessionState:
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __contains__(self, key):
        return key in self.data
    
    def __delitem__(self, key):
        del self.data[key]

class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()
    
    def error(self, message):
        print(f"ERROR: {message}")
    
    def info(self, message):
        print(f"INFO: {message}")

# Install mock
sys.modules['streamlit'] = MockStreamlit()
st = sys.modules['streamlit']

def test_filtering():
    print("Testing commit filtering...")
    
    # Create test commits
    now = datetime.now()
    commits = [
        {'date': now - timedelta(days=30), 'message': '30 days ago'},
        {'date': now - timedelta(days=400), 'message': '400 days ago'},
        {'date': now - timedelta(days=800), 'message': '800 days ago'},
    ]
    
    # Create a simple filtering function based on our implementation
    def filter_commits_by_time_frame(commits):
        selected_time_frame = st.session_state.get('selected_time_frame', 'all')
        
        if selected_time_frame == 'all':
            return commits
        
        now = datetime.now()
        cutoff_date = None
        
        if selected_time_frame == '1_year':
            cutoff_date = now - timedelta(days=365)
        elif selected_time_frame == '2_years':
            cutoff_date = now - timedelta(days=2*365)
        elif selected_time_frame == '3_years':
            cutoff_date = now - timedelta(days=3*365)
        elif selected_time_frame == '5_years':
            cutoff_date = now - timedelta(days=5*365)
        else:
            return commits
        
        filtered_commits = []
        for commit in commits:
            commit_date = commit.get('date')
            if commit_date and commit_date >= cutoff_date:
                filtered_commits.append(commit)
        
        # Error handling
        if not filtered_commits and commits and selected_time_frame != 'all':
            time_frame_display = {
                '1_year': 'last 1 year',
                '2_years': 'last 2 years',
                '3_years': 'last 3 years',
                '5_years': 'last 5 years'
            }.get(selected_time_frame, selected_time_frame)
            
            st.session_state['commit_filter_error'] = {
                'message': f"No commits found for the {time_frame_display}",
                'total_commits': len(commits),
                'selected_period': time_frame_display
            }
        else:
            if 'commit_filter_error' in st.session_state:
                del st.session_state['commit_filter_error']
        
        return filtered_commits
    
    # Test different time frames
    test_cases = ['all', '1_year', '2_years', '3_years']
    
    for time_frame in test_cases:
        print(f"\nTesting time frame: {time_frame}")
        st.session_state['selected_time_frame'] = time_frame
        
        filtered = filter_commits_by_time_frame(commits)
        print(f"  Original: {len(commits)} commits")
        print(f"  Filtered: {len(filtered)} commits")
        
        for commit in filtered:
            print(f"    - {commit['message']}")
        
        # Check for errors
        error = st.session_state.get('commit_filter_error')
        if error:
            print(f"  Error: {error['message']}")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_filtering()
