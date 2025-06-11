#!/usr/bin/env python3
"""
Quick validation script to check that all required components are accessible
for the Enhanced Gap Filling test with Ballantine Poland brief.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_imports():
    """Check if all required imports are working"""
    print("🔍 Checking imports...")
    
    try:
        from Brief_Gap_Filling.test_config import BALLANTINE_POLAND_BRIEF
        print("✅ BALLANTINE_POLAND_BRIEF imported successfully")
        print(f"   Brief length: {len(BALLANTINE_POLAND_BRIEF)} characters")
    except ImportError as e:
        print(f"❌ Failed to import BALLANTINE_POLAND_BRIEF: {e}")
        return False
    
    try:
        from Brief_Gap_Filling.test_config import STANDARD_DIMENSIONS
        print("✅ STANDARD_DIMENSIONS imported successfully")
        print(f"   Number of dimensions: {len(STANDARD_DIMENSIONS)}")
    except ImportError as e:
        print(f"❌ Failed to import STANDARD_DIMENSIONS: {e}")
        return False
    
    try:
        from Brief_Gap_Filling.utils import gap_fill_with_evaluation
        print("✅ gap_fill_with_evaluation imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import gap_fill_with_evaluation: {e}")
        return False
    
    try:
        # Import deepseek_chat from root utils (not Brief_Gap_Filling utils)
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils import deepseek_chat
        print("✅ deepseek_chat imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import deepseek_chat: {e}")
        return False
    
    return True

def check_brandworld_file():
    """Check if brandworld analysis file exists and is valid"""
    print("\n🔍 Checking brandworld analysis file...")
    
    try:
        from Brief_Gap_Filling.test_config import DEFAULT_BRANDWORLD_PATH
        brandworld_path = DEFAULT_BRANDWORLD_PATH
    except ImportError:
        brandworld_path = "files/brandword_distribution/dimensions_ballantine_poland.json"
    
    if not os.path.exists(brandworld_path):
        print(f"❌ Brandworld file not found: {brandworld_path}")
        return False
    
    try:
        with open(brandworld_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Brandworld file loaded successfully: {brandworld_path}")
        print(f"   File size: {os.path.getsize(brandworld_path)} bytes")
        
        # Check file structure
        required_keys = ['metadata', 'briefs', 'all_dimensions']
        for key in required_keys:
            if key in data:
                print(f"   ✅ Contains '{key}' section")
            else:
                print(f"   ⚠️ Missing '{key}' section")
        
        if 'all_dimensions' in data:
            print(f"   Total dimensions in file: {len(data['all_dimensions'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading brandworld file: {e}")
        return False

def check_output_directory():
    """Check if output directory exists"""
    print("\n🔍 Checking output directory...")
    
    output_dir = "Brief_Gap_Filling"
    if os.path.exists(output_dir):
        print(f"✅ Output directory exists: {output_dir}")
        return True
    else:
        print(f"❌ Output directory not found: {output_dir}")
        return False

def show_dimension_preview():
    """Show a preview of the dimensions that will be used"""
    print("\n📋 Dimension Preview:")
    
    try:
        from Brief_Gap_Filling.test_config import STANDARD_DIMENSIONS
        print(f"Will test with {len(STANDARD_DIMENSIONS)} dimensions:")
        for i, dim in enumerate(STANDARD_DIMENSIONS[:5], 1):  # Show first 5
            print(f"   {i}. {dim}")
        if len(STANDARD_DIMENSIONS) > 5:
            print(f"   ... and {len(STANDARD_DIMENSIONS) - 5} more")
    except ImportError:
        print("❌ Could not load STANDARD_DIMENSIONS")

def show_brief_preview():
    """Show a preview of the brief content"""
    print("\n📖 Brief Preview:")
    
    try:
        from Brief_Gap_Filling.test_config import BALLANTINE_POLAND_BRIEF
        brief_lines = BALLANTINE_POLAND_BRIEF.strip().split('\n')[:3]
        print(f"Brief has {len(BALLANTINE_POLAND_BRIEF.strip().split('\\n'))} lines. First 3 lines:")
        for i, line in enumerate(brief_lines, 1):
            preview = line[:60] + "..." if len(line) > 60 else line
            print(f"   {i}. {preview}")
    except ImportError:
        print("❌ Could not load BALLANTINE_POLAND_BRIEF")

def main():
    """Main validation function"""
    print("="*60)
    print("ENHANCED GAP FILLING - VALIDATION CHECK")
    print("="*60)
    
    all_checks_passed = True
    
    # Run all checks
    if not check_imports():
        all_checks_passed = False
    
    if not check_brandworld_file():
        all_checks_passed = False
    
    if not check_output_directory():
        all_checks_passed = False
    
    # Show previews if imports worked
    show_dimension_preview()
    show_brief_preview()
    
    # Final result
    print("\n" + "="*60)
    if all_checks_passed:
        print("🎉 ALL VALIDATION CHECKS PASSED!")
        print("✅ Ready to run the enhanced gap filling test")
        print("💡 Run: python Brief_Gap_Filling/test_ballantine_enhanced.py")
    else:
        print("❌ VALIDATION FAILED!")
        print("⚠️ Please fix the issues above before running the test")
    print("="*60)
    
    return all_checks_passed

if __name__ == "__main__":
    main() 