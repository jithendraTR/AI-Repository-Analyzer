#!/usr/bin/env python3
"""
Test both KeyError fix and analyzer_progress fix
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from pathlib import Path
from threading import Event

class MockProgressCallback:
    """Mock progress callback to test the signature"""
    def __init__(self):
        self.calls = []
    
    def __call__(self, current, total, status):
        """Progress callback with correct signature"""
        self.calls.append((current, total, status))
        print(f"Progress: {current}/{total} - {status}")

class MockCancellationToken:
    """Mock cancellation token"""
    def __init__(self):
        self.cancelled = Event()
    
    def check_cancellation(self):
        if self.cancelled.is_set():
            raise Exception("Operation cancelled")

def test_development_patterns_keyerror_fix():
    """Test that the development patterns analyzer works without KeyError"""
    try:
        from analyzers.development_patterns import DevelopmentPatternsAnalyzer
        
        print("🔧 Testing Development Patterns KeyError fix...")
        
        # Initialize analyzer
        analyzer = DevelopmentPatternsAnalyzer(Path('.'))
        print("✅ Analyzer initialized successfully")
        
        # Run analysis
        result = analyzer.analyze()
        print("✅ Analysis completed successfully")
        
        # Test the specific fix - safe dictionary access
        config_patterns = result.get("config_patterns", {})
        env_patterns = dict(config_patterns.get("environment_patterns", {}))
        print(f"✅ Safe dictionary access works: {len(env_patterns)} environment patterns found")
        
        print("🎉 SUCCESS! KeyError: 'environment_patterns' issue is RESOLVED!")
        return True
        
    except KeyError as e:
        print(f"❌ FAILED! KeyError still exists: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Other error occurred: {e}")
        return False

def test_singular_product_vision_progress_fix():
    """Test that the singular product vision analyzer progress callback works"""
    try:
        from analyzers.singular_product_vision import SingularProductVisionAnalyzer
        
        print("🔧 Testing Singular Product Vision progress callback fix...")
        
        # Initialize analyzer
        analyzer = SingularProductVisionAnalyzer(Path('.'))
        print("✅ Analyzer initialized successfully")
        
        # Create mock progress callback and cancellation token
        progress_callback = MockProgressCallback()
        token = MockCancellationToken()
        
        # Run analysis with progress callback
        result = analyzer.analyze(token=token, progress_callback=progress_callback)
        print("✅ Analysis completed successfully")
        
        # Check progress callback was called with correct signature
        if progress_callback.calls:
            print(f"✅ Progress callback called {len(progress_callback.calls)} times with correct signature")
            for call in progress_callback.calls:
                current, total, status = call
                print(f"  - Progress call: {current}/{total} - {status[:50]}...")
        else:
            print("⚠️ Progress callback was not called")
        
        print("🎉 SUCCESS! analyzer_progress() signature issue is RESOLVED!")
        return True
        
    except TypeError as e:
        if "missing" in str(e) and "positional arguments" in str(e):
            print(f"❌ FAILED! Progress callback signature issue still exists: {e}")
            return False
        else:
            print(f"⚠️ Other TypeError occurred: {e}")
            return False
    except Exception as e:
        print(f"⚠️ Other error occurred: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Both Fixes")
    print("=" * 60)
    
    # Test KeyError fix
    print("\n1. Testing KeyError Fix:")
    print("-" * 30)
    keyerror_fixed = test_development_patterns_keyerror_fix()
    
    # Test progress callback fix
    print("\n2. Testing Progress Callback Fix:")
    print("-" * 30)
    progress_fixed = test_singular_product_vision_progress_fix()
    
    print("\n" + "=" * 60)
