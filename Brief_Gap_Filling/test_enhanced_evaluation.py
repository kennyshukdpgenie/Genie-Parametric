#!/usr/bin/env python3
"""
Test script for the enhanced gap filling with evaluation functionality.
This script demonstrates the new features that generate N versions of gap-filled 
dimension tables and evaluate them using DeepSeek.
"""

import sys
import os
from typing import List, Dict, Any

# Add parent directory to path to import from root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Brief_Gap_Filling.main import (
    gap_fill_brief_with_evaluation,
    compare_briefs_with_enhanced_evaluation,
    list_available_briefs
)

def test_single_brief_enhanced_evaluation():
    """Test enhanced evaluation on a single brief"""
    print("="*80)
    print("TEST 1: Single Brief Enhanced Evaluation")
    print("="*80)
    
    try:
        # Test with ballantine_poland brief, generate 3 versions
        result = gap_fill_brief_with_evaluation(
            brief_name='ballantine_poland',
            n_versions=3
        )
        
        print(f"\n✅ Test completed successfully!")
        print(f"📊 Generated {result['metadata']['versions_generated']} versions")
        print(f"🏆 Best score: {result['evaluation_summary']['best_score']:.2f}")
        print(f"📉 Worst score: {result['evaluation_summary']['worst_score']:.2f}")
        print(f"📊 Average score: {result['evaluation_summary']['average_score']:.2f}")
        print(f"💾 Saved {len(result['saved_files'])} top result files")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_multi_brief_enhanced_evaluation():
    """Test enhanced evaluation on multiple briefs"""
    print("\n" + "="*80)
    print("TEST 2: Multi-Brief Enhanced Evaluation")
    print("="*80)
    
    try:
        # Test with two briefs, generate 2 versions each
        result = compare_briefs_with_enhanced_evaluation(
            brief_names=['abs_china', 'ballantine_poland'],
            n_versions=2
        )
        
        print(f"\n✅ Test completed successfully!")
        print(f"📊 Processed {len(result['metadata']['briefs_processed'])} briefs")
        print(f"🔢 Generated {result['metadata']['versions_per_brief']} versions per brief")
        
        if result['cross_brief_analysis']['best_overall_version']:
            best = result['cross_brief_analysis']['best_overall_version']
            print(f"👑 Overall winner: {best['brief_name']} (Score: {best['evaluation']['summary_scores']['total_score']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def demonstrate_evaluation_scores():
    """Demonstrate the evaluation scoring system"""
    print("\n" + "="*80)
    print("EVALUATION SCORING DEMONSTRATION")
    print("="*80)
    
    print("\n📋 How the evaluation works:")
    print("1. Generate N versions of gap-filled dimension tables")
    print("2. For each filled dimension, evaluate two aspects:")
    print("   - Dimension-Value Match (1-5): How well the value fits the dimension")
    print("   - Context Coherence (1-5): How well the value fits with other dimensions")
    print("3. Calculate average scores and rank versions")
    print("4. Save top 3 versions as JSON files")
    
    print("\n🏆 Scoring criteria:")
    print("- Score 5: Perfect match/coherence")
    print("- Score 4: Very good match/coherence")
    print("- Score 3: Decent match/coherence")
    print("- Score 2: Weak match/coherence")
    print("- Score 1: Poor match/coherence")
    
    print("\n💾 Output files include:")
    print("- Complete dimension tables with filled values")
    print("- Detailed evaluation scores for each dimension")
    print("- Source tracking (DeepSeek vs Brandworld)")
    print("- Reasoning for each evaluation score")

def main():
    """Main test function"""
    print("Enhanced Gap Filling Evaluation Test Suite")
    print("=" * 50)
    
    # Show available briefs
    print("\nAvailable briefs for testing:")
    list_available_briefs()
    
    # Demonstrate evaluation system
    demonstrate_evaluation_scores()
    
    # Run tests
    test1_success = test_single_brief_enhanced_evaluation()
    test2_success = test_multi_brief_enhanced_evaluation()
    
    print("\n" + "="*80)
    print("TEST RESULTS SUMMARY")
    print("="*80)
    print(f"Single Brief Enhanced Evaluation: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    print(f"Multi-Brief Enhanced Evaluation: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! The enhanced evaluation system is working correctly.")
        print("\n📁 Check the Brief_Gap_Filling folder for output files:")
        print("- top_1_*, top_2_*, top_3_* files contain the best evaluated versions")
        print("- enhanced_comparison_* files contain cross-brief analysis")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main() 