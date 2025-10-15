#!/usr/bin/env python3
"""
Test script to verify KeyError fixes in all analyzers
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from analyzers.version_governance import VersionGovernanceAnalyzer
from analyzers.tech_debt_detection import TechDebtAnalyzer
from analyzers.design_patterns import DesignPatternAnalyzer
from analyzers.development_patterns import DevelopmentPatternsAnalyzer

def test_analyzer_keyerror_fixes():
    """Test all analyzers for KeyError issues"""
    
    print("🧪 Testing analyzers for KeyError fixes...")
    print("=" * 50)
    
    repo_path = Path(".")  # Current directory
    
    # List of analyzers to test
    analyzers_to_test = [
        ("Version Governance", VersionGovernanceAnalyzer),
        ("Tech Debt Detection", TechDebtAnalyzer),
        ("Design Patterns", DesignPatternAnalyzer),
        ("Development Patterns", DevelopmentPatternsAnalyzer),
    ]
    
    results = {}
    
    for analyzer_name, analyzer_class in analyzers_to_test:
        print(f"🔍 Testing {analyzer_name} Analyzer...")
        
        try:
            # Initialize analyzer
            analyzer = analyzer_class(repo_path)
            
            # Test analysis (this is where KeyErrors would occur)
            analysis_result = analyzer.analyze()
            
            # Check if result has required keys and is not empty
            if isinstance(analysis_result, dict) and analysis_result:
                print(f"✅ {analyzer_name}: Analysis completed successfully")
                results[analyzer_name] = "PASS"
                
                # Check for specific keys that were causing issues
                if analyzer_name == "Development Patterns":
                    config_patterns = analysis_result.get("config_patterns", {})
                    if "environment_patterns" in config_patterns:
                        print(f"   ✅ environment_patterns key found")
                    else:
                        print(f"   ❌ environment_patterns key missing")
                        results[analyzer_name] = "PARTIAL"
                        
            else:
                print(f"❌ {analyzer_name}: Analysis returned empty or invalid result")
                results[analyzer_name] = "FAIL"
                
        except KeyError as e:
            print(f"❌ {analyzer_name}: KeyError - {str(e)}")
            results[analyzer_name] = f"KEYERROR: {str(e)}"
            
        except Exception as e:
            print(f"⚠️  {analyzer_name}: Other error - {str(e)}")
            results[analyzer_name] = f"ERROR: {str(e)}"
        
        print()
    
    # Summary
    print("📊 Test Results Summary:")
    print("=" * 30)
    
    passed = 0
    failed = 0
    
    for analyzer_name, result in results.items():
        status_icon = "✅" if result == "PASS" else "❌" if "KEYERROR" in result else "⚠️"
        print(f"{status_icon} {analyzer_name}: {result}")
        
        if result == "PASS":
            passed += 1
        else:
            failed += 1
    
    print()
    print(f"Total: {passed + failed} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("🎉 All analyzers are working correctly!")
        return True
    else:
        print("⚠️  Some analyzers still have issues")
        return False

if __name__ == "__main__":
    success = test_analyzer_keyerror_fixes()
    sys.exit(0 if success else 1)
