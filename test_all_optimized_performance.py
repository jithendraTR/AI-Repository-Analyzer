#!/usr/bin/env python3
"""
Comprehensive Performance Test for All Optimized Analyzers
Tests all analyzers to ensure they complete under 5 minutes total
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

def test_analyzer_performance():
    """Test all analyzers for sub-5-minute performance"""
    
    # Use current directory as test repo
    test_repo_path = project_root
    
    print("🚀 Starting Comprehensive Performance Test for All Optimized Analyzers")
    print(f"📁 Test Repository: {test_repo_path}")
    print("⏱️  Target: All analyzers complete under 5 minutes total")
    print("=" * 70)
    
    # All analyzer classes with their names
    analyzers_to_test = [
        ("Expertise Mapping", ExpertiseMappingAnalyzer),
        ("Tech Debt Detection", TechDebtAnalyzer),
        ("Risk Analysis", RiskAnalyzer),
        ("Timeline Analysis", TimelineAnalyzer),
        ("Version Governance", VersionGovernanceAnalyzer),
        ("Design Patterns", DesignPatternsAnalyzer),
        ("Development Patterns", DevelopmentPatternsAnalyzer),
        ("API Contracts", APIContractAnalyzer),
        ("AI Context", AIContextAnalyzer),
        ("Singular Product Vision", SingularProductVisionAnalyzer)
    ]
    
    overall_start_time = time.time()
    results = []
    total_errors = 0
    
    for analyzer_name, analyzer_class in analyzers_to_test:
        print(f"\n🔍 Testing {analyzer_name}...")
        
        try:
            # Initialize analyzer
            analyzer = analyzer_class(test_repo_path)
            
            # Test with progress callback
            def progress_callback(message):
                print(f"   ⏳ {message}")
            
            # Measure performance
            start_time = time.time()
            
            # Run analysis
            result = analyzer.analyze(progress_callback=progress_callback)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Check for errors
            if "error" in result:
                print(f"   ❌ ERROR: {result['error']}")
                total_errors += 1
                results.append({
                    "analyzer": analyzer_name,
                    "duration": duration,
                    "status": "ERROR",
                    "error": result['error']
                })
            else:
                # Check if analysis returned meaningful data
                non_empty_keys = [k for k, v in result.items() if v]
                data_quality = len(non_empty_keys)
                
                print(f"   ✅ SUCCESS: {duration:.2f}s ({data_quality} data fields)")
                results.append({
                    "analyzer": analyzer_name,
                    "duration": duration,
                    "status": "SUCCESS",
                    "data_quality": data_quality
                })
                
        except Exception as e:
            duration = time.time() - start_time if 'start_time' in locals() else 0
            print(f"   ❌ EXCEPTION: {str(e)}")
            total_errors += 1
            results.append({
                "analyzer": analyzer_name,
                "duration": duration,
                "status": "EXCEPTION",
                "error": str(e)
            })
    
    overall_end_time = time.time()
    total_duration = overall_end_time - overall_start_time
    
    # Print comprehensive results
    print("\n" + "=" * 70)
    print("📊 PERFORMANCE TEST RESULTS")
    print("=" * 70)
    
    successful_count = 0
    total_successful_time = 0
    
    for result in results:
        status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
        analyzer_name = result["analyzer"]
        duration = result["duration"]
        
        if result["status"] == "SUCCESS":
            successful_count += 1
            total_successful_time += duration
            data_quality = result.get("data_quality", 0)
            print(f"{status_icon} {analyzer_name:<25} {duration:>6.2f}s  ({data_quality} fields)")
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"{status_icon} {analyzer_name:<25} {duration:>6.2f}s  ERROR: {error_msg[:50]}...")
    
    print("-" * 70)
    print(f"📈 SUMMARY:")
    print(f"   Total Analyzers:     {len(analyzers_to_test)}")
    print(f"   Successful:          {successful_count}")
    print(f"   Failed:              {total_errors}")
    print(f"   Success Rate:        {(successful_count/len(analyzers_to_test)*100):.1f}%")
    print(f"   Total Time:          {total_duration:.2f}s ({total_duration/60:.2f} min)")
    print(f"   Successful Time:     {total_successful_time:.2f}s ({total_successful_time/60:.2f} min)")
    print(f"   Average per Success: {(total_successful_time/successful_count if successful_count > 0 else 0):.2f}s")
    
    # Performance assessment
    print("\n🎯 PERFORMANCE ASSESSMENT:")
    
    if total_duration <= 300:  # 5 minutes
        print(f"   ✅ EXCELLENT: Total time ({total_duration:.1f}s) is under 5 minutes!")
    elif total_duration <= 600:  # 10 minutes
        print(f"   ⚠️  GOOD: Total time ({total_duration:.1f}s) is under 10 minutes")
    else:
        print(f"   ❌ SLOW: Total time ({total_duration:.1f}s) exceeds 10 minutes")
    
    if successful_count == len(analyzers_to_test):
        print("   ✅ ALL ANALYZERS WORKING: No errors detected!")
    elif successful_count >= len(analyzers_to_test) * 0.8:
        print(f"   ⚠️  MOSTLY WORKING: {successful_count}/{len(analyzers_to_test)} analyzers successful")
    else:
        print(f"   ❌ MAJOR ISSUES: Only {successful_count}/{len(analyzers_to_test)} analyzers successful")
    
    if total_successful_time <= 180:  # 3 minutes
        print("   🚀 ULTRA-FAST: Successful analyzers complete in under 3 minutes!")
    elif total_successful_time <= 300:  # 5 minutes
        print("   ✅ FAST: Successful analyzers complete in under 5 minutes!")
    else:
        print("   ⚠️  NEEDS OPTIMIZATION: Successful analyzers take over 5 minutes")
    
    print("\n" + "=" * 70)
    
    # Return results for further analysis if needed
    return {
        "total_duration": total_duration,
        "successful_count": successful_count,
        "total_count": len(analyzers_to_test),
        "results": results,
        "meets_performance_goal": total_duration <= 300 and successful_count == len(analyzers_to_test)
    }

if __name__ == "__main__":
    test_results = test_analyzer_performance()
    
    # Exit with appropriate code
    if test_results["meets_performance_goal"]:
        print("🎉 ALL PERFORMANCE GOALS MET!")
        sys.exit(0)
    else:
        print("⚠️  Performance goals not fully met - see results above")
        sys.exit(1)
