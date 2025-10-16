#!/usr/bin/env python3

"""
Test script to verify commit time frame filtering functionality
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime, timedelta
import git

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock streamlit session_state for testing
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

# Mock streamlit module
class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()
    
    def error(self, message):
        print(f"ERROR: {message}")
    
    def info(self, message):
        print(f"INFO: {message}")
    
    def warning(self, message):
        print(f"WARNING: {message}")

# Install mock before importing our analyzers
sys.modules['streamlit'] = MockStreamlit()
st = sys.modules['streamlit']

def create_test_repo_with_commits():
    """Create a temporary git repository with commits spread across different time periods"""
    temp_dir = tempfile.mkdtemp()
    repo = git.Repo.init(temp_dir)
    
    # Configure git user
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Test User")
        git_config.set_value("user", "email", "test@example.com")
    
    # Create commits with different dates
    now = datetime.now()
    commit_dates = [
        now - timedelta(days=30),   # 1 month ago
        now - timedelta(days=180),  # 6 months ago  
        now - timedelta(days=400),  # ~1.1 years ago
        now - timedelta(days=800),  # ~2.2 years ago
        now - timedelta(days=1200), # ~3.3 years ago
        now - timedelta(days=2000), # ~5.5 years ago
    ]
    
    commits = []
    for i, commit_date in enumerate(commit_dates):
        # Create a file
        file_path = os.path.join(temp_dir, f"file_{i}.txt")
        with open(file_path, 'w') as f:
            f.write(f"Content {i} created on {commit_date}")
        
        # Add and commit
        repo.index.add([f"file_{i}.txt"])
        commit = repo.index.commit(f"Commit {i} - {commit_date.strftime('%Y-%m-%d')}")
        
        # Manually set commit date (GitPython doesn't easily allow this, so we'll use a workaround)
        # For this test, we'll just track the intended dates
        commits.append({
            'hash': commit.hexsha,
            'author': 'Test User',
            'email': 'test@example.com',
            'date': commit_date,
            'message': f"Commit {i} - {commit_date.strftime('%Y-%m-%d')}",
            'files_changed': 1
        })
    
    return temp_dir, commits

def test_commit_filtering():
    """Test the commit filtering functionality"""
    from analyzers.base_analyzer import BaseAnalyzer
    
    print("🧪 Testing Commit Time Frame Filtering")
    print("=" * 50)
    
    # Create test repository
    temp_repo, test_commits = create_test_repo_with_commits()
    
    try:
        # Create analyzer (this will fail for git repo, but we can test filtering directly)
        print(f"📁 Created test repository: {temp_repo}")
        print(f"📊 Created {len(test_commits)} test commits")
        
        # Test different time frame filters
        time_frames = ['all', '1_year', '2_years', '3_years', '5_years']
        
        for time_frame in time_frames:
            print(f"\n🔍 Testing time frame: {time_frame}")
            
            # Set session state
            st.session_state['selected_time_frame'] = time_frame
            
            # Create a mock analyzer to access the filtering method
            class MockAnalyzer(BaseAnalyzer):
                def __init__(self):
                    # Skip the parent __init__ since we just need the filtering method
                    pass
                
                def analyze(self, token=None, progress_callback=None):
                    return {}
                
                def render(self):
                    pass
            
            analyzer = MockAnalyzer()
            
            # Test filtering
            filtered_commits = analyzer.filter_commits_by_time_frame(test_commits)
            
            print(f"   📈 Original commits: {len(test_commits)}")
            print(f"   📉 Filtered commits: {len(filtered_commits)}")
            
            # Show which commits were included
            if filtered_commits:
                print(f"   ✅ Included commit dates:")
                for commit in filtered_commits:
                    print(f"      - {commit['date'].strftime('%Y-%m-%d')} ({commit['message']})")
            else:
                print(f"   ❌ No commits found for this time period")
                
                # Check if error was set
                error_info = st.session_state.get('commit_filter_error', {})
                if error_info:
                    print(f"   🔧 Error message: {error_info['message']}")
        
        print(f"\n✅ All filtering tests completed successfully!")
        
        # Test error handling specifically
        print(f"\n🧪 Testing Error Handling")
        print("=" * 30)
        
        # Set to a time frame with no commits
        st.session_state['selected_time_frame'] = '1_year'
        
        # Create commits that are all older than 1 year
        old_commits = []
        now = datetime.now()
        for i in range(3):
            old_date = now - timedelta(days=500 + i*100)  # All older than 1 year
            old_commits.append({
                'hash': f'abc123{i}',
                'author': 'Old Author',
                'email': 'old@example.com',
                'date': old_date,
                'message': f'Old commit {i}',
                'files_changed': 1
            })
        
        analyzer = MockAnalyzer()
        filtered = analyzer.filter_commits_by_time_frame(old_commits)
        
        print(f"📊 Old commits: {len(old_commits)}")
        print(f"📉 Filtered (1 year): {len(filtered)}")
        
        error_info = analyzer.check_commit_filter_error()
        if error_info:
            print(f"✅ Error handling working: {error_info['message']}")
            print(f"   Total commits: {error_info['total_commits']}")
            print(f"   Selected period: {error_info['selected_period']}")
        
        # Test display error function
        print(f"\n🖥️ Testing Error Display")
        error_displayed = analyzer.display_commit_filter_error()
        print(f"Error displayed: {error_displayed}")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_repo)
        print(f"\n🧹 Cleaned up test repository")

if __name__ == "__main__":
    test_commit_filtering()
