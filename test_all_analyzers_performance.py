#!/usr/bin/env python3
"""
Comprehensive Performance Test for All AI Repository Analyzers
Tests all optimized analyzers to ensure sub-5-minute completion time
"""

import time
import sys
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent))

from analyzers.expertise_mapping import ExpertiseMappingAnalyzer
from analyzers.tech_debt_detection import TechDebtAnalyzer
from analyzers.risk_analysis import RiskAnalyzer
from analyzers.timeline_analysis import TimelineAnalyzer
from analyzers.version_governance import VersionGovernanceAnalyzer
from analyzers.design_patterns import DesignPatternsAnalyzer
from analyzers.development_patterns import DevelopmentPatternsAnalyzer
from analyzers.api_contracts import APIContractsAnalyzer
from analyzers.ai_context import AIContextAnalyzer
from analyzers.singular_product_vision import SingularProductVisionAnalyzer

class PerformanceTestRunner:
    """Test runner for analyzer performance validation"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.results = {}
        self.max_time_limit = 300  # 5 minutes = 300 seconds
        
        # Initialize all analyzers
        self.analyzers = {
            "ExpertiseMapping": ExpertiseMappingAnalyzer(self.repo_path),
            "TechDebt": TechDebtAnalyzer(self.repo_path),
            "Risk": RiskAnalyzer(self.repo_path),
            "Timeline": TimelineAnalyzer(self.repo_path),
            "VersionGovernance": VersionGovernanceAnalyzer(self.repo_path),
            "DesignPatterns": DesignPatternsAnalyzer(self.repo_path),
            "DevelopmentPatterns": DevelopmentPatternsAnalyzer(self.repo_path),
            "APIContracts": APIContractsAnalyzer(self.repo_path),
            "AIContext": AIContextAnalyzer(self.repo_path),
            "SingularProductVision": SingularProductVisionAnalyzer(self.repo_path)
        }
        
        print(f"🚀 Performance Test Runner Initialized")
        print(f"📁 Repository Path: {self.repo_path.absolute()}")
        print(f"⏱️  Maximum Time Limit: {self.max_time_limit} seconds (5 minutes)")
        print(f"🔧 Analyzers to test: {len(self.analyzers)}")
        print("-" * 80)
    
    def test_analyzer(self, name: str, analyzer) -> dict:
        """Test a single analyzer performance"""
        
        print(f"\n🧪 Testing {name} Analyzer...")
        
        try:
            # Clear any existing cache for fair testing
            if hasattr(analyzer, '_cache'):
                analyzer._cache.clear()
            
            # Record start time
            start_time = time.time()
            
            # Run the analysis with progress callback
            def progress_callback(message):
                print(f"   📋 {message}")
            
            result = analyzer.analyze(progress_callback=progress_callback)
            
            # Record end time
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Check for errors
            if isinstance(result, dict) and "error" in result:
                return {
                    "success": False,
                    "execution_time": execution_time,
                    "error": result["error"],
                    "within_limit": execution_time <= self.max_time_limit
                }
            
            # Calculate performance metrics
            performance_result = {
                "success": True,
                "execution_time": execution_time,
                "within_limit": execution_time <= self.max_time_limit,
                "performance_rating": self._get_performance_rating(execution_time),
                "data_points": len(result) if isinstance(result, dict) else 0,
                "error": None
            }
            
            # Display results
            status = "✅ PASS" if performance_result["within_limit"] else "❌ FAIL"
            rating = performance_result["performance_rating"]
            
            print(f"   ⏱️  Execution Time: {execution_time:.2f} seconds")
            print(f"   🎯 Performance: {rating}")
            print(f"   📊 Data Points: {performance_result['data_points']}")
            print(f"   🔍 Status: {status}")
            
            return performance_result
            
        except Exception as e:
            execution_time = time.time() - start_time if 'start_time' in locals() else 0
            error_result = {
                "success": False,
                "execution_time": execution_time,
                "error": str(e),
                "within_limit": execution_time <= self.max_time_limit
            }
            
            print(f"   ❌ ERROR: {str(e)}")
            print(f"   ⏱️  Time before error: {execution_time:.2f} seconds")
            
            return error_result
    
    def _get_performance_rating(self, execution_time: float) -> str:
        """Get performance rating based on execution time"""
        if execution_time <= 30:
            return "🚀 ULTRA-FAST"
        elif execution_time <= 60:
            return "⚡ VERY FAST"
        elif execution_time <= 120:
            return "🏃 FAST"
        elif execution_time <= 240:
            return "🚶 ACCEPTABLE"
        elif execution_time <= 300:
            return "⚠️  BARELY ACCEPTABLE"
        else:
            return "🐌 TOO SLOW"
    
    def run_all_tests(self):
        """Run performance tests for all analyzers"""
        
        print("\n" + "="*80)
        print("🎯 STARTING COMPREHENSIVE ANALYZER PERFORMANCE TESTS")
        print("="*80)
        
        total_start_time = time.time()
        
        # Test each analyzer
        for name, analyzer in self.analyzers.items():
            test_result = self.test_analyzer(name, analyzer)
            self.results[name] = test_result
            
            # Short pause between tests
            time.sleep(1)
        
        total_end_time = time.time()
        total_execution_time = total_end_time - total_start_time
        
        # Generate summary report
        self._generate_summary_report(total_execution_time)
    
    def _generate_summary_report(self, total_time: float):
        """Generate comprehensive summary report"""
        
        print("\n" + "="*80)
        print("📊 PERFORMANCE TEST SUMMARY REPORT")
        print("="*80)
        
        # Count results
        passed_tests = sum(1 for r in self.results.values() if r["success"] and r["within_limit"])
        failed_tests = sum(1 for r in self.results.values() if not r["success"] or not r["within_limit"])
        total_tests = len(self.results)
        
        # Calculate total analysis time (if all run sequentially)
        total_analysis_time = sum(r["execution_time"] for r in self.results.values())
        
        print(f"\n📈 OVERALL RESULTS:")
        print(f"   ✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"   ❌ Tests Failed: {failed_tests}/{total_tests}")
        print(f"   📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"   ⏱️  Total Test Time: {total_time:.2f} seconds")
        print(f"   🔄 Total Analysis Time: {total_analysis_time:.2f} seconds")
        
        print(f"\n📋 DETAILED RESULTS:")
        print("-" * 80)
        
        # Sort results by execution time
        sorted_results = sorted(self.results.items(), key=lambda x: x[1]["execution_time"])
        
        for name, result in sorted_results:
            status_icon = "✅" if result["success"] and result["within_limit"] else "❌"
            time_str = f"{result['execution_time']:.2f}s"
            rating = result.get("performance_rating", "N/A")
            
            if result["error"]:
                print(f"   {status_icon} {name:20} | {time_str:>8} | ERROR: {result['error'][:50]}...")
            else:
                print(f"   {status_icon} {name:20} | {time_str:>8} | {rating}")
        
        print("-" * 80)
        
        # Performance insights
        print(f"\n🔍 PERFORMANCE INSIGHTS:")
        
        if passed_tests == total_tests:
            print("   🎉 EXCELLENT! All analyzers meet the 5-minute performance requirement!")
            print("   🚀 The optimization efforts have been successful!")
        elif passed_tests >= total_tests * 0.8:
            print("   ✅ GOOD! Most analyzers meet the performance requirement.")
            print("   🔧 Some minor optimizations needed for failing analyzers.")
        else:
            print("   ⚠️  WARNING! Many analyzers still exceed the 5-minute limit.")
            print("   🛠️  Significant optimization work is still required.")
        
        # Fastest and slowest
        fastest = min(sorted_results, key=lambda x: x[1]["execution_time"])
        slowest = max(sorted_results, key=lambda x: x[1]["execution_time"])
        
        print(f"\n   🏆 Fastest: {fastest[0]} ({fastest[1]['execution_time']:.2f}s)")
        print(f"   🐌 Slowest: {slowest[0]} ({slowest[1]['execution_time']:.2f}s)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        slow_analyzers = [name for name, result in self.results.items() 
                         if result["execution_time"] > 60]
        if slow_analyzers:
            print(f"   ⚡ Consider further optimization for: {', '.join(slow_analyzers)}")
        
        failed_analyzers = [name for name, result in self.results.items() 
                           if not result["success"] or not result["within_limit"]]
        if failed_analyzers:
            print(f"   🔧 Immediate attention needed for: {', '.join(failed_analyzers)}")
        
        if total_analysis_time < 300:
            print(f"   ✨ Total analysis time under 5 minutes - GOAL ACHIEVED!")
        else:
            print(f"   ⏰ Total analysis time: {total_analysis_time/60:.2f} minutes")
        
        print("\n" + "="*80)
        print("🏁 PERFORMANCE TEST COMPLETED")
        print("="*80)
    
    def run_quick_test(self):
        """Run a quick test of just a few analyzers"""
        
        print("\n🚀 RUNNING QUICK PERFORMANCE TEST")
        print("Testing 3 key analyzers...")
        
        quick_analyzers = {
            "ExpertiseMapping": self.analyzers["ExpertiseMapping"],
            "TechDebt": self.analyzers["TechDebt"],
            "Risk": self.analyzers["Risk"]
        }
        
        start_time = time.time()
        
        for name, analyzer in quick_analyzers.items():
            result = self.test_analyzer(name, analyzer)
            self.results[name] = result
        
        total_time = time.time() - start_time
        
        print(f"\n📊 Quick Test Results:")
        print(f"   ⏱️  Total Time: {total_time:.2f} seconds")
        
        all_passed = all(r["success"] and r["within_limit"] for r in self.results.values())
        if all_passed:
            print("   ✅ All quick tests PASSED!")
        else:
            print("   ❌ Some tests FAILED!")

def main():
    """Main function to run performance tests"""
    
    print("🧪 AI Repository Analyzer - Performance Test Suite")
    print("="*60)
    
    # Check if repository path is provided
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Create test runner
    runner = PerformanceTestRunner(repo_path)
    
    # Check command line arguments
    if len(sys.argv) > 2 and sys.argv[2] == "--quick":
        runner.run_quick_test()
    else:
        runner.run_all_tests()

if __name__ == "__main__":
    main()
