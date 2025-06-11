"""
Test script for Brief Gap Filling using Tarik's distinct words approach
This demonstrates the new integration between Brand_World and Brief_Gap_Filling

Author: Assistant AI (incorporating Tarik's distinct words approach)
Date: 2025-06-11
"""

import os
import sys
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import deepseek_chat if available
try:
    from deepseek_chat import deepseek_chat
    print("✅ DeepSeek chat loaded successfully")
except ImportError:
    print("⚠️  DeepSeek chat not available - using mock function")
    def deepseek_chat(message):
        return """```json
{
    "Campaign Theme": "Premium Scotch Whisky Heritage",
    "Marketing Objectives": "Build brand awareness and premium positioning",
    "Target Audience": "Affluent whisky enthusiasts aged 30-55",
    "Creative Concept": "Authentic ballantine scottish heritage",
    "Key Message": "True ballantine craftsmanship since 1827",
    "Tone and Style": "Premium confident ballantine brand voice"
}
```"""

from Brief_Gap_Filling.utils import main as gap_filling_main, print_gap_filling_results

# Sample brief for testing
SAMPLE_BRIEF = """
We need to create a premium campaign for Ballantines Scotch Whisky targeting affluent consumers in Poland. 
The campaign should emphasize the brand's Scottish heritage and craftsmanship traditions dating back to 1827.
Focus on sophisticated whisky enthusiasts who appreciate quality and authenticity.
The creative should showcase the premium nature of the product while maintaining approachable elegance.
Budget considerations require efficient media placement with emphasis on digital channels.
"""

# Standard dimensions for testing
TEST_DIMENSIONS = [
    "Campaign Theme",
    "Marketing Objectives", 
    "Target Audience",
    "Creative Concept",
    "Key Message",
    "Tone and Style",
    "Media Strategy",
    "Budget Allocation",
    "Timeline",
    "Success Metrics"
]

def test_distinct_words_gap_filling():
    """Test the new distinct words gap filling approach"""
    print("="*80)
    print("TESTING BRIEF GAP FILLING WITH TARIK'S DISTINCT WORDS APPROACH")
    print("="*80)
    
    # Check if distinct words file exists
    distinct_words_file = "Brand_World/BALLANTINES-IBP-7_distinct_words.json"
    
    if not os.path.exists(distinct_words_file):
        print(f"❌ Distinct words file not found: {distinct_words_file}")
        print("Please ensure you have generated the distinct words file from Brand_World")
        return
    
    # Load and display sample of distinct words
    with open(distinct_words_file, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    
    distinct_words = words_data.get('distinct_words', [])
    print(f"📚 Using {len(distinct_words)} distinct words from Brand_World")
    print(f"📄 Sample words: {', '.join(distinct_words[:15])}...")
    
    print(f"\n📋 Test Brief (first 200 chars):")
    print(f"'{SAMPLE_BRIEF[:200]}...'")
    
    print(f"\n📊 Testing {len(TEST_DIMENSIONS)} dimensions:")
    for i, dim in enumerate(TEST_DIMENSIONS, 1):
        print(f"  {i:2d}. {dim}")
    
    try:
        # Test with distinct words approach
        print(f"\n🔄 Running gap filling with Tarik's distinct words approach...")
        result = gap_filling_main(
            brief_text=SAMPLE_BRIEF,
            dimension_list=TEST_DIMENSIONS,
            brandworld_file_path=distinct_words_file,
            deepseek_chat_func=deepseek_chat,
            output_filename="Brief_Gap_Filling/test_distinct_words_result.json",
            use_distinct_words=True
        )
        
        print(f"\n✅ Gap filling completed successfully!")
        return result
        
    except Exception as e:
        print(f"❌ Error during gap filling: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_with_legacy_approach():
    """Compare new distinct words approach with legacy TF-IDF approach"""
    print("\n" + "="*80)
    print("COMPARING DISTINCT WORDS VS LEGACY TF-IDF APPROACHES")
    print("="*80)
    
    # Check if legacy file exists
    legacy_file = "Brand_World/Skrewball Brand World_analysis.json"
    distinct_words_file = "Brand_World/BALLANTINES-IBP-7_distinct_words.json"
    
    if not os.path.exists(legacy_file):
        print(f"⚠️  Legacy file not found: {legacy_file}")
        print("Skipping comparison...")
        return
    
    if not os.path.exists(distinct_words_file):
        print(f"⚠️  Distinct words file not found: {distinct_words_file}")
        print("Skipping comparison...")
        return
    
    # Test both approaches with smaller dimension set for comparison
    comparison_dimensions = [
        "Campaign Theme",
        "Target Audience", 
        "Creative Concept",
        "Key Message",
        "Tone and Style"
    ]
    
    results = {}
    
    try:
        # Test legacy approach
        print(f"\n🔄 Testing Legacy TF-IDF approach...")
        legacy_result = gap_filling_main(
            brief_text=SAMPLE_BRIEF,
            dimension_list=comparison_dimensions,
            brandworld_file_path=legacy_file,
            deepseek_chat_func=deepseek_chat,
            output_filename="Brief_Gap_Filling/test_legacy_result.json",
            use_distinct_words=False
        )
        results['legacy'] = legacy_result
        
    except Exception as e:
        print(f"⚠️  Legacy approach failed: {e}")
        results['legacy'] = None
    
    try:
        # Test distinct words approach
        print(f"\n🔄 Testing Tarik's Distinct Words approach...")
        distinct_result = gap_filling_main(
            brief_text=SAMPLE_BRIEF,
            dimension_list=comparison_dimensions,
            brandworld_file_path=distinct_words_file,
            deepseek_chat_func=deepseek_chat,
            output_filename="Brief_Gap_Filling/test_distinct_comparison_result.json",
            use_distinct_words=True
        )
        results['distinct'] = distinct_result
        
    except Exception as e:
        print(f"⚠️  Distinct words approach failed: {e}")
        results['distinct'] = None
    
    # Compare results
    if results['legacy'] and results['distinct']:
        print(f"\n📊 COMPARISON SUMMARY:")
        print(f"  Legacy TF-IDF approach:")
        print(f"    Method: {results['legacy']['metadata']['gap_filling_method']}")
        print(f"    Filled: {results['legacy']['metadata']['filled_count']}/{len(comparison_dimensions)}")
        
        print(f"  Tarik's Distinct Words approach:")
        print(f"    Method: {results['distinct']['metadata']['gap_filling_method']}")
        print(f"    Filled: {results['distinct']['metadata']['filled_count']}/{len(comparison_dimensions)}")
        
        print(f"\n🎯 Both approaches completed successfully!")
        return results
    else:
        print(f"\n⚠️  Could not complete comparison due to errors")
        return results

def main():
    """Main test function"""
    print("🚀 Starting Brief Gap Filling tests...")
    
    # Test 1: Basic distinct words functionality
    result1 = test_distinct_words_gap_filling()
    
    # Test 2: Compare approaches
    result2 = compare_with_legacy_approach()
    
    print(f"\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result1:
        print("✅ Distinct words gap filling: SUCCESS")
    else:
        print("❌ Distinct words gap filling: FAILED")
    
    if result2 and (result2.get('legacy') or result2.get('distinct')):
        print("✅ Approach comparison: COMPLETED")
    else:
        print("⚠️  Approach comparison: PARTIAL/FAILED")
    
    print(f"\n🎉 Testing completed!")
    print(f"📁 Check Brief_Gap_Filling/ folder for output files")

if __name__ == "__main__":
    main() 