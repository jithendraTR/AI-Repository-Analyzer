#!/usr/bin/env python3
"""
Test script to verify the performance improvements in Timeline Analysis
"""

import time
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path.cwd()))

from analyzers.timeline_analysis import TimelineAnalyzer

def test_timeline_analysis_performance():
    """Test the performance of the optimized Timeline Analysis analyzer"""
    print("🚀 Testing Optimized Timeline Analysis Performance")
    print("=" * 60)
    
    # Initialize the analyzer
    repo_path = Path.cwd()
    analyzer = TimelineAnalyzer(repo_path)
    
    if not analyzer.repo:
        print("❌ Error: Not a Git repository")
        return False
    
    print(f"📁 Repository: {repo_path}")
    print(f"🏷️  Repository has Git history: {analyzer.repo is not None}")
    
    # Start timing
    start_time = time.time()
    
    print("\n⏱️  Starting analysis...")
    print("This should complete in under 5 minutes with optimizations...")
    
    # Run the analysis
    try:
        result = analyzer.analyze()
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"⏱️  Time taken: {minutes}m {seconds}s")
        
        if elapsed_time < 300:  # 5 minutes = 300 seconds
            print("🎉 SUCCESS: Analysis completed in under 5 minutes!")
        else:
            print("⚠️  WARNING: Analysis took longer than 5 minutes")
        
        # Display results summary
        if "error" not in result:
            print("\n📊 Results Summary:")
            print(f"   • Total Commits Analyzed: {result.get('total_commits', 'N/A')}")
            
            # Project age
            age_data = result.get('project_age', {})
            if age_data:
                print(f"   • Project Age: {age_data.get('age_years', 0):.1f} years")
            
            # Timeline data
            timeline_data = result.get('timeline_data', {})
            if timeline_data:
                print(f"   • Monthly Commit Periods: {len(timeline_data.get('monthly_commits', {}))}")
                print(f"   • Daily Commit Records: {len(timeline_data.get('daily_commits', {}))}")
            
            # Recent changes
            recent_data = result.get('recent_changes', {})
            if recent_data:
                print(f"   • Recent Commits (30d): {recent_data.get('total_recent_commits', 0)}")
                print(f"   • Feature Commits: {len(recent_data.get('feature_commits', []))}")
                print(f"   • Bug Fixes: {len(recent_data.get('bug_fixes', []))}")
            
            # Development phases
            phases = result.get('development_phases', [])
            print(f"   • Development Phases Identified: {len(phases)}")
            
            # File evolution
            file_evolution = result.get('file_evolution', {})
            print(f"   • Files Analyzed for Evolution: {len(file_evolution)}")
            
            # Release patterns
            release_patterns = result.get('release_patterns', {})
            if release_patterns:
                print(f"   • Releases Found: {release_patterns.get('total_releases', 0)}")
            
            # Show development phases details if available
            if phases:
                print(f"\n🔄 Development Phases Overview:")
                for i, phase in enumerate(phases[:3]):  # Show first 3 phases
                    velocity = phase.get('velocity', 0)
                    activity = phase.get('dominant_activity', 'maintenance')
                    duration = phase.get('duration_days', 0)
                    commits = phase.get('commit_count', 0)
                    print(f"   Phase {i+1}: {activity} ({commits} commits, {duration} days, {velocity:.2f} commits/day)")
        else:
            print(f"❌ Error in analysis: {result['error']}")
            return False
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        print(f"\n❌ Analysis failed after {minutes}m {seconds}s")
        print(f"Error: {str(e)}")
        return False
    
    return elapsed_time < 300

if __name__ == "__main__":
    success = test_timeline_analysis_performance()
    sys.exit(0 if success else 1)
