#!/usr/bin/env python3
"""
Test script for Brief_Dimension_Generation
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

def test_brief_dimension_generation():
    """Test the Brief_Dimension_Generation main function with actual brief files"""
    
    try:
        # Import the main function and utilities
        from Brief_Dimension_Generation.main import main
        from Brief_Dimension_Generation.document_parser import list_available_briefs, get_available_brief_files
        
        print("=== Brief Dimension Generation Test ===")
        
        # List available briefs
        print("\n1. Checking available briefs...")
        list_available_briefs()
        
        # Get available briefs from files
        available_briefs = get_available_brief_files()
        
        # Test with first available brief
        if not available_briefs:
            print("❌ No brief files found!")
            return False
            
        brief_to_test = list(available_briefs.keys())[0]  # Use first available brief
        print(f"\n2. Testing with: {brief_to_test}")
        
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
    """Test with multiple briefs"""
    
    try:
        from Brief_Dimension_Generation.main import main
        from Brief_Dimension_Generation.document_parser import get_available_brief_files
        
        print("\n=== Multiple Briefs Test ===")
        
        # Get available briefs and test with first 3
        available_briefs = get_available_brief_files()
        test_briefs = list(available_briefs.keys())[:3]  # Test with first 3 available
        
        if len(test_briefs) < 2:
            print("⚠️ Not enough briefs for multiple brief test, skipping...")
            return True
        
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
        from Brief_Dimension_Generation.document_parser import load_brief_content, get_available_brief_files
        available_briefs = get_available_brief_files()
        if available_briefs:
            first_brief_name = list(available_briefs.keys())[0]
            brief_content = load_brief_content(first_brief_name)
            print("✅ document parser imported and working successfully")
            print(f"📄 Sample brief '{first_brief_name}' length: {len(brief_content)} characters")
        else:
            print("⚠️ No brief files found for testing")
    except ImportError as e:
        print(f"❌ document parser import failed: {e}")
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