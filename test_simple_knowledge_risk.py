#!/usr/bin/env python3
"""
Simple test to verify Knowledge Risk Assessment feature
"""
import sys
from pathlib import Path
sys.path.append('.')

# Test if the feature is properly integrated
def test_knowledge_risk_feature():
    try:
        from analyzers.risk_analysis import RiskAnalysisAnalyzer
        
        # Initialize analyzer
        repo_path = Path('.')
        analyzer = RiskAnalysisAnalyzer(repo_path, None, None)
        
        # Check if methods exist
        methods = [
            '_analyze_knowledge_risks',
            '_identify_file_spofs', 
            '_identify_technology_silos',
            '_calculate_bus_factor_risks',
            '_identify_critical_files_limited_knowledge',
            '_calculate_file_importance',
            '_calculate_spof_risk_level'
        ]
        
        with open('knowledge_risk_test_results.txt', 'w') as f:
            f.write("KNOWLEDGE RISK ASSESSMENT FEATURE TEST\n")
            f.write("="*50 + "\n\n")
            
            f.write("1. Method Verification:\n")
            f.write("-"*30 + "\n")
            
            all_exist = True
            for method in methods:
                if hasattr(analyzer, method):
                    f.write(f"✓ {method}\n")
                else:
                    f.write(f"✗ {method} - MISSING\n")
                    all_exist = False
            
            if all_exist:
                f.write("\n✅ All Knowledge Risk Assessment methods are present!\n")
                
                # Try to run analysis
                f.write("\n2. Running Analysis Test:\n")
                f.write("-"*30 + "\n")
                
                try:
                    results = analyzer.analyze()
                    
                    if 'knowledge_risks' in results:
                        knowledge_risks = results['knowledge_risks']
                        
                        f.write("✅ Knowledge risk analysis executed successfully!\n\n")
                        f.write("Results Summary:\n")
                        f.write(f"- Single Points of Failure: {len(knowledge_risks.get('single_point_failures', []))}\n")
                        f.write(f"- Knowledge Silos: {len(knowledge_risks.get('knowledge_silos', []))}\n")
                        f.write(f"- Bus Factor Risks: {len(knowledge_risks.get('bus_factor_risks', []))}\n")
                        f.write(f"- Critical Files with Few Contributors: {len(knowledge_risks.get('critical_files_with_few_contributors', []))}\n")
                        
                        summary = knowledge_risks.get('summary', {})
                        f.write(f"- Total Risks: {summary.get('total_risks', 0)}\n")
                        f.write(f"- High Risk Files: {summary.get('high_risk_files', 0)}\n")
                        f.write(f"- Contributors at Risk: {summary.get('contributors_at_risk', 0)}\n")
                        
                        # Show some example risks
                        spofs = knowledge_risks.get('single_point_failures', [])
                        if spofs:
                            f.write("\nExample Single Points of Failure:\n")
                            for i, spof in enumerate(spofs[:3], 1):
                                f.write(f"{i}. File: {spof.get('file', 'Unknown')}\n")
                                f.write(f"   Risk Level: {spof.get('risk_level', 'Unknown')}\n")
                                f.write(f"   Contributors: {len(spof.get('contributors', []))}\n")
                                f.write(f"   Description: {spof.get('risk_description', 'No description')}\n\n")
                        
                        # Show critical files
                        critical_files = knowledge_risks.get('critical_files_with_few_contributors', [])
                        if critical_files:
                            f.write("Critical Files with Limited Knowledge:\n")
                            for i, file_risk in enumerate(critical_files[:3], 1):
                                f.write(f"{i}. File: {file_risk.get('file', 'Unknown')}\n")
                                f.write(f"   Contributors: {len(file_risk.get('contributors', []))}\n")
                                f.write(f"   Importance Score: {file_risk.get('importance_score', 0):.2f}\n")
                                f.write(f"   Risk Level: {file_risk.get('risk_level', 'Unknown')}\n\n")
                        
                    else:
                        f.write("❌ Knowledge risks not found in analysis results\n")
                        f.write(f"Available keys: {list(results.keys())}\n")
                        
                except Exception as e:
                    f.write(f"❌ Error during analysis: {str(e)}\n")
                    import traceback
                    f.write(f"Traceback: {traceback.format_exc()}\n")
            else:
                f.write("\n❌ Some methods are missing!\n")
                
        print("Test completed! Results saved to knowledge_risk_test_results.txt")
        
    except Exception as e:
        with open('knowledge_risk_test_results.txt', 'w') as f:
            f.write(f"❌ Test failed: {str(e)}\n")
            import traceback
            f.write(f"Traceback: {traceback.format_exc()}\n")
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_knowledge_risk_feature()
