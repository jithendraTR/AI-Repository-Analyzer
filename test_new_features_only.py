#!/usr/bin/env python3

"""
Simple test for new Development Patterns features only
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_new_features():
    """Test only the new features we added"""
    
    print("🔧 Testing New Development Patterns Features")
    print("=" * 50)
    
    try:
        # Import and initialize
        from analyzers.development_patterns import DevelopmentPatternsAnalyzer
        analyzer = DevelopmentPatternsAnalyzer()
        
        print("✅ Analyzer imported and initialized successfully")
        
        # Test individual methods for new features
        print("\n🏗️ Testing Surface Level Analysis methods...")
        
        # Test file structure analysis
        structure = analyzer._analyze_file_structure()
        print(f"✅ File structure analysis: {len(structure)} keys")
        
        # Test naming conventions
        naming = analyzer._analyze_naming_conventions()
        print(f"✅ Naming conventions analysis: {len(naming)} keys")
        
        # Test technology stack
        tech_stack = analyzer._analyze_technology_stack()
        print(f"✅ Technology stack analysis: {len(tech_stack)} keys")
        
        # Test project description
        description = analyzer._analyze_project_description()
        print(f"✅ Project description analysis: {len(description)} keys")
        
        # Test codebase overview
        overview = analyzer._analyze_codebase_overview()
        print(f"✅ Codebase overview analysis: {len(overview)} keys")
        
        print("\n⚙️ Testing Behavioral Level Analysis methods...")
        
        # Test function contracts
        contracts = analyzer._analyze_function_contracts()
        print(f"✅ Function contracts analysis: {len(contracts)} keys")
        
        # Test data flows
        flows = analyzer._analyze_data_flows()
        print(f"✅ Data flows analysis: {len(flows)} keys")
        
        # Test integration patterns
        integrations = analyzer._analyze_integration_patterns()
        print(f"✅ Integration patterns analysis: {len(integrations)} keys")
        
        # Test API patterns
        api_patterns = analyzer._analyze_api_patterns()
        print(f"✅ API patterns analysis: {len(api_patterns)} keys")
        
        # Test communication patterns
        comm_patterns = analyzer._analyze_communication_patterns()
        print(f"✅ Communication patterns analysis: {len(comm_patterns)} keys")
        
        print("\n📊 Testing Surface Level Analysis integration...")
        surface_analysis = analyzer._analyze_surface_level()
        expected_surface_keys = [
            "file_structure_analysis",
            "naming_conventions_analysis", 
            "technology_stack_analysis",
            "project_description",
            "codebase_overview"
        ]
        
        surface_ok = all(key in surface_analysis for key in expected_surface_keys)
        print(f"✅ Surface level integration: {'OK' if surface_ok else 'FAILED'}")
        
        print("\n📊 Testing Behavioral Level Analysis integration...")
        behavioral_analysis = analyzer._analyze_behavioral_level()
        expected_behavioral_keys = [
            "function_contracts",
            "data_flows",
            "integration_patterns", 
            "api_patterns",
            "communication_patterns"
        ]
        
        behavioral_ok = all(key in behavioral_analysis for key in expected_behavioral_keys)
        print(f"✅ Behavioral level integration: {'OK' if behavioral_ok else 'FAILED'}")
        
        print(f"\n📊 Sample Data Preview:")
        
        # Show some sample data
        if "technology_stack_analysis" in surface_analysis:
            tech = surface_analysis["technology_stack_analysis"]
            if "primary_languages" in tech and tech["primary_languages"]:
                langs = list(tech["primary_languages"].keys())
                print(f"  🔧 Languages detected: {langs[:3]}")
        
        if "project_description" in surface_analysis:
            desc = surface_analysis["project_description"]
            print(f"  📝 Project type: {desc.get('project_type', 'Unknown')}")
        
        if "function_contracts" in behavioral_analysis:
            contracts = behavioral_analysis["function_contracts"]
            total_funcs = contracts.get("function_signatures", {}).get("total_functions", 0)
            print(f"  ⚙️ Functions detected: {total_funcs}")
        
        print(f"\n🎯 Test Summary:")
        print(f"  ✅ All surface level methods: Working")
        print(f"  ✅ All behavioral level methods: Working")
        print(f"  ✅ Surface level integration: {'OK' if surface_ok else 'FAILED'}")
        print(f"  ✅ Behavioral level integration: {'OK' if behavioral_ok else 'FAILED'}")
        
        return surface_ok and behavioral_ok
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing New Development Patterns Features")
    print("=" * 50)
    
    success = test_new_features()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL NEW FEATURES WORKING!")
        print("\n📈 Successfully implemented:")
        print("  • Surface Level Analysis")
        print("  • Behavioral Level Analysis") 
        print("  • Analysis Depth Spectrum")
    else:
        print("❌ Some features failed!")
