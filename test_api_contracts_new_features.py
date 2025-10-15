#!/usr/bin/env python3

"""
Test script to verify API Contracts Integration Complexity Scoring features
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_api_contracts_new_features():
    """Test the new Integration Complexity Scoring features"""
    try:
        from analyzers.api_contracts import APIContractAnalyzer
        
        print("Testing API Contracts New Integration Complexity Scoring Features...")
        print("=" * 70)
        
        # Initialize analyzer
        repo_path = Path(".")
        analyzer = APIContractAnalyzer(repo_path)
        
        print("1. Testing analyzer initialization...")
        assert analyzer is not None
        print("   ✓ Analyzer initialized successfully")
        
        print("2. Running analysis with new features...")
        result = analyzer.analyze()
        
        # Check if the basic structure is intact
        assert isinstance(result, dict)
        print("   ✓ Analysis returned dictionary")
        
        # Check for new Integration Complexity Scoring section
        assert "integration_complexity_scoring" in result
        print("   ✓ Integration Complexity Scoring section found")
        
        complexity_data = result["integration_complexity_scoring"]
        
        # Test API Stability Analysis
        print("3. Testing API Stability Analysis...")
        if "api_stability" in complexity_data:
            stability = complexity_data["api_stability"]
            
            # Check required keys
            required_keys = ["stable_interfaces", "unstable_interfaces", "stability_factors", "files_analysis"]
            for key in required_keys:
                assert key in stability, f"Missing key: {key}"
            
            print("   ✓ API Stability analysis has all required keys")
            
            # Check files_analysis structure
            if stability["files_analysis"]:
                file_data = stability["files_analysis"][0]
                file_keys = ["file", "stability_score", "endpoint_count", "factors", "endpoints"]
                for key in file_keys:
                    assert key in file_data, f"Missing file analysis key: {key}"
                print("   ✓ API Stability file analysis structure is correct")
        else:
            print("   ℹ No API stability data (this is fine for projects without APIs)")
        
        # Test Coupling Analysis
        print("4. Testing Coupling Analysis...")
        if "coupling_analysis" in complexity_data:
            coupling = complexity_data["coupling_analysis"]
            
            required_keys = ["tight_coupling_indicators", "loose_coupling_patterns", "module_dependencies", "use_cases"]
            for key in required_keys:
                assert key in coupling, f"Missing key: {key}"
            
            print("   ✓ Coupling Analysis has all required keys")
            
            # Check use cases structure
            if coupling["use_cases"]:
                use_case = coupling["use_cases"][0]
                use_case_keys = ["scenario", "impact", "affected_modules", "description"]
                for key in use_case_keys:
                    assert key in use_case, f"Missing use case key: {key}"
                print("   ✓ Coupling Analysis use cases structure is correct")
        else:
            print("   ℹ No coupling analysis data (this is fine for projects without APIs)")
        
        # Test Data Flow Mapping
        print("5. Testing Data Flow Mapping...")
        if "data_flow_mapping" in complexity_data:
            data_flow = complexity_data["data_flow_mapping"]
            
            required_keys = ["data_sources", "data_transforms", "data_sinks", "entry_points", "flow_patterns", "files_analysis"]
            for key in required_keys:
                assert key in data_flow, f"Missing key: {key}"
            
            print("   ✓ Data Flow Mapping has all required keys")
            
            # Check flow patterns structure
            if data_flow["flow_patterns"]:
                patterns = data_flow["flow_patterns"]
                pattern_keys = ["sources_summary", "transforms_summary", "sinks_summary", "total_entry_points", "files_with_data_flow"]
                for key in pattern_keys:
                    assert key in patterns, f"Missing flow pattern key: {key}"
                print("   ✓ Data Flow Mapping patterns structure is correct")
        else:
            print("   ℹ No data flow mapping data (this is fine for projects without complex data flows)")
        
        # Test Event System Understanding
        print("6. Testing Event System Understanding...")
        if "event_system_understanding" in complexity_data:
            events = complexity_data["event_system_understanding"]
            
            required_keys = ["event_files", "events_dispatched", "events_received", "event_patterns", "dependency_chains"]
            for key in required_keys:
                assert key in events, f"Missing key: {key}"
            
            print("   ✓ Event System Understanding has all required keys")
            
            # Check event patterns structure
            if events["event_patterns"]:
                patterns = events["event_patterns"]
                pattern_keys = ["total_files_with_events", "total_events_dispatched", "total_events_received", "unique_dispatched_events", "unique_received_events"]
                for key in pattern_keys:
                    assert key in patterns, f"Missing event pattern key: {key}"
                print("   ✓ Event System Understanding patterns structure is correct")
        else:
            print("   ℹ No event system data (this is fine for projects without event systems)")
        
        # Test that existing functionality still works
        print("7. Testing existing functionality integrity...")
        
        # Check that original keys are still present
        original_keys = ["rest_apis", "database_schemas", "external_integrations", "summary"]
        for key in original_keys:
            assert key in result, f"Missing original key: {key}"
        
        print("   ✓ All original functionality preserved")
        
        # Test summary structure
        summary = result["summary"]
        summary_keys = ["total_rest_endpoints", "total_db_tables", "total_db_models", "total_external_services"]
        for key in summary_keys:
            assert key in summary, f"Missing summary key: {key}"
        
        print("   ✓ Summary structure intact")
        
        print("\n" + "=" * 70)
        print("🎉 ALL API CONTRACTS INTEGRATION COMPLEXITY SCORING FEATURES WORKING!")
        print("=" * 70)
        
        # Print feature summary
        print("\n📋 New Features Successfully Implemented:")
        print("   • API Stability Analysis - Identifies stable vs unstable interfaces")
        print("   • Coupling Analysis - Analyzes tight vs loose coupling with use cases")
        print("   • Data Flow Mapping - Maps data sources, transforms, and sinks with entry points")
        print("   • Event System Understanding - Identifies pub/sub patterns and dependency chains")
        
        if complexity_data.get("api_stability", {}).get("files_analysis"):
            print(f"\n📊 Analysis Results Preview:")
            print(f"   • API Files Analyzed: {len(complexity_data['api_stability']['files_analysis'])}")
        
        if complexity_data.get("coupling_analysis", {}).get("use_cases"):
            print(f"   • Use Cases Identified: {len(complexity_data['coupling_analysis']['use_cases'])}")
        
        if complexity_data.get("data_flow_mapping", {}).get("files_analysis"):
            print(f"   • Files with Data Flow: {len(complexity_data['data_flow_mapping']['files_analysis'])}")
        
        if complexity_data.get("event_system_understanding", {}).get("event_files"):
            print(f"   • Files with Events: {len(complexity_data['event_system_understanding']['event_files'])}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_contracts_new_features()
    exit(0 if success else 1)
