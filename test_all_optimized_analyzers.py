#!/usr/bin/env python3
"""
Comprehensive test for all optimized analyzers
Verifies sub-5-minute performance for all analyzers
"""

import time
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from analyzers.expertise_mapping import ExpertiseMappingAnalyzer
from analyzers.tech_debt_detection import TechDebtAnalyzer
from analyzers.risk_analysis import RiskAnalyzer
from analyzers.timeline_analysis import TimelineAnalyzer
from analyzers.version_governance import VersionGovernanceAnalyzer
from analyzers.design_patterns import DesignPatternsAnalyzer
from analyzers.development_patterns import DevelopmentPatternsAnalyzer
from analyzers.api_contracts import APIContractAnalyzer
from analyzers.ai_context import AIContextAnalyzer
from analyzers.singular_product_vision import SingularProductVisionAnalyzer

class MockProgressCallback:
    def __init__(self, analyzer_name):
        self.analyzer_name = analyzer_name
    
    def __call__(self, message):
        print(f"[{self.analyzer_name}] {message}")

def test_analyzer(analyzer_class, analyzer_name, repo_path):
    """Test a single analyzer for performance and functionality"""
    print(f"\n{'='*60}")
    print(f"Testing {analyzer_name}")
    print(f"{'='*60}")
    
    try:
        # Initialize analyzer
        analyzer = analyzer_class(repo_path)
        progress_callback = MockProgressCallback(analyzer_name)
        
        # Record start time
        start_time = time.time()
        
        # Run analysis
        result = analyzer.analyze(progress_callback=progress_callback)
        
        # Record end time
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Check for errors
        if "error" in result:
            print(f"❌ ERROR in {analyzer_name}: {result['error']}")
            return False, execution_time
        
        # Validate result structure
        if not isinstance(result, dict) or len(result) == 0:
            print(f"❌ Invalid result structure for {analyzer_name}")
            return False, execution_time
        
        # Performance check
        if execution_time > 300:  # 5 minutes = 300 seconds
            print(f"⚠️  PERFORMANCE WARNING: {analyzer_name} took {execution_time:.2f} seconds (>{5} minutes)")
            return False, execution_time
        elif execution_time > 120:  # 2 minutes = warning
            print(f"⚠️  {analyzer_name} took {execution_time:.2f} seconds (>2 minutes but <5 minutes)")
        else:
            print(f"✅ {analyzer_name} completed successfully in {execution_time:.2f} seconds")
        
        # Print key metrics
        print(f"   Result keys: {len(result)} main sections")
        for key, value in result.items():
            if isinstance(value, list):
                print(f"   - {key}: {len(value)} items")
            elif isinstance(value, dict):
                print(f"   - {key}: {len(value)} sub-items")
            elif isinstance(value, (int, float)):
                print(f"   - {key}: {value}")
            else:
                print(f"   - {key}: {type(value).__name__}")
        
        return True, execution_time
        
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"❌ EXCEPTION in {analyzer_name}: {str(e)}")
        return False, execution_time

def main():
    """Main test runner"""
    print("AI Repository Analyzer - Comprehensive Performance Test")
    print("=" * 60)
    
    # Use current directory as repo path
    repo_path = Path.cwd()
    print(f"Testing repository: {repo_path}")
    
    # Define all analyzers to test
    analyzers = [
        (ExpertiseMappingAnalyzer, "Expertise Mapping"),
        (TechDebtAnalyzer, "Tech Debt Detection"),
        (RiskAnalyzer, "Risk Analysis"),
        (TimelineAnalyzer, "Timeline Analysis"),
        (VersionGovernanceAnalyzer, "Version Governance"),
        (DesignPatternsAnalyzer, "Design Patterns"),
        (DevelopmentPatternsAnalyzer, "Development Patterns"),
        (APIContractAnalyzer, "API Contracts"),
        (AIContextAnalyzer, "AI Context"),
        (SingularProductVisionAnalyzer, "Singular Product Vision")
    ]
    
    # Test results
    results = []
    total_start_time = time.time()
    
    # Run tests for each analyzer
    for analyzer_class, analyzer_name in analyzers:
        success, execution_time = test_analyzer(analyzer_class, analyzer_name, repo_path)
        results.append({
            "name": analyzer_name,
            "success": success,
            "time": execution_time
        })
    
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    successful_tests = 0
    failed_tests = 0
    performance_issues = 0
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        perf_warning = " ⚠️ SLOW" if result["time"] > 120 else ""
        print(f"{status:<10} {result['name']:<25} {result['time']:.2f}s{perf_warning}")
        
        if result["success"]:
            successful_tests += 1
        else:
            failed_tests += 1
        
        if result["time"] > 120:
            performance_issues += 1
    
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    print(f"Successful tests: {successful_tests}/{len(results)}")
    print(f"Failed tests: {failed_tests}")
    print(f"Performance issues (>2 minutes): {performance_issues}")
    
    # Performance goal check
    max_time = max(result["time"] for result in results)
    avg_time = sum(result["time"] for result in results) / len(results)
    
    print(f"\nPerformance Analysis:")
    print(f"- Fastest analyzer: {min(result['time'] for result in results):.2f} seconds")
    print(f"- Slowest analyzer: {max_time:.2f} seconds")
    print(f"- Average time: {avg_time:.2f} seconds")
    
    if max_time <= 300:  # 5 minutes
        print("✅ PERFORMANCE GOAL ACHIEVED: All analyzers complete under 5 minutes!")
    else:
        print("❌ PERFORMANCE GOAL NOT MET: Some analyzers take more than 5 minutes")
    
    if total_time <= 600:  # 10 minutes total
        print("✅ TOTAL TIME GOAL ACHIEVED: All analyzers complete under 10 minutes total!")
    else:
        print("❌ TOTAL TIME GOAL NOT MET: Total execution exceeds 10 minutes")
    
    # Overall result
    if failed_tests == 0 and max_time <= 300:
        print(f"\n🎉 ALL TESTS PASSED! Optimization successful!")
        return 0
    else:
        print(f"\n⚠️  Some issues found. See details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
