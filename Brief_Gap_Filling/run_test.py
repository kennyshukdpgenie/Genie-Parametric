#!/usr/bin/env python3
"""
Simple script to run the Enhanced Gap Filling test for Ballantine Poland.
This script first validates the setup and then runs the main test.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Main execution function"""
    print("🚀 Enhanced Gap Filling Test Runner")
    print("="*50)
    
    # Step 1: Run validation
    print("Step 1: Running validation checks...")
    try:
        from Brief_Gap_Filling.validate_test_setup import main as validate_main
        validation_passed = validate_main()
    except Exception as e:
        print(f"❌ Validation script failed: {e}")
        return False
    
    if not validation_passed:
        print("\n❌ Validation failed. Please fix the issues and try again.")
        return False
    
    # Step 2: Run main test
    print("\nStep 2: Running enhanced gap filling test...")
    try:
        from Brief_Gap_Filling.test_ballantine_enhanced import main as test_main
        result = test_main()
        
        print("\n🎉 Test completed successfully!")
        print(f"📊 Best score: {result['evaluation_summary']['best_score']:.2f}/10.0")
        print(f"💾 Files saved: {len(result['saved_files'])}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1) 