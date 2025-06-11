#!/usr/bin/env python3
"""
Simple test script for Brand_World PDF processing
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

def test_brand_world():
    """Test the Brand_World main function with Skrewball PDF"""
    
    try:
        # Import the main function
        from Brand_World.main import main, list_available_pdfs
        
        print("=== Brand_World PDF Processing Test ===")
        
        # List available PDFs
        print("\n1. Checking available PDFs...")
        available_pdfs = list_available_pdfs()
        
        if not available_pdfs:
            print("❌ No PDFs found in files/brandword folder!")
            return False
        
        # Test with Skrewball PDF
        pdf_to_test = "Skrewball Brand World.pdf"
        print(f"\n2. Testing with: {pdf_to_test}")
        
        if pdf_to_test not in available_pdfs:
            print(f"❌ PDF '{pdf_to_test}' not found!")
            print("Available PDFs:")
            for pdf in available_pdfs:
                print(f"  - {pdf}")
            return False
        
        # Run the analysis
        print(f"\n3. Running analysis on {pdf_to_test}...")
        results = main(pdf_to_test)
        
        if results:
            print("✅ Analysis completed successfully!")
            print(f"📊 Processed {results['metadata']['total_chunks_processed']} chunks")
            print(f"📈 Found data in {results['summary']['dimensions_with_data']} dimensions")
            return True
        else:
            print("❌ Analysis failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install langchain pdfplumber")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_brand_world()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
    
    sys.exit(0 if success else 1) 