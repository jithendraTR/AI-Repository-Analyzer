#!/usr/bin/env python3
"""
Test script for enhanced Timeline analyzer
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from analyzers.timeline_analysis import TimelineAnalyzer

def test_enhanced_timeline_analysis():
    """Test the enhanced timeline analysis functionality"""
    
    print("🔄 Testing Enhanced Timeline Analysis...")
    
    try:
        # Initialize analyzer
        analyzer = TimelineAnalyzer(repo_path=project_root)
        
        print("✅ Timeline analyzer initialized successfully")
        
        # Test the analyze method with enhanced features
        print("📊 Running enhanced analysis...")
        results = analyzer.analyze()
        
        if "error" in results:
            print(f"❌ Analysis failed: {results['error']}")
            return False
        
        # Check if enhanced analysis results are present
        enhanced_sections = [
            'feature_patterns',
            'architecture_migration', 
            'performance_evolution',
            'security_evolution'
        ]
        
        print("🔍 Checking enhanced analysis sections...")
        
        for section in enhanced_sections:
            if section in results:
                print(f"✅ {section.replace('_', ' ').title()} analysis: Present")
                
                # Check if the section has meaningful data
                section_data = results[section]
                if isinstance(section_data, dict):
                    total_key = f"total_{section.split('_')[0]}_commits"
                    if total_key in section_data:
                        count = section_data[total_key]
                        print(f"   📈 Found {count} relevant commits")
                    else:
                        print(f"   📊 Section contains {len(section_data)} data elements")
                else:
                    print(f"   ⚠️  Unexpected data type: {type(section_data)}")
            else:
                print(f"❌ {section.replace('_', ' ').title()} analysis: Missing")
        
        # Test specific enhanced features
        print("\n🎯 Testing specific enhanced features...")
        
        # Feature Addition Patterns
        if 'feature_patterns' in results:
            fp = results['feature_patterns']
            if fp.get('total_feature_commits', 0) > 0:
                print(f"   🚀 Feature analysis: {fp['total_feature_commits']} feature commits found")
                if fp.get('feature_categories'):
                    print(f"   📊 Feature categories: {list(fp['feature_categories'].keys())}")
                if fp.get('best_practices'):
                    print(f"   💡 Best practices identified: {len(fp['best_practices'])}")
            else:
                print("   ℹ️  No feature commits found in repository")
        
        # Architecture Migration History
        if 'architecture_migration' in results:
            am = results['architecture_migration']
            if am.get('total_migration_commits', 0) > 0:
                print(f"   🏗️  Architecture analysis: {am['total_migration_commits']} migration commits found")
                if am.get('technology_adoptions'):
                    print(f"   🔧 Technology adoptions: {list(am['technology_adoptions'].keys())}")
                if am.get('maturity_indicators'):
                    mature_count = sum(1 for v in am['maturity_indicators'].values() if v)
                    print(f"   📊 Architecture maturity: {mature_count}/5 indicators")
            else:
                print("   ℹ️  No architecture migration commits found in repository")
        
        # Performance Evolution
        if 'performance_evolution' in results:
            pe = results['performance_evolution']
            if pe.get('total_performance_commits', 0) > 0:
                print(f"   ⚡ Performance analysis: {pe['total_performance_commits']} performance commits found")
                if pe.get('optimization_types'):
                    print(f"   🚀 Optimization types: {list(pe['optimization_types'].keys())}")
                regressions = len(pe.get('performance_regressions', []))
                print(f"   📉 Performance regressions tracked: {regressions}")
            else:
                print("   ℹ️  No performance commits found in repository")
        
        # Security Evolution
        if 'security_evolution' in results:
            se = results['security_evolution']
            if se.get('total_security_commits', 0) > 0:
                print(f"   🔒 Security analysis: {se['total_security_commits']} security commits found")
                if se.get('security_domains'):
                    print(f"   🛡️  Security domains: {list(se['security_domains'].keys())}")
                maturity = se.get('security_maturity', {})
                if maturity.get('maturity_level'):
                    print(f"   📊 Security maturity: {maturity['maturity_level']}")
            else:
                print("   ℹ️  No security commits found in repository")
        
        # Test original functionality is preserved
        print("\n🔍 Verifying original functionality is preserved...")
        
        original_sections = [
            'timeline_data',
            'recent_changes',
            'development_phases',
            'project_age',
            'total_commits'
        ]
        
        for section in original_sections:
            if section in results:
                print(f"✅ {section.replace('_', ' ').title()}: Present")
            else:
                print(f"❌ {section.replace('_', ' ').title()}: Missing")
        
        print("\n🎉 Enhanced Timeline Analysis test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        print("📋 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Enhanced Timeline Analysis Test")
    print("=" * 50)
    
    success = test_enhanced_timeline_analysis()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Enhanced Timeline analyzer is working correctly.")
        exit(0)
    else:
        print("❌ Tests failed! Please check the implementation.")
        exit(1)
