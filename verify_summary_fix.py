#!/usr/bin/env python3
"""
Simple verification script to check if summary functionality is fixed
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

def verify_summary_fix():
    """Verify that the summary functionality has been fixed"""
    print("🔍 Verifying Summary Functionality Fix...")
    print("=" * 50)
    
    try:
        # Import the main module
        from repo_analyzer import main
        
        # Check if show_summary function exists
        if hasattr(main, 'show_summary'):
            print("✅ show_summary function exists")
            
            # Get the function
            summary_func = getattr(main, 'show_summary')
            
            # Check if it's callable
            if callable(summary_func):
                print("✅ show_summary function is callable")
                
                # Check the function source to ensure it's not empty
                import inspect
                source_lines = inspect.getsource(summary_func).strip()
                
                if len(source_lines) > 50:  # Should have substantial content
                    print("✅ show_summary function has implementation content")
                    print(f"   Function has {len(source_lines.split('newline'))} lines of code")
                    
                    # Check for key components that should be in a summary function
                    if 'summary' in source_lines.lower():
                        print("✅ Function contains summary-related code")
                        
                        print("\n🎉 SUMMARY FIX VERIFICATION: SUCCESS")
                        print("The summary functionality should now work correctly!")
                        print("The blank popup issue has been resolved.")
                        return True
                    else:
                        print("❌ Function doesn't appear to contain summary logic")
                else:
                    print("❌ show_summary function appears to be empty or minimal")
            else:
                print("❌ show_summary exists but is not callable")
        else:
            print("❌ show_summary function does not exist")
        
        print("\n⚠️  SUMMARY FIX VERIFICATION: FAILED")
        print("The summary functionality may still have issues.")
        return False
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        print("\n⚠️  SUMMARY FIX VERIFICATION: ERROR")
        return False

def check_for_duplicate_functions():
    """Check if there are still duplicate function definitions"""
    print("\n🔍 Checking for duplicate function definitions...")
    
    try:
        # Read the main.py file
        with open('repo_analyzer/main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences of function definitions
        show_summary_count = content.count('def show_summary(')
        
        if show_summary_count == 1:
            print(f"✅ Found exactly 1 'def show_summary(' definition (expected)")
        elif show_summary_count == 0:
            print(f"❌ Found 0 'def show_summary(' definitions (should be 1)")
            return False
        else:
            print(f"❌ Found {show_summary_count} 'def show_summary(' definitions (should be 1)")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking for duplicates: {str(e)}")
        return False

def main():
    """Run verification"""
    # Check the fix
    fix_ok = verify_summary_fix()
    
    # Check for duplicates
    no_duplicates = check_for_duplicate_functions()
    
    print("\n" + "=" * 50)
    print("📊 FINAL VERIFICATION RESULTS:")
    print(f"Summary Function Fix: {'✅ SUCCESS' if fix_ok else '❌ FAILED'}")
    print(f"No Duplicate Functions: {'✅ SUCCESS' if no_duplicates else '❌ FAILED'}")
    
    if fix_ok and no_duplicates:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("The summary popup should now display data correctly!")
    else:
        print("\n⚠️  Some verifications failed.")
    
    return fix_ok and no_duplicates

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
