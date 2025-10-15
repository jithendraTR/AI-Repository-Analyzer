#!/usr/bin/env python3
"""
Test script to verify the performance improvements in Expertise Mapping
"""

import time
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path.cwd()))

from analyzers.expertise_mapping import ExpertiseMapper

def test_expertise_mapping_performance():
    """Test the performance of the optimized Expertise Mapping analyzer"""
    print("🚀 Testing Optimized Expertise Mapping Performance")
    print("=" * 60)
    
    # Initialize the analyzer
    repo_path = Path.cwd()
    mapper = ExpertiseMapper(repo_path)
    
    if not mapper.repo:
        print("❌ Error: Not a Git repository")
        return
    
    print(f"📁 Repository: {repo_path}")
    print(f"🏷️  Repository has Git history: {mapper.repo is not None}")
    
    # Start timing
    start_time = time.time()
    
    print("\n⏱️  Starting analysis...")
    print("This should complete in under 5 minutes with optimizations...")
    
    # Run the analysis
    try:
        result = mapper.analyze()
        
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
            print(f"   • Total Contributors: {result.get('total_contributors', 'N/A')}")
            print(f"   • Technologies Found: {len(result.get('tech_expertise', {}))}")
            print(f"   • Files Analyzed: {len(result.get('file_expertise', {}))}")
            print(f"   • Active Developers (30d): {result.get('recent_activity', {}).get('active_developers', 'N/A')}")
            
            # Show top technologies
            tech_expertise = result.get('tech_expertise', {})
            if tech_expertise:
                print(f"\n🔧 Top Technologies:")
                for i, (tech, developers) in enumerate(list(tech_expertise.items())[:5]):
                    total_commits = sum(developers.values())
                    print(f"   {i+1}. {tech}: {total_commits} commits by {len(developers)} developers")
        else:
            print(f"❌ Error in analysis: {result['error']}")
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        print(f"\n❌ Analysis failed after {minutes}m {seconds}s")
        print(f"Error: {str(e)}")
        return False
    
    return elapsed_time < 300

if __name__ == "__main__":
    success = test_expertise_mapping_performance()
    sys.exit(0 if success else 1)
