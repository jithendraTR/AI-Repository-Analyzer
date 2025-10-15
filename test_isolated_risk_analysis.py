#!/usr/bin/env python3
"""
Isolated test for Risk Analysis with Knowledge Risk Assessment
"""
import sys
from pathlib import Path
sys.path.append('.')

def test_isolated_risk_analysis():
    """Test the Risk Analysis analyzer in isolation"""
    
    print("=" * 60)
    print("ISOLATED RISK ANALYSIS TEST - KNOWLEDGE RISK ASSESSMENT")
    print("=" * 60)
    
    try:
        from analyzers.risk_analysis import RiskAnalysisAnalyzer
        
        # Initialize analyzer
        repo_path = Path('.')
        analyzer = RiskAnalysisAnalyzer(repo_path, None, None)
        
        print("\n1. Testing Knowledge Risk Assessment Methods:")
        print("-" * 50)
        
        # Check all required methods
        required_methods = [
            '_analyze_knowledge_risks',
            '_identify_file_spofs', 
            '_identify_technology_silos',
            '_calculate_bus_factor_risks',
            '_identify_critical_files_limited_knowledge',
            '_calculate_file_importance',
            '_calculate_spof_risk_level'
        ]
        
        all_methods_exist = True
        for method in required_methods:
            if hasattr(analyzer, method):
                print(f"✓ {method}")
            else:
                print(f"✗ {method} - MISSING")
                all_methods_exist = False
        
        if not all_methods_exist:
            print("\n❌ Some required methods are missing!")
            return False
        
        print("\n2. Testing Knowledge Risk Analysis Execution:")
        print("-" * 50)
        
        # Test just the knowledge risk analysis method
        try:
            knowledge_risks = analyzer._analyze_knowledge_risks()
            
            if isinstance(knowledge_risks, dict):
                print("✅ Knowledge risk analysis method executed successfully!")
                
                # Check structure
                expected_keys = [
                    'single_point_failures',
                    'knowledge_silos', 
                    'bus_factor_risks',
                    'critical_files_with_few_contributors',
                    'summary'
                ]
                
                print("\n3. Verifying Knowledge Risk Structure:")
                print("-" * 50)
                
                structure_valid = True
                for key in expected_keys:
                    if key in knowledge_risks:
                        print(f"✓ {key}: {type(knowledge_risks[key])}")
                    else:
                        print(f"✗ {key} - MISSING")
                        structure_valid = False
                
                if structure_valid:
                    print("\n✅ Knowledge risk structure is valid!")
                    
                    # Show results summary
                    print("\n4. Knowledge Risk Analysis Results:")
                    print("-" * 50)
                    
                    summary = knowledge_risks.get('summary', {})
                    print(f"Total Risks: {summary.get('total_risks', 0)}")
                    print(f"High Risk Files: {summary.get('high_risk_files', 0)}")
                    print(f"Contributors at Risk: {summary.get('contributors_at_risk', 0)}")
                    
                    # Show details for each risk type
                    risk_types = [
                        ('Single Point Failures', 'single_point_failures'),
                        ('Knowledge Silos', 'knowledge_silos'),
                        ('Bus Factor Risks', 'bus_factor_risks'),
                        ('Critical Files with Few Contributors', 'critical_files_with_few_contributors')
                    ]
                    
                    for risk_name, risk_key in risk_types:
                        risks = knowledge_risks.get(risk_key, [])
                        print(f"\n{risk_name}: {len(risks)} found")
                        
                        if risks:
                            for i, risk in enumerate(risks[:2], 1):  # Show first 2
                                print(f"  {i}. {risk}")
                    
                    return True
                else:
                    print("❌ Knowledge risk structure is invalid!")
                    return False
            else:
                print("❌ Knowledge risk analysis returned invalid data type")
                return False
                
        except Exception as e:
            print(f"❌ Knowledge risk analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    except Exception as e:
        print(f"❌ Failed to import or initialize Risk Analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_risk_analysis():
    """Test the full risk analysis including knowledge risks"""
    
    print("\n" + "=" * 60)
    print("FULL RISK ANALYSIS TEST")
    print("=" * 60)
    
    try:
        from analyzers.risk_analysis import RiskAnalysisAnalyzer
        
        # Initialize analyzer
        repo_path = Path('.')
        analyzer = RiskAnalysisAnalyzer(repo_path, None, None)
        
        print("\n5. Testing Full Analysis with Knowledge Risks:")
        print("-" * 50)
        
        # Run full analysis
        results = analyzer.analyze()
        
        if "error" in results:
            print(f"❌ Analysis failed: {results['error']}")
            return False
        
        # Check if knowledge_risks is in results
        if 'knowledge_risks' in results:
            print("✅ Knowledge risks included in full analysis!")
            
            knowledge_risks = results['knowledge_risks']
            
            print(f"Knowledge Risk Summary:")
            summary = knowledge_risks.get('summary', {})
            print(f"  - Total Risks: {summary.get('total_risks', 0)}")
            print(f"  - High Risk Files: {summary.get('high_risk_files', 0)}")
            print(f"  - Contributors at Risk: {summary.get('contributors_at_risk', 0)}")
            
            # Check risk_summary includes knowledge risk score
            risk_summary = results.get('risk_summary', {})
            if 'knowledge_risk_score' in risk_summary:
                print(f"  - Knowledge Risk Score: {risk_summary['knowledge_risk_score']}")
                print("✅ Knowledge risks properly integrated into risk summary!")
            else:
                print("❌ Knowledge risk score missing from risk summary")
                return False
            
            return True
        else:
            print("❌ Knowledge risks missing from full analysis results")
            print(f"Available keys: {list(results.keys())}")
            return False
            
    except Exception as e:
        print(f"❌ Full analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_isolated_risk_analysis()
    success2 = test_full_risk_analysis()
    
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    
    if success1 and success2:
        print("✅ ALL TESTS PASSED - Knowledge Risk Assessment is working!")
        print("\nThe Knowledge Risk Assessment feature is properly implemented and functional.")
        print("If you're having issues in the main application, the problem is likely")
        print("with a different analyzer (like singular_product_vision.py).")
    else:
        print("❌ SOME TESTS FAILED - There are issues with the Knowledge Risk Assessment")
        
    print("\nTo view results in the main application:")
    print("1. Run: streamlit run repo_analyzer/main.py")
    print("2. Navigate to the 'Risk Analysis' tab")
    print("3. Look for the 'Knowledge Risk Assessment' section")
