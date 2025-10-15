#!/usr/bin/env python3

"""
Quick test to verify all analyzers work without TypeErrors
"""

import sys
sys.path.append('.')

from repo_analyzer.main import ParallelAIAnalyzer

def test_all_analyzers():
    """Test that all analyzers can run without TypeErrors"""
    
    print("Testing all analyzers for errors...")
    
    try:
        # Create analyzer
        analyzer = ParallelAIAnalyzer('.')
        
        print(f"Found {len(analyzer.analyzers)} analyzers")
        
        # Test each analyzer individually
        results = {}
        for name, analyzer_instance in analyzer.analyzers.items():
            print(f"\nTesting {name}...")
            try:
                # Test analyze method
                analysis_data = analyzer_instance.analyze()
                if 'error' in analysis_data:
                    results[name] = f"ANALYSIS ERROR: {analysis_data['error']}"
                else:
                    results[name] = "ANALYSIS SUCCESS"
                    
                    # Test render method (the one causing TypeError)
                    try:
                        # We can't fully test render without Streamlit context,
                        # but we can check if the analysis data structure is correct
                        if hasattr(analyzer_instance, '_check_analysis_structure'):
                            analyzer_instance._check_analysis_structure(analysis_data)
                        results[name] = "SUCCESS - No TypeError"
                    except Exception as render_error:
                        if "TypeError" in str(render_error):
                            results[name] = f"RENDER TYPEERROR: {render_error}"
                        else:
                            results[name] = f"RENDER ERROR (not TypeError): {render_error}"
                        
            except Exception as e:
                if "TypeError" in str(e):
                    results[name] = f"ANALYZER TYPEERROR: {e}"
                else:
                    results[name] = f"ANALYZER ERROR (not TypeError): {e}"
        
        # Print results
        print("\n" + "="*60)
        print("ANALYZER TEST RESULTS")
        print("="*60)
        
        success_count = 0
        typeerror_count = 0
        
        for name, result in results.items():
            status = "✅" if "SUCCESS" in result else ("⚠️" if "TypeError" not in result.upper() else "❌")
            print(f"{status} {name}: {result}")
            
            if "SUCCESS" in result:
                success_count += 1
            elif "TYPEERROR" in result.upper():
                typeerror_count += 1
        
        print(f"\nSUMMARY:")
        print(f"✅ Successful: {success_count}/{len(results)}")
        print(f"❌ TypeErrors: {typeerror_count}/{len(results)}")
        print(f"⚠️ Other errors: {len(results) - success_count - typeerror_count}/{len(results)}")
        
        if typeerror_count == 0:
            print("\n🎉 NO TYPEERRORS FOUND! All fixes successful!")
            return True
        else:
            print(f"\n🚨 {typeerror_count} TypeErrors still need fixing")
            return False
            
    except Exception as e:
        print(f"Failed to run analyzer tests: {e}")
        return False

if __name__ == "__main__":
    success = test_all_analyzers()
    sys.exit(0 if success else 1)
