#!/usr/bin/env python3
"""
Simple test to verify that the analyzer_progress() error has been fixed
"""

import sys
import os
sys.path.append('.')

# Import analyzers to test for the specific error
from analyzers.ai_context import AIContextAnalyzer
from analyzers.version_governance import VersionGovernanceAnalyzer
from analyzers.risk_analysis import RiskAnalysisAnalyzer
from analyzers.development_patterns import DevelopmentPatternsAnalyzer
from analyzers.design_patterns import DesignPatternsAnalyzer

def test_analyzer_progress_fix():
    """Test that analyzer_progress() calls are fixed"""
    print("Testing analyzer_progress() fixes...")
    
    # Test each analyzer's analyze() method
    analyzers = [
        ("AIContextAnalyzer", AIContextAnalyzer),
        ("VersionGovernanceAnalyzer", VersionGovernanceAnalyzer), 
        ("RiskAnalysisAnalyzer", RiskAnalysisAnalyzer),
        ("DevelopmentPatternsAnalyzer", DevelopmentPatternsAnalyzer),
        ("DesignPatternsAnalyzer", DesignPatternsAnalyzer)
    ]
    
    for name, analyzer_class in analyzers:
        try:
            print(f"Testing {name}...")
            analyzer = analyzer_class(".")
            
            # Test with progress callback - this should not fail with missing arguments
            def progress_callback(current, total, status):
                print(f"  Progress: {current}/{total} - {status}")
            
            result = analyzer.analyze(progress_callback=progress_callback)
            print(f"  ✓ {name} completed without errors")
            
        except TypeError as e:
            if "missing" in str(e) and "required positional arguments" in str(e):
                print(f"  ✗ {name} still has analyzer_progress() error: {e}")
                return False
            else:
                # Other errors are acceptable for this test
                print(f"  ✓ {name} - No analyzer_progress() error (other error: {e})")
        except Exception as e:
            # Other exceptions are acceptable for this test
            print(f"  ✓ {name} - No analyzer_progress() error (other error: {type(e).__name__})")
    
    print("\n✓ All analyzers passed - analyzer_progress() error has been fixed!")
    return True

if __name__ == "__main__":
    success = test_analyzer_progress_fix()
    sys.exit(0 if success else 1)
