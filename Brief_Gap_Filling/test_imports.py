#!/usr/bin/env python3
"""
Quick script to test if all imports work correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        print("1. Testing test_config imports...")
        from Brief_Gap_Filling.test_config import (
            BALLANTINE_POLAND_BRIEF,
            STANDARD_DIMENSIONS,
            DEFAULT_BRANDWORLD_PATH
        )
        print(f"   ✅ Brief length: {len(BALLANTINE_POLAND_BRIEF)}")
        print(f"   ✅ Dimensions: {len(STANDARD_DIMENSIONS)}")
        print(f"   ✅ Brandworld path: {DEFAULT_BRANDWORLD_PATH}")
        
        print("2. Testing gap filling utils...")
        from Brief_Gap_Filling.utils import gap_fill_with_evaluation
        print("   ✅ gap_fill_with_evaluation imported")
        
        print("3. Testing deepseek_chat import...")
        # Import deepseek_chat from root utils (not Brief_Gap_Filling utils)
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils import deepseek_chat
        print("   ✅ deepseek_chat imported from root utils")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_file_existence():
    """Test if required files exist"""
    print("\n📁 Testing file existence...")
    
    try:
        from Brief_Gap_Filling.test_config import DEFAULT_BRANDWORLD_PATH
        
        if os.path.exists(DEFAULT_BRANDWORLD_PATH):
            print(f"   ✅ Brandworld file exists: {DEFAULT_BRANDWORLD_PATH}")
            return True
        else:
            print(f"   ❌ Brandworld file missing: {DEFAULT_BRANDWORLD_PATH}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking files: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 Import and File Test")
    print("="*40)
    
    imports_ok = test_imports()
    files_ok = test_file_existence()
    
    print("\n" + "="*40)
    print("RESULTS:")
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Files: {'✅ PASS' if files_ok else '❌ FAIL'}")
    
    if imports_ok and files_ok:
        print("\n🎉 Ready to run tests!")
        print("💡 Run: python Brief_Gap_Filling/simple_test.py")
    else:
        print("\n⚠️ Please fix the issues above before running tests.")
    
    return imports_ok and files_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 