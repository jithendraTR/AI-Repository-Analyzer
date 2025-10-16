#!/usr/bin/env python3
"""
Demo script to test the Knowledge Risk Assessment feature in Risk Analysis
"""
import sys
from pathlib import Path
sys.path.append('.')

from analyzers.risk_analysis import RiskAnalysisAnalyzer

def main():
    print("=" * 60)
    print("KNOWLEDGE RISK ASSESSMENT FEATURE DEMONSTRATION")
    print("=" * 60)
    
    # Initialize the analyzer
    repo_path = Path('.')
    analyzer = RiskAnalysisAnalyzer(repo_path, None, None)
    
    print("\n1. Verifying Knowledge Risk Assessment Methods:")
    print("-" * 50)
    
    methods = [
        '_analyze_knowledge_risks',
        '_identify_file_spofs', 
        '_identify_technology_silos',
        '_calculate_bus_factor_risks',
        '_identify_critical_files_limited_knowledge',
        '_calculate_file_importance',
        '_calculate_spof_risk_level'
    ]
    
    all_methods_exist = True
    for method in methods:
        if hasattr(analyzer, method):
            print(f"✓ {method}")
        else:
            print(f"✗ {method} - MISSING")
            all_methods_exist = False
    
    if not all_methods_exist:
        print("\n❌ Some methods are missing!")
        return
    
    print("\n2. Running Knowledge Risk Analysis:")
    print("-" * 50)
    
    try:
        # Run the analysis
        results = analyzer.analyze()
        
        if 'knowledge_risks' in results:
            knowledge_risks = results['knowledge_risks']
            
            print("\n📊 KNOWLEDGE RISK ANALYSIS RESULTS:")
            print("=" * 50)
            
            # Summary
            summary = knowledge_risks.get('summary', {})
            print(f"Total Knowledge Risks: {summary.get('total_risks', 0)}")
            print(f"High Risk Files: {summary.get('high_risk_files', 0)}")
            print(f"Contributors at Risk: {summary.get('contributors_at_risk', 0)}")
            
            # Single Point of Failures
            spofs = knowledge_risks.get('single_point_failures', [])
            print(f"\n🔍 Single Points of Failure: {len(spofs)} found")
            if spofs:
                print("\n| File Path | Risk Level | Main Contributors | Risk Description |")
                print("|-----------|------------|------------------|------------------|")
                for spof in spofs[:5]:  # Show first 5
                    file_path = spof.get('file', 'Unknown')
                    risk_level = spof.get('risk_level', 'Unknown')
                    contributors = ', '.join(spof.get('contributors', [])[:2])  # First 2 contributors
                    if len(spof.get('contributors', [])) > 2:
                        contributors += f" (+{len(spof.get('contributors', [])) - 2} more)"
                    risk_desc = spof.get('risk_description', 'No description')[:50] + "..."
                    print(f"| `{file_path}` | {risk_level} | {contributors} | {risk_desc} |")
                
                if len(spofs) > 5:
                    print(f"| ... | ... | ... | ({len(spofs) - 5} more risks) |")
            
            # Knowledge Silos
            silos = knowledge_risks.get('knowledge_silos', [])
            print(f"\n🏗️ Technology/Knowledge Silos: {len(silos)} found")
            if silos:
                for i, silo in enumerate(silos[:3], 1):  # Show first 3
                    tech = silo.get('technology', 'Unknown')
                    experts = ', '.join(silo.get('experts', [])[:2])
                    if len(silo.get('experts', [])) > 2:
                        experts += f" (+{len(silo.get('experts', [])) - 2} more)"
                    print(f"   {i}. {tech} - Experts: {experts}")
            
            # Bus Factor Risks
            bus_risks = knowledge_risks.get('bus_factor_risks', [])
            print(f"\n🚌 Bus Factor Risks: {len(bus_risks)} found")
            if bus_risks:
                for i, risk in enumerate(bus_risks[:3], 1):  # Show first 3
                    area = risk.get('area', 'Unknown')
                    factor = risk.get('bus_factor', 0)
                    print(f"   {i}. {area} - Bus Factor: {factor}")
            
            # Critical Files with Limited Knowledge
            critical_files = knowledge_risks.get('critical_files_with_few_contributors', [])
            print(f"\n⚠️ Critical Files with Few Contributors: {len(critical_files)} found")
            if critical_files:
                print("\n| File Path | Contributors | Importance Score | Risk Level |")
                print("|-----------|--------------|------------------|------------|")
                for file_risk in critical_files[:5]:  # Show first 5
                    file_path = file_risk.get('file', 'Unknown')
                    contributor_count = len(file_risk.get('contributors', []))
                    importance = file_risk.get('importance_score', 0)
                    risk_level = file_risk.get('risk_level', 'Unknown')
                    print(f"| `{file_path}` | {contributor_count} | {importance:.2f} | {risk_level} |")
                
                if len(critical_files) > 5:
                    print(f"| ... | ... | ... | ({len(critical_files) - 5} more files) |")
            
            print(f"\n✅ Knowledge Risk Assessment feature is working successfully!")
            print(f"📁 Results are displayed in the Risk Analysis tab of the main application.")
            
        else:
            print("❌ Knowledge risk analysis not found in results")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
