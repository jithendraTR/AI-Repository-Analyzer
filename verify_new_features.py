#!/usr/bin/env python3

"""
Verification script for the new Development Patterns Analysis Depth Spectrum features
"""

import sys
sys.path.insert(0, '.')

from analyzers.development_patterns import DevelopmentPatternsAnalyzer

def main():
    print("🔍 Verifying Development Patterns Analysis Depth Spectrum Features")
    print("="*70)
    
    try:
        # Create analyzer instance
        analyzer = DevelopmentPatternsAnalyzer('.')
        print("✅ DevelopmentPatternsAnalyzer created successfully")
        
        # Run analysis
        result = analyzer.analyze()
        print("✅ Analysis completed successfully")
        
        # Check for Analysis Depth Spectrum
        if 'analysis_depth_spectrum' not in result:
            print("❌ MISSING: analysis_depth_spectrum key")
            return False
        
        spectrum = result['analysis_depth_spectrum']
        print(f"✅ Analysis Depth Spectrum found with keys: {list(spectrum.keys())}")
        
        # Verify Surface Level Analysis
        surface_level = spectrum.get('surface_level', {})
        surface_features = [
            'file_structure_analysis',
            'naming_conventions_analysis',
            'technology_stack_analysis',
            'project_description',
            'codebase_overview'
        ]
        
        print("\n🔍 SURFACE LEVEL ANALYSIS VERIFICATION:")
        all_surface_present = True
        for feature in surface_features:
            if feature in surface_level:
                print(f"  ✅ {feature}: IMPLEMENTED")
            else:
                print(f"  ❌ {feature}: MISSING")
                all_surface_present = False
        
        # Verify Behavioral Level Analysis
        behavioral_level = spectrum.get('behavioral_level', {})
        behavioral_features = [
            'function_contracts',
            'data_flows',
            'integration_patterns',
            'api_patterns',
            'communication_patterns'
        ]
        
        print("\n🔍 BEHAVIORAL LEVEL ANALYSIS VERIFICATION:")
        all_behavioral_present = True
        for feature in behavioral_features:
            if feature in behavioral_level:
                print(f"  ✅ {feature}: IMPLEMENTED")
            else:
                print(f"  ❌ {feature}: MISSING")
                all_behavioral_present = False
        
        # Verify original features still exist
        original_features = [
            'framework_usage',
            'coding_patterns',
            'structure_patterns',
            'pattern_summary'
        ]
        
        print("\n🔍 ORIGINAL FEATURES VERIFICATION:")
        all_original_present = True
        for feature in original_features:
            if feature in result:
                print(f"  ✅ {feature}: PRESERVED")
            else:
                print(f"  ❌ {feature}: MISSING")
                all_original_present = False
        
        # Final assessment
        print("\n" + "="*70)
        if all_surface_present and all_behavioral_present and all_original_present:
            print("🎉 SUCCESS: All requested features have been implemented!")
            print("✅ Surface Level Analysis: Complete")
            print("✅ Behavioral Level Analysis: Complete")
            print("✅ Original functionality: Preserved")
            return True
        else:
            print("❌ PARTIAL SUCCESS: Some features are missing")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during verification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
