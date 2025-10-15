#!/usr/bin/env python3
"""Simple performance test for optimized analyzers"""

import time
import sys
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent))

def test_expertise_mapping():
    """Test the expertise mapping analyzer"""
    try:
        from analyzers.expertise_mapping import ExpertiseMappingAnalyzer
        
        print("🧪 Testing ExpertiseMapping Analyzer...")
        analyzer = ExpertiseMappingAnalyzer(".")
        
        start_time = time.time()
        result = analyzer.analyze()
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"✅ ExpertiseMapping completed in {execution_time:.2f} seconds")
        
        if execution_time <= 300:  # 5 minutes
            print("🎉 PASSED: Under 5-minute limit!")
        else:
            print("❌ FAILED: Exceeded 5-minute limit")
            
        return execution_time < 300
        
    except Exception as e:
        print(f"❌ ERROR in ExpertiseMapping: {e}")
        return False

def test_tech_debt():
    """Test the tech debt analyzer"""
    try:
        from analyzers.tech_debt_detection import TechDebtAnalyzer
        
        print("\n🧪 Testing TechDebt Analyzer...")
        analyzer = TechDebtAnalyzer(".")
        
        start_time = time.time()
        result = analyzer.analyze()
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"✅ TechDebt completed in {execution_time:.2f} seconds")
        
        if execution_time <= 300:  # 5 minutes
            print("🎉 PASSED: Under 5-minute limit!")
        else:
            print("❌ FAILED: Exceeded 5-minute limit")
            
        return execution_time < 300
        
    except Exception as e:
        print(f"❌ ERROR in TechDebt: {e}")
        return False

def test_risk_analysis():
    """Test the risk analyzer"""
    try:
        from analyzers.risk_analysis import RiskAnalyzer
        
        print("\n🧪 Testing Risk Analyzer...")
        analyzer = RiskAnalyzer(".")
        
        start_time = time.time()
        result = analyzer.analyze()
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"✅ Risk completed in {execution_time:.2f} seconds")
        
        if execution_time <= 300:  # 5 minutes
            print("🎉 PASSED: Under 5-minute limit!")
        else:
            print("❌ FAILED: Exceeded 5-minute limit")
            
        return execution_time < 300
        
    except Exception as e:
        print(f"❌ ERROR in Risk: {e}")
        return False

def main():
    """Run simple performance tests"""
    print("🚀 Simple Performance Test for AI Repository Analyzers")
    print("=" * 60)
    
    tests = [
        test_expertise_mapping,
        test_tech_debt,
        test_risk_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\n📊 Summary:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Optimizations successful!")
    else:
        print("⚠️  Some tests failed. Further optimization needed.")

if __name__ == "__main__":
    main()
