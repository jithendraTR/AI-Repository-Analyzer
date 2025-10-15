#!/usr/bin/env python3
"""
Performance Timing Test for AI Repository Analyzer
Measures actual execution times for all optimized analyzers
"""

import time
import sys
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Import all analyzers
from analyzers.expertise_mapping import ExpertiseMappingAnalyzer
from analyzers.tech_debt_detection import TechnicalDebtAnalyzer
from analyzers.risk_analysis import RiskAnalysisAnalyzer
from analyzers.timeline_analysis import TimelineAnalyzer
from analyzers.version_governance import VersionGovernanceAnalyzer
from analyzers.design_patterns import DesignPatternsAnalyzer
from analyzers.development_patterns import DevelopmentPatternsAnalyzer
from analyzers.api_contracts import APIContractAnalyzer
from analyzers.ai_context import AIContextAnalyzer
from analyzers.singular_product_vision import SingularProductVisionAnalyzer

class MockToken:
    """Mock cancellation token for testing"""
    def check_cancellation(self):
        pass

def progress_callback(current, total, status):
    """Progress callback for timing tests"""
    print(f"  Progress: {current}/{total} - {status}")

def measure_analyzer_time(analyzer_class, repo_path, name):
    """Measure the execution time of a single analyzer"""
    print(f"\n🔍 Testing {name}...")
    
    start_time = time.time()
    
    try:
        # Initialize analyzer
        analyzer = analyzer_class(repo_path)
        
        # Run analysis with token and progress callback
        token = MockToken()
        result = analyzer.analyze(token=token, progress_callback=progress_callback)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Check if analysis was successful
        if "error" in result:
            print(f"  ❌ FAILED: {result['error']}")
            return None, False
        else:
            print(f"  ✅ SUCCESS: {execution_time:.2f} seconds")
            return execution_time, True
            
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"  ❌ ERROR: {str(e)} (after {execution_time:.2f}s)")
        return execution_time, False

def main():
    """Run comprehensive timing test for all analyzers"""
    print("🚀 AI Repository Analyzer - Performance Timing Test")
    print("=" * 60)
    
    # Get repository path (current directory)
    repo_path = Path.cwd()
    print(f"Repository: {repo_path}")
    
    # Define all analyzers to test
    analyzers_to_test = [
        (ExpertiseMappingAnalyzer, "Expertise Mapping"),
        (TechnicalDebtAnalyzer, "Technical Debt Detection"), 
        (RiskAnalysisAnalyzer, "Risk Analysis"),
        (TimelineAnalyzer, "Timeline Analysis"),
        (VersionGovernanceAnalyzer, "Version Governance"),
        (DesignPatternsAnalyzer, "Design Patterns"),
        (DevelopmentPatternsAnalyzer, "Development Patterns"),
        (APIContractAnalyzer, "API Contracts"),
        (AIContextAnalyzer, "AI Context"),
        (SingularProductVisionAnalyzer, "Singular Product Vision")
    ]
    
    print(f"\nTesting {len(analyzers_to_test)} optimized analyzers...")
    
    # Track results
    results = []
    total_start_time = time.time()
    successful_count = 0
    failed_count = 0
    
    # Test each analyzer individually
    for analyzer_class, name in analyzers_to_test:
        execution_time, success = measure_analyzer_time(analyzer_class, repo_path, name)
        
        results.append({
            'name': name,
            'time': execution_time,
            'success': success
        })
        
        if success:
            successful_count += 1
        else:
            failed_count += 1
    
    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    
    # Display results summary
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal Execution Time: {total_execution_time:.2f} seconds ({total_execution_time/60:.2f} minutes)")
    print(f"Target: < 300 seconds (5 minutes)")
    
    if total_execution_time <= 300:
        print("🎉 SUCCESS: All analyzers completed within 5-minute target!")
    else:
        print("⚠️  WARNING: Total time exceeded 5-minute target")
    
    print(f"\nAnalyzers Successful: {successful_count}/{len(analyzers_to_test)}")
    print(f"Analyzers Failed: {failed_count}/{len(analyzers_to_test)}")
    
    # Individual analyzer results
    print("\n📋 Individual Analyzer Performance:")
    print("-" * 50)
    
    for result in results:
        if result['success']:
            status_icon = "✅"
            time_str = f"{result['time']:.2f}s"
        else:
            status_icon = "❌"
            time_str = f"{result['time']:.2f}s (FAILED)" if result['time'] else "FAILED"
        
        print(f"{status_icon} {result['name']:<25} {time_str:>12}")
    
    # Performance analysis
    if successful_count > 0:
        successful_times = [r['time'] for r in results if r['success'] and r['time']]
        if successful_times:
            avg_time = sum(successful_times) / len(successful_times)
            max_time = max(successful_times)
            min_time = min(successful_times)
            
            print(f"\n📈 Performance Statistics (Successful Analyzers):")
            print(f"   Average Time: {avg_time:.2f} seconds")
            print(f"   Fastest Time: {min_time:.2f} seconds") 
            print(f"   Slowest Time: {max_time:.2f} seconds")
    
    # Final verdict
    print("\n" + "=" * 60)
    if total_execution_time <= 300 and failed_count == 0:
        print("🏆 OPTIMIZATION SUCCESS: All analyzers working under 5-minute target!")
    elif total_execution_time <= 300 and failed_count > 0:
        print("⚠️  PARTIAL SUCCESS: Time target met but some analyzers failed")
    else:
        print("❌ OPTIMIZATION INCOMPLETE: Performance target not met")
    print("=" * 60)
    
    return total_execution_time <= 300 and failed_count == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
