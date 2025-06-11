#!/usr/bin/env python3
"""
Simple test script for Enhanced Gap Filling with Ballantine Poland.
No Brand_World dependencies, just loads pre-configured data and runs the test.
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Run the enhanced gap filling test"""
    print("🚀 Enhanced Gap Filling - Simple Test")
    print("="*50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Import all required components
        from Brief_Gap_Filling.test_config import (
            BALLANTINE_POLAND_BRIEF,
            STANDARD_DIMENSIONS,
            DEFAULT_BRANDWORLD_PATH
        )
        from Brief_Gap_Filling.utils import gap_fill_with_evaluation
        
        # Import deepseek_chat from root utils (not Brief_Gap_Filling utils)
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils import deepseek_chat
        
        print("✅ All imports successful")
        print(f"📋 Brief length: {len(BALLANTINE_POLAND_BRIEF)} characters")
        print(f"📊 Dimensions: {len(STANDARD_DIMENSIONS)}")
        print(f"🎯 Brandworld file: {DEFAULT_BRANDWORLD_PATH}")
        
        # Check brandworld file exists
        if not os.path.exists(DEFAULT_BRANDWORLD_PATH):
            print(f"❌ Brandworld file not found: {DEFAULT_BRANDWORLD_PATH}")
            return False
        
        print("✅ Brandworld file exists")
        
        # Run the test with 3 versions for speed
        print("\n🔄 Running enhanced gap filling (3 versions)...")
        start_time = datetime.now()
        
        result = gap_fill_with_evaluation(
            brief_text=BALLANTINE_POLAND_BRIEF,
            dimension_list=STANDARD_DIMENSIONS,
            brandworld_analysis_path=DEFAULT_BRANDWORLD_PATH,
            deepseek_chat_func=deepseek_chat,
            n_versions=3,
            brief_name="ballantine_poland_simple_test"
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Display results
        print(f"\n🎉 Test completed successfully!")
        print(f"⏱️ Duration: {duration:.1f} seconds")
        print(f"🏆 Best score: {result['evaluation_summary']['best_score']:.2f}/10.0")
        print(f"📊 Average score: {result['evaluation_summary']['average_score']:.2f}/10.0")
        print(f"💾 Files saved: {len(result['saved_files'])}")
        
        print("\n📁 Output files:")
        for i, filepath in enumerate(result['saved_files'], 1):
            filename = os.path.basename(filepath)
            print(f"  {i}. {filename}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        print("\nFull error details:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Simple test completed successfully!")
        print("💡 For detailed analysis, run: python Brief_Gap_Filling/test_ballantine_enhanced.py")
    else:
        print("\n❌ Simple test failed!")
    
    print("="*50) 