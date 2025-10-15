#!/usr/bin/env python3
"""
Quick performance verification script for optimized analyzers
"""
import sys
import time
import traceback

# Add current directory to path
sys.path.append('.')

def test_analyzer(analyzer_class, analyzer_name, repo_path='.'):
    """Test a single analyzer and return timing results"""
    try:
        print(f"Testing {analyzer_name}...")
        start_time = time.time()
        
        # Create and run analyzer
        analyzer = analyzer_class(repo_path)
        result = analyzer.analyze()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Check if result contains error
        if isinstance(result, dict) and "error" in result:
            return {
                "name": analyzer_name,
                "status": "ERROR",
                "duration": duration,
                "error": result["error"]
            }
        
        # Success
        return {
            "name": analyzer_name,
            "status": "SUCCESS",
            "duration": duration,
            "data_keys": list(result.keys()) if isinstance(result, dict) else "N/A"
        }
        
    except Exception as e:
        return {
            "name": analyzer_name,
            "status": "FAILED",
            "duration": time.time() - start_time if 'start_time' in locals() else 0,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

def main():
    print("=== AI Repository Analyzer Performance Verification ===")
    print(f"Starting performance test at {time.strftime('%H:%M:%S')}")
    print()
    
    # Import analyzers
    try:
        from analyzers.expertise_mapping import ExpertiseMapper
        from analyzers.tech_debt_detection import TechDebtDetectionAnalyzer
        from analyzers.design_patterns import DesignPatternAnalyzer
        from analyzers.risk_analysis import RiskAnalyzer
        from analyzers.timeline_analysis import TimelineAnalyzer
        print("✅ All analyzer imports successful!")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return
    
    # Test key optimized analyzers
    tests = [
        (ExpertiseMapper, "ExpertiseMapper"),
        (TechDebtDetectionAnalyzer, "TechDebtDetectionAnalyzer"), 
        (DesignPatternAnalyzer, "DesignPatternAnalyzer"),
        (RiskAnalyzer, "RiskAnalyzer"),
        (TimelineAnalyzer, "TimelineAnalyzer")
    ]
    
    results = []
    total_start = time.time()
    
    print("Running performance tests...")
    print("-" * 50)
    
    for analyzer_class, name in tests:
        result = test_analyzer(analyzer_class, name)
        results.append(result)
        
        status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
        print(f"{status_icon} {result['name']}: {result['duration']:.2f}s - {result['status']}")
        
        if result["status"] != "SUCCESS":
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    total_time = time.time() - total_start
    print("-" * 50)
    print(f"Total test time: {total_time:.2f} seconds")
    
    # Summary
    successful = [r for r in results if r["status"] == "SUCCESS"]
    failed = [r for r in results if r["status"] != "SUCCESS"]
    
    print(f"\n=== SUMMARY ===")
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        avg_time = sum(r["duration"] for r in successful) / len(successful)
        max_time = max(r["duration"] for r in successful)
        print(f"⏱️  Average time: {avg_time:.2f}s")
        print(f"⏱️  Max time: {max_time:.2f}s")
        
        # Check if all are under 5 minutes (300 seconds)
        over_limit = [r for r in successful if r["duration"] > 300]
        if over_limit:
            print(f"⚠️  {len(over_limit)} analyzers took over 5 minutes:")
            for r in over_limit:
                print(f"   - {r['name']}: {r['duration']:.2f}s")
        else:
            print("🎯 All successful analyzers completed under 5 minutes!")
    
    if failed:
        print(f"\n❌ Failed analyzers:")
        for r in failed:
            print(f"   - {r['name']}: {r.get('error', 'Unknown error')}")
    
    print(f"\nTest completed at {time.strftime('%H:%M:%S')}")
    return len(failed) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
