#!/usr/bin/env python3
"""
Test script for Brief_Dimension_Generation
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

def test_brief_dimension_generation():
    """Test the Brief_Dimension_Generation main function with ballantine_poland"""
    
    try:
        # Import the main function and utilities
        from Brief_Dimension_Generation.main import main, list_available_briefs, AVAILABLE_BRIEFS
        
        print("=== Brief Dimension Generation Test ===")
        
        # List available briefs
        print("\n1. Checking available briefs...")
        list_available_briefs()
        
        # Test with ballantine_poland brief
        brief_to_test = "ballantine_poland"
        print(f"\n2. Testing with: {brief_to_test}")
        
        if brief_to_test not in AVAILABLE_BRIEFS:
            print(f"❌ Brief '{brief_to_test}' not found!")
            print("Available briefs:")
            for brief_name in AVAILABLE_BRIEFS.keys():
                print(f"  - {brief_name}")
            return False
        
        # Run the analysis with single brief
        print(f"\n3. Running dimension extraction on [{brief_to_test}]...")
        results = main([brief_to_test])  # Pass as list since main expects a list
        
        if results and results.get('metadata'):
            print("✅ Analysis completed successfully!")
            print(f"📊 Processed {results['metadata']['total_briefs_processed']} brief(s)")
            print(f"📈 Found {results['summary']['total_unique_dimensions']} unique dimensions")
            print(f"📋 Average dimensions per brief: {results['summary']['average_dimensions_per_brief']:.1f}")
            
            # Show extracted dimensions for the brief
            if brief_to_test in results['briefs']:
                brief_data = results['briefs'][brief_to_test]
                print(f"\n📝 Dimensions extracted from {brief_to_test}:")
                for i, dimension in enumerate(brief_data['dimensions'][:10], 1):  # Show first 10
                    print(f"  {i}. {dimension}")
                if len(brief_data['dimensions']) > 10:
                    print(f"  ... and {len(brief_data['dimensions']) - 10} more")
            
            return True
        else:
            print("❌ Analysis failed or returned empty results!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are available.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_briefs():
    """Test with multiple briefs including ballantine_poland"""
    
    try:
        from Brief_Dimension_Generation.main import main
        
        print("\n=== Multiple Briefs Test ===")
        
        # Test with multiple briefs
        test_briefs = ["ballantine_poland", "abs_china", "codigo"]
        print(f"Testing with multiple briefs: {test_briefs}")
        
        results = main(test_briefs)
        
        if results and results.get('metadata'):
            print("✅ Multiple briefs analysis completed!")
            print(f"📊 Processed {results['metadata']['total_briefs_processed']} briefs")
            print(f"📈 Total unique dimensions: {results['summary']['total_unique_dimensions']}")
            
            # Show most common dimensions
            if results['summary']['most_common_dimensions']:
                print(f"\n🔥 Top 5 most common dimensions:")
                for i, (dim, freq) in enumerate(results['summary']['most_common_dimensions'][:5], 1):
                    print(f"  {i}. {dim} (appears in {freq}/{len(test_briefs)} briefs)")
            
            return True
        else:
            print("❌ Multiple briefs analysis failed!")
            return False
            
    except Exception as e:
        print(f"❌ Multiple briefs test error: {e}")
        return False

def test_imports():
    """Test if required modules can be imported"""
    
    print("\n=== Import Test ===")
    
    try:
        from utils import deepseek_chat
        print("✅ deepseek_chat imported successfully")
    except ImportError as e:
        print(f"❌ deepseek_chat import failed: {e}")
        return False
    
    try:
        from prompts import dimension_extraction_prompt
        print("✅ dimension_extraction_prompt imported successfully")
    except ImportError as e:
        print(f"❌ prompts import failed: {e}")
        return False
    
    try:
        from Brief_Dimension_Generation.briefs import ballantine_poland
        print("✅ briefs module imported successfully")
        print(f"📄 ballantine_poland brief length: {len(ballantine_poland)} characters")
    except ImportError as e:
        print(f"❌ briefs import failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Running Brief Dimension Generation tests...\n")
    
    # Test imports first
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n💥 Import tests failed! Please fix dependencies.")
        sys.exit(1)
    
    # Test single brief
    single_ok = test_brief_dimension_generation()
    
    # Test multiple briefs
    multiple_ok = test_multiple_briefs()
    
    if single_ok and multiple_ok:
        print("\n🎉 All tests completed successfully!")
        print("The Brief_Dimension_Generation system is working correctly.")
    else:
        print("\n💥 Some tests failed!")
    
    sys.exit(0 if (single_ok and multiple_ok) else 1) 