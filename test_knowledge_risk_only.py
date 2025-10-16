#!/usr/bin/env python3
"""
Direct test for Knowledge Risk Assessment functionality only
"""
import sys
from pathlib import Path
sys.path.append('.')

def test_knowledge_risk_assessment_directly():
    """Test Knowledge Risk Assessment without AI dependencies"""
    
    print("=" * 70)
    print("DIRECT KNOWLEDGE RISK ASSESSMENT TEST")
    print("=" * 70)
    
    try:
        from analyzers.risk_analysis import RiskAnalysisAnalyzer
        from analyzers.expertise_mapping import ExpertiseMapper
        
        # Initialize analyzer
        repo_path = Path('.')
        analyzer = RiskAnalysisAnalyzer(repo_path, None, None)
        
        print("\n✓ Successfully imported RiskAnalysisAnalyzer")
        
        # Test if all knowledge risk methods exist
        knowledge_methods = [
            '_analyze_knowledge_risks',
            '_identify_file_spofs', 
            '_identify_technology_silos',
            '_calculate_bus_factor_risks',
            '_identify_critical_files_limited_knowledge',
            '_calculate_file_importance',
            '_calculate_spof_risk_level'
        ]
        
        print("\n1. Checking Knowledge Risk Methods:")
        print("-" * 50)
        
        all_methods_exist = True
        for method in knowledge_methods:
            if hasattr(analyzer, method):
                print(f"✓ {method}")
            else:
                print(f"✗ {method} - MISSING")
                all_methods_exist = False
        
        if not all_methods_exist:
            return False
        
        print("\n2. Testing Individual Methods:")
        print("-" * 50)
        
        # Test file importance calculation
        try:
            importance = analyzer._calculate_file_importance("analyzers/risk_analysis.py", 25)
            print(f"✓ File importance calculation: {importance:.2f}")
        except Exception as e:
            print(f"✗ File importance calculation failed: {e}")
            return False
        
        # Test risk level calculation
        try:
            risk_level = analyzer._calculate_spof_risk_level(40.0, 30)
            print(f"✓ SPOF risk level calculation: {risk_level}")
        except Exception as e:
            print(f"✗ SPOF risk level calculation failed: {e}")
            return False
        
        print("\n3. Testing Knowledge Risk Analysis:")
        print("-" * 50)
        
        # Test the main knowledge risk analysis
        try:
            knowledge_risks = analyzer._analyze_knowledge_risks()
            
            if isinstance(knowledge_risks, dict):
                print("✓ Knowledge risk analysis executed successfully")
                
                # Check structure
                expected_keys = [
                    'single_point_failures',
                    'knowledge_silos',
                    'bus_factor_risks', 
                    'critical_files_with_few_contributors',
                    'summary'
                ]
                
                structure_ok = True
                for key in expected_keys:
                    if key in knowledge_risks:
                        count = len(knowledge_risks[key]) if isinstance(knowledge_risks[key], list) else "dict"
                        print(f"  ✓ {key}: {count}")
                    else:
                        print(f"  ✗ {key}: MISSING")
                        structure_ok = False
                
                if structure_ok:
                    print("\n✓ Knowledge risk structure is valid")
                    
                    # Show summary
                    summary = knowledge_risks.get('summary', {})
                    print(f"\n4. Knowledge Risk Summary:")
                    print("-" * 50)
                    print(f"Total Risks: {summary.get('total_risks', 0)}")
                    print(f"High Risk Files: {summary.get('high_risk_files', 0)}")
                    print(f"Contributors at Risk: {summary.get('contributors_at_risk', 0)}")
                    
                    # Show some example results
                    spofs = knowledge_risks.get('single_point_failures', [])
                    if spofs:
                        print(f"\n5. Example Single Points of Failure ({len(spofs)} total):")
                        print("-" * 50)
                        for i, spof in enumerate(spofs[:3], 1):
                            print(f"{i}. File: {spof.get('file', 'Unknown')}")
                            print(f"   Primary Contributor: {spof.get('primary_contributor', 'Unknown')}")
                            print(f"   Commits: {spof.get('commits', 0)}")
                            print(f"   Risk Level: {spof.get('risk_level', 'Unknown')}")
                            print(f"   Risk: {spof.get('explanation', 'No explanation')[:100]}...")
                            print()
                    
                    silos = knowledge_risks.get('knowledge_silos', [])
                    if silos:
                        print(f"6. Example Knowledge Silos ({len(silos)} total):")
                        print("-" * 50)
                        for i, silo in enumerate(silos[:2], 1):
                            print(f"{i}. Technology: {silo.get('technology', 'Unknown')}")
                            print(f"   Primary Expert: {silo.get('primary_contributor', 'Unknown')}")
                            print(f"   Commits: {silo.get('commits', silo.get('primary_commits', 0))}")
                            print(f"   Risk Level: {silo.get('risk_level', 'Unknown')}")
                            print()
                    
                    critical_files = knowledge_risks.get('critical_files_with_few_contributors', [])
                    if critical_files:
                        print(f"7. Example Critical Files with Limited Knowledge ({len(critical_files)} total):")
                        print("-" * 50)
                        for i, cf in enumerate(critical_files[:2], 1):
                            print(f"{i}. File: {cf.get('file', 'Unknown')}")
                            print(f"   Contributors: {len(cf.get('contributors', []))}")
                            print(f"   Total Commits: {cf.get('total_commits', 0)}")
                            print(f"   Risk Level: {cf.get('risk_level', 'Unknown')}")
                            print()
                    
                    return True
                else:
                    print("✗ Knowledge risk structure is invalid")
                    return False
            else:
                print(f"✗ Knowledge risk analysis returned wrong type: {type(knowledge_risks)}")
                return False
                
        except Exception as e:
            print(f"✗ Knowledge risk analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    except ImportError as e:
        print(f"✗ Failed to import required modules: {e}")
        return False
    except Exception as e:
        print(f"✗ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_in_full_analyzer():
    """Test if knowledge risks are integrated in the full analyzer"""
    
    print("\n" + "=" * 70)
    print("INTEGRATION TEST")
    print("=" * 70)
    
    try:
        from analyzers.risk_analysis import RiskAnalysisAnalyzer
        
        # Initialize analyzer 
        repo_path = Path('.')
        analyzer = RiskAnalysisAnalyzer(repo_path, None, None)
        
        print("\n8. Testing Integration with Full Analysis:")
        print("-" * 50)
        
        # Check if analyze method calls knowledge risk analysis
        try:
            # Run full analysis but handle potential AI errors
            results = analyzer.analyze()
            
            # Should have knowledge_risks key even if other parts fail
            if 'knowledge_risks' in results:
                print("✓ Knowledge risks included in full analysis results")
                
                knowledge_risks = results['knowledge_risks']
                if isinstance(knowledge_risks, dict):
                    print("✓ Knowledge risks data structure is valid")
                    
                    # Check if it's integrated into risk summary
                    risk_summary = results.get('risk_summary', {})
                    if 'knowledge_risk_score' in risk_summary:
                        score = risk_summary['knowledge_risk_score']
                        print(f"✓ Knowledge risk score integrated: {score}")
                        return True
                    else:
                        print("✗ Knowledge risk score missing from summary")
                        return False
                else:
                    print("✗ Knowledge risks data is invalid")
                    return False
            else:
                print("✗ Knowledge risks missing from full analysis")
                print(f"Available keys: {list(results.keys())}")
                return False
                
        except Exception as e:
            print(f"✗ Integration test failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Integration test setup failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Knowledge Risk Assessment Feature...")
    print("This test focuses specifically on the Knowledge Risk functionality")
    print("and bypasses external API dependencies.")
    
    success1 = test_knowledge_risk_assessment_directly()
    success2 = test_integration_in_full_analyzer()
    
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    
    if success1 and success2:
        print("🎉 SUCCESS! Knowledge Risk Assessment is fully implemented and working!")
        print("\n📋 FEATURE SUMMARY:")
        print("✓ All required methods implemented")  
        print("✓ Knowledge risk analysis executes successfully")
        print("✓ Proper data structure returned")
        print("✓ Integration with full risk analysis working")
        print("✓ Risk scoring includes knowledge factors")
        print("\n📂 Feature Location: analyzers/risk_analysis.py")
        print("🎯 UI Section: Risk Analysis tab → Knowledge Risk Assessment")
        
        print("\n🔍 RISK TYPES DETECTED:")
        print("• Single Points of Failure (SPOFs)")
        print("• Technology Knowledge Silos") 
        print("• Bus Factor Risks")
        print("• Critical Files with Limited Knowledge")
        
        if success1:
            print("\n✨ The Knowledge Risk Assessment feature is ready to use!")
    else:
        if success1:
            print("⚠️  Knowledge Risk Assessment works in isolation but has integration issues")
        else:
            print("❌ Knowledge Risk Assessment has fundamental issues")
        
        print("\nCheck the error messages above for specific issues to fix.")
