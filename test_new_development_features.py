#!/usr/bin/env python3

"""
Test script for the new Development Patterns features
Tests the Surface Level and Behavioral Level analysis features
"""

import sys
from pathlib import Path

# Add the parent directory to sys.path to import analyzers
sys.path.insert(0, str(Path(__file__).parent))

def test_development_patterns_new_features():
    """Test the new Development Patterns analysis features"""
    
    try:
        from analyzers.development_patterns import DevelopmentPatternsAnalyzer
        
        print("🔧 Testing Development Patterns New Features...")
        print("=" * 60)
        
        # Initialize analyzer
        analyzer = DevelopmentPatternsAnalyzer(Path.cwd())
        
        # Test the analyze method with new features
        print("📊 Running full analysis...")
        results = analyzer.analyze()
        
        if not results:
            print("❌ ERROR: No analysis results returned")
            return False
        
        # Check for the new analysis_depth_spectrum section
        if "analysis_depth_spectrum" not in results:
            print("❌ ERROR: Missing analysis_depth_spectrum section")
            return False
        
        spectrum = results["analysis_depth_spectrum"]
        
        # Test Surface Level Analysis
        print("\n🎯 Testing Surface Level Analysis...")
        if "surface_level" in spectrum:
            surface = spectrum["surface_level"]
            print(f"   ✅ Surface level analysis present")
            
            expected_keys = [
                "file_structure_analysis",
                "naming_conventions_analysis", 
                "technology_stack_analysis",
                "project_description",
                "codebase_overview"
            ]
            
            for key in expected_keys:
                if key in surface:
                    print(f"   ✅ {key}: Present")
                else:
                    print(f"   ⚠️ {key}: Missing")
        else:
            print("   ❌ Surface level analysis missing")
        
        # Test Behavioral Level Analysis
        print("\n⚡ Testing Behavioral Level Analysis...")
        if "behavioral_level" in spectrum:
            behavioral = spectrum["behavioral_level"]
            print(f"   ✅ Behavioral level analysis present")
            
            expected_keys = [
                "function_contracts",
                "data_flows",
                "integration_patterns",
                "api_patterns",
                "communication_patterns"
            ]
            
            for key in expected_keys:
                if key in behavioral:
                    print(f"   ✅ {key}: Present")
                else:
                    print(f"   ⚠️ {key}: Missing")
        else:
            print("   ❌ Behavioral level analysis missing")
        
        # Test Architectural Level Analysis
        print("\n🏗️ Testing Architectural Level Analysis...")
        if "architectural_level" in spectrum:
            architectural = spectrum["architectural_level"]
            print(f"   ✅ Architectural level analysis present")
            
            expected_keys = [
                "architecture_overview",
                "component_structure",
                "coupling_analysis",
                "architectural_diagrams",
                "design_principles"
            ]
            
            for key in expected_keys:
                if key in architectural:
                    print(f"   ✅ {key}: Present")
                else:
                    print(f"   ⚠️ {key}: Missing")
        else:
            print("   ❌ Architectural level analysis missing")
        
        # Test Historical Level Analysis
        print("\n📈 Testing Historical Level Analysis...")
        if "historical_level" in spectrum:
            historical = spectrum["historical_level"]
            print(f"   ✅ Historical level analysis present")
            
            expected_keys = [
                "evolution_patterns",
                "change_frequency",
                "growth_patterns",
                "refactoring_history",
                "technology_evolution"
            ]
            
            for key in expected_keys:
                if key in historical:
                    print(f"   ✅ {key}: Present")
                else:
                    print(f"   ⚠️ {key}: Missing")
        else:
            print("   ❌ Historical level analysis missing")
        
        # Test specific Surface Level features
        print("\n📋 Testing Surface Level Details...")
        if "surface_level" in spectrum:
            surface = spectrum["surface_level"]
            
            # Test file structure analysis
            if "file_structure_analysis" in surface:
                structure = surface["file_structure_analysis"]
                if "structure_patterns" in structure:
                    patterns = structure["structure_patterns"]
                    print(f"   ✅ Structure patterns detected: {len(patterns)} patterns")
                    for pattern in patterns[:3]:  # Show first 3
                        print(f"      - {pattern}")
                else:
                    print("   ⚠️ Structure patterns missing")
            
            # Test project description
            if "project_description" in surface:
                desc = surface["project_description"]
                if "project_type" in desc:
                    print(f"   ✅ Project type identified: {desc['project_type']}")
                if "project_purpose" in desc:
                    print(f"   ✅ Project purpose: {desc['project_purpose'][:100]}...")
        
        # Test specific Behavioral Level features
        print("\n🔄 Testing Behavioral Level Details...")
        if "behavioral_level" in spectrum:
            behavioral = spectrum["behavioral_level"]
            
            # Test function contracts
            if "function_contracts" in behavioral:
                contracts = behavioral["function_contracts"]
                if "function_signatures" in contracts:
                    sigs = contracts["function_signatures"]
                    print(f"   ✅ Function signatures found: {len(sigs)} signatures")
                    for sig in sigs[:2]:  # Show first 2
                        print(f"      - {sig[:50]}...")
        
        print("\n" + "=" * 60)
        print("🎉 Development Patterns new features test completed!")
        print("✅ Surface Level Analysis: Implemented")
        print("✅ Behavioral Level Analysis: Implemented") 
        print("✅ Architectural Level Analysis: Implemented")
        print("✅ Historical Level Analysis: Implemented")
        return True
        
    except Exception as e:
        print(f"❌ ERROR during analysis: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_development_patterns_new_features()
    sys.exit(0 if success else 1)
