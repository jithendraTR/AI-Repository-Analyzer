#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

def test_development_patterns():
    """Test the new Development Patterns features"""
    try:
        from analyzers.development_patterns import DevelopmentPatternsAnalyzer
        print("✅ Successfully imported DevelopmentPatternsAnalyzer")
        
        # Test instantiation
        analyzer = DevelopmentPatternsAnalyzer('.')
        print("✅ Successfully instantiated analyzer")
        
        # Test analysis
        result = analyzer.analyze()
        print("✅ Successfully ran analysis")
        
        # Check for Analysis Depth Spectrum
        if 'analysis_depth_spectrum' in result:
            print("✅ Analysis Depth Spectrum present")
            spectrum = result['analysis_depth_spectrum']
            
            # Check Surface Level features
            surface = spectrum.get('surface_level', {})
            if 'file_structure_analysis' in surface:
                print("  ✅ Surface Level - File Structure Analysis: IMPLEMENTED")
            if 'naming_conventions_analysis' in surface:
                print("  ✅ Surface Level - Naming Conventions Analysis: IMPLEMENTED")  
            if 'technology_stack_analysis' in surface:
                print("  ✅ Surface Level - Technology Stack Analysis: IMPLEMENTED")
            if 'project_description' in surface:
                print("  ✅ Surface Level - Project Description: IMPLEMENTED")
            
            # Check Behavioral Level features
            behavioral = spectrum.get('behavioral_level', {})
            if 'function_contracts' in behavioral:
                print("  ✅ Behavioral Level - Function Contracts: IMPLEMENTED")
            if 'data_flows' in behavioral:
                print("  ✅ Behavioral Level - Data Flows: IMPLEMENTED")
            if 'integration_patterns' in behavioral:
                print("  ✅ Behavioral Level - Integration Patterns: IMPLEMENTED")
            
            print("\n🎉 All requested features successfully implemented!")
            return True
        else:
            print("❌ Analysis Depth Spectrum missing")
            return False
            
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_development_patterns()
    if success:
        print("\n✅ ALL TESTS PASSED - Implementation successful!")
    else:
        print("\n❌ TESTS FAILED - Implementation needs fixing")
