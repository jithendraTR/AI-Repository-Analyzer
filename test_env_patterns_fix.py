#!/usr/bin/env python3
"""
Focused test to verify environment_patterns KeyError fix
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from analyzers.development_patterns import DevelopmentPatternsAnalyzer

def test_development_patterns_keyerror():
    """Test that DevelopmentPatternsAnalyzer doesn't throw KeyError for environment_patterns"""
    
    print("🔍 Testing Development Patterns Analyzer for environment_patterns KeyError...")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        repo_path = Path(".")
        analyzer = DevelopmentPatternsAnalyzer(repo_path)
        
        # Test analysis method
        print("1️⃣ Testing analyze() method...")
        result = analyzer.analyze()
        
        # Check if the result has the expected structure
        if "config_patterns" in result:
            config_patterns = result["config_patterns"]
            
            if "environment_patterns" in config_patterns:
                print("   ✅ environment_patterns key found in analyze() result")
                print(f"   📊 Content: {config_patterns['environment_patterns']}")
            else:
                print("   ❌ environment_patterns key missing in analyze() result")
                return False
                
        else:
            print("   ❌ config_patterns key missing in analyze() result")
            return False
        
        # Test render method access pattern
        print("2️⃣ Testing render() method access pattern...")
        try:
            # This simulates what the render method does
            env_patterns = dict(config_patterns.get("environment_patterns", {}))
            print(f"   ✅ render() method access pattern works: {env_patterns}")
        except KeyError as e:
            print(f"   ❌ render() method would fail: {e}")
            return False
        
        print("\n🎉 SUCCESS: All tests passed! No KeyError issues detected.")
        return True
        
    except KeyError as e:
        print(f"❌ KeyError detected: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Other error: {e}")
        return False

if __name__ == "__main__":
    success = test_development_patterns_keyerror()
    if success:
        print("\n✅ FINAL RESULT: environment_patterns KeyError has been FIXED!")
    else:
        print("\n❌ FINAL RESULT: environment_patterns KeyError still exists!")
    
    sys.exit(0 if success else 1)
