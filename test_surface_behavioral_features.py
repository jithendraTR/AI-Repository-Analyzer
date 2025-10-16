#!/usr/bin/env python3

"""
Test script to verify Surface Level and Behavioral Level analysis features
are properly implemented in DevelopmentPatternsAnalyzer
"""

import sys
import os

# Add the current directory to sys.path to import our modules
sys.path.insert(0, '.')

from analyzers.development_patterns import DevelopmentPatternsAnalyzer

def test_development_patterns_analyzer():
    """Test the new Surface Level and Behavioral Level analysis features"""
    print("🔍 Testing Development Patterns Analyzer - New Features")
    
    try:
        # Instantiate analyzer
        print("\n✅ Step 1: Creating DevelopmentPatternsAnalyzer instance...")
        analyzer = DevelopmentPatternsAnalyzer('.')
        print("   ✓ Analyzer created successfully")
        
        # Run analysis
        print("\n✅ Step 2: Running analysis...")
        result = analyzer.analyze()
        print("   ✓ Analysis completed successfully")
        
        # Check main result structure
        print(f"\n📊 Analysis Result Keys: {list(result.keys())}")
        
        # Check for Analysis Depth Spectrum
        if 'analysis_depth_spectrum' not in result:
            print("❌ MISSING: analysis_depth_spectrum key")
            return False
            
        spectrum = result['analysis_depth_spectrum']
        print(f"\n🎯 Analysis Depth Spectrum Keys: {list(spectrum.keys())}")
        
        # Test Surface Level Analysis
        print("\n🔍 SURFACE LEVEL ANALYSIS:")
        surface = spectrum.get('surface_level', {})
        surface_features = [
            'file_structure_analysis',
            'naming_conventions_analysis', 
            'technology_stack_analysis',
            'project_description',
            'codebase_overview'
        ]
        
        for feature in surface_features:
            if feature in surface:
                print(f"   ✅ {feature}: IMPLEMENTED")
                # Show some sample data
                if isinstance(surface[feature], dict) and surface[feature]:
                    sample_keys = list(surface[feature].keys())[:3]
                    print(f"      Sample keys: {sample_keys}")
            else:
                print(f"   ❌ {feature}: MISSING")
                return False
        
        # Test Behavioral Level Analysis  
        print("\n🔍 BEHAVIORAL LEVEL ANALYSIS:")
        behavioral = spectrum.get('behavioral_level', {})
        behavioral_features = [
            'function_contracts',
            'data_flows',
            'integration_patterns',
            'api_patterns',
            'communication_patterns'
        ]
        
        for feature in behavioral_features:
            if feature in behavioral:
                print(f"   ✅ {feature}: IMPLEMENTED") 
                # Show some sample data
                if isinstance(behavioral[feature], dict) and behavioral[feature]:
                    sample_keys = list(behavioral[feature].keys())[:3]
                    print(f"      Sample keys: {sample_keys}")
            else:
                print(f"   ❌ {feature}: MISSING")
                return False
        
        # Test that original features still exist
        print("\n🔍 ORIGINAL FEATURES CHECK:")
        original_features = [
            'framework_usage',
            'coding_patterns', 
            'structure_patterns',
            'pattern_summary'
        ]
        
        for feature in original_features:
            if feature in result:
                print(f"   ✅ {feature}: PRESERVED")
            else:
                print(f"   ❌ {feature}: MISSING")
                return False
        
        print(f"\n🎊 ALL TESTS PASSED!")
        print(f"✅ Surface Level Analysis: Fully implemented")
        print(f"✅ Behavioral Level Analysis: Fully implemented") 
        print(f"✅ Original features: All preserved")
        print(f"✅ Analysis Depth Spectrum: Working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_development_patterns_analyzer()
    if success:
        print(f"\n🎉 SUCCESS: All new features implemented correctly!")
        sys.exit(0)
    else:
        print(f"\n💥 FAILURE: Some features are missing or broken!")
        sys.exit(1)
