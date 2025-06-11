#!/usr/bin/env python3
"""
Test script for improved Brand_World TF-IDF analysis
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

def test_tfidf_analysis():
    """Test the improved TF-IDF analysis with stop word removal"""
    
    try:
        from Brand_World.main import main, list_available_pdfs
        
        print("=== Brand_World TF-IDF Analysis Test ===")
        print("🔄 Testing improved analysis with:")
        print("  ✅ Stop word removal")
        print("  ✅ TF-IDF scoring (instead of simple frequency)")
        print("  ✅ Better tokenization")
        print("  ✅ Meaningful word filtering")
        
        # List available PDFs
        print("\n1. Checking available PDFs...")
        available_pdfs = list_available_pdfs()
        
        if not available_pdfs:
            print("❌ No PDFs found in files/brandword folder!")
            return False
        
        # Test with Skrewball PDF
        pdf_to_test = "Skrewball Brand World.pdf"
        print(f"\n2. Testing TF-IDF analysis with: {pdf_to_test}")
        
        if pdf_to_test not in available_pdfs:
            print(f"❌ PDF '{pdf_to_test}' not found!")
            print("Available PDFs:")
            for pdf in available_pdfs:
                print(f"  - {pdf}")
            return False
        
        # Run the improved analysis
        print(f"\n3. Running TF-IDF analysis on {pdf_to_test}...")
        print("   This will:")
        print("   • Extract and chunk the PDF")
        print("   • Process chunks through DeepSeek API")
        print("   • Remove stop words from extracted text")
        print("   • Calculate TF-IDF scores for meaningful words")
        print("   • Create probability distributions based on TF-IDF")
        
        results = main(pdf_to_test)
        
        if results and results.get('metadata'):
            print("\n✅ TF-IDF Analysis completed successfully!")
            print(f"📊 Processed {results['metadata']['total_chunks_processed']} chunks")
            print(f"📈 Found meaningful data in {results['summary']['dimensions_with_data']} dimensions")
            print(f"🎯 Total unique meaningful words: {results['summary']['total_unique_meaningful_words']}")
            print(f"📋 Average unique words per dimension: {results['summary']['average_unique_words_per_dimension']:.1f}")
            
            # Show analysis type
            print(f"\n🔬 Analysis Details:")
            print(f"   Type: {results['metadata']['analysis_type']}")
            print(f"   Stop words used: {results['metadata']['stop_words_used']}")
            print(f"   NLTK available: {results['metadata']['nltk_available']}")
            
            # Show most active dimensions
            if results['summary']['most_active_dimensions']:
                print(f"\n🏆 Most content-rich dimensions:")
                for i, (dim, word_count) in enumerate(results['summary']['most_active_dimensions'], 1):
                    print(f"   {i}. {dim}: {word_count} meaningful words")
            
            # Show example TF-IDF scores from one dimension
            print(f"\n📝 Sample TF-IDF Analysis (from most active dimension):")
            if results['summary']['most_active_dimensions']:
                top_dimension = results['summary']['most_active_dimensions'][0][0]
                tfidf_data = results['tfidf_analysis'].get(top_dimension, {})
                
                if tfidf_data.get('top_10_tfidf'):
                    print(f"   Dimension: {top_dimension}")
                    print(f"   Raw words: {tfidf_data['raw_word_count']}, Stop words removed: {tfidf_data['removed_stop_words']}")
                    print(f"   Top meaningful words by TF-IDF:")
                    for word, score in tfidf_data['top_10_tfidf'][:5]:
                        prob = tfidf_data['probability_distribution'].get(word, 0)
                        print(f"     • '{word}': TF-IDF={score:.4f}, Probability={prob:.2%}")
            
            return True
        else:
            print("❌ TF-IDF analysis failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install langchain pdfplumber nltk")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def compare_with_old_method():
    """Compare the improvements over simple frequency counting"""
    
    print("\n=== Comparison: TF-IDF vs Simple Frequency ===")
    print("🆚 Improvements in new method:")
    print("   ✅ Stop words removed (the, and, is, of, etc.)")
    print("   ✅ TF-IDF scoring gives higher weight to unique/important words")
    print("   ✅ Better tokenization with NLTK")
    print("   ✅ Filters out numbers and non-alphabetic tokens")
    print("   ✅ Probability distributions based on semantic importance")
    print("   ✅ Cross-dimension analysis for better IDF calculation")
    
    print("\n❌ Problems with old simple frequency method:")
    print("   • Common words (the, and, is) got high scores")
    print("   • No consideration of word importance across dimensions")
    print("   • Numbers and punctuation included")
    print("   • Simple counting doesn't reflect semantic value")

if __name__ == "__main__":
    print("Testing improved Brand_World TF-IDF Analysis...\n")
    
    # Show comparison first
    compare_with_old_method()
    
    # Run the test
    success = test_tfidf_analysis()
    
    if success:
        print("\n🎉 TF-IDF analysis test completed successfully!")
        print("The new analysis provides much better, more meaningful results!")
    else:
        print("\n💥 Test failed!")
    
    sys.exit(0 if success else 1) 