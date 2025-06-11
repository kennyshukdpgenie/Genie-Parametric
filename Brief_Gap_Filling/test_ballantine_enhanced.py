#!/usr/bin/env python3
"""
Test script for Enhanced Gap Filling with Evaluation using Ballantine Poland brief.
This script tests the complete enhanced functionality using:
- ballantine_poland brief from Brand_World/briefs.py
- dimensions_ballantine_poland.json as brandworld analysis input
- DIM_LIST from Brand_World/utils.py as dimensions
"""

import sys
import os
import json
from typing import List, Dict, Any
from datetime import datetime

# Add parent directory to path to import from root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
from Brief_Gap_Filling.test_config import (
    BALLANTINE_POLAND_BRIEF,
    STANDARD_DIMENSIONS,
    DEFAULT_BRANDWORLD_PATH,
    TEST_CONFIG
)
from Brief_Gap_Filling.utils import gap_fill_with_evaluation

# Import deepseek_chat from root utils (not Brief_Gap_Filling utils)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import deepseek_chat

def print_test_header():
    """Print test header with configuration info"""
    print("="*80)
    print("ENHANCED GAP FILLING TEST - BALLANTINE POLAND")
    print("="*80)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 Brief: Ballantine Poland (self-contained)")
    print(f"📊 Brandworld Analysis: {DEFAULT_BRANDWORLD_PATH}")
    print(f"🎯 Dimension List: STANDARD_DIMENSIONS ({len(STANDARD_DIMENSIONS)} dimensions)")
    print(f"🔄 Test Type: Enhanced Gap Filling with AI Evaluation")
    print("="*80)

def validate_inputs():
    """Validate that all required input files and data exist"""
    print("\n🔍 VALIDATION PHASE")
    print("-"*40)
    
    # Check if brief exists
    if not BALLANTINE_POLAND_BRIEF:
        raise ValueError("❌ BALLANTINE_POLAND_BRIEF not found in test_config.py")
    print(f"✅ Brief loaded: {len(BALLANTINE_POLAND_BRIEF)} characters")
    
    # Check if dimension list exists
    if not STANDARD_DIMENSIONS or len(STANDARD_DIMENSIONS) == 0:
        raise ValueError("❌ STANDARD_DIMENSIONS not found or empty in test_config.py")
    print(f"✅ Dimensions loaded: {len(STANDARD_DIMENSIONS)} dimensions")
    
    # Check if brandworld analysis file exists
    brandworld_path = DEFAULT_BRANDWORLD_PATH
    if not os.path.exists(brandworld_path):
        raise FileNotFoundError(f"❌ Brandworld analysis file not found: {brandworld_path}")
    
    # Validate brandworld file content
    try:
        with open(brandworld_path, 'r', encoding='utf-8') as f:
            brandworld_data = json.load(f)
        print(f"✅ Brandworld analysis loaded: {brandworld_path}")
        print(f"   - Contains data for: {len(brandworld_data.get('briefs', {}))} briefs")
        print(f"   - Total dimensions found: {len(brandworld_data.get('all_dimensions', []))}")
    except Exception as e:
        raise ValueError(f"❌ Error loading brandworld analysis: {e}")
    
    print("✅ All inputs validated successfully!")
    return brandworld_path

def print_brief_preview():
    """Print a preview of the brief content"""
    print("\n📖 BRIEF PREVIEW")
    print("-"*40)
    brief_lines = BALLANTINE_POLAND_BRIEF.strip().split('\n')
    print(f"Brief has {len(brief_lines)} lines")
    print("First 5 lines:")
    for i, line in enumerate(brief_lines[:5]):
        print(f"  {i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
    
    if len(brief_lines) > 10:
        print("...")
        print("Last 3 lines:")
        for i, line in enumerate(brief_lines[-3:], len(brief_lines)-2):
            print(f"  {i}: {line[:80]}{'...' if len(line) > 80 else ''}")

def print_dimension_list():
    """Print the dimension list being used"""
    print("\n📋 DIMENSION LIST")
    print("-"*40)
    print(f"Using {len(STANDARD_DIMENSIONS)} standard dimensions:")
    for i, dim in enumerate(STANDARD_DIMENSIONS, 1):
        print(f"  {i:2d}. {dim}")

def run_enhanced_gap_filling_test(brandworld_path: str, n_versions: int = 5):
    """Run the enhanced gap filling test"""
    print(f"\n🚀 RUNNING ENHANCED GAP FILLING TEST")
    print("-"*40)
    print(f"🔢 Generating {n_versions} versions for evaluation")
    print(f"🤖 Using DeepSeek for evaluation")
    print(f"💾 Will save top 3 results automatically")
    
    start_time = datetime.now()
    
    try:
        # Run the enhanced gap filling with evaluation
        result = gap_fill_with_evaluation(
            brief_text=BALLANTINE_POLAND_BRIEF,
            dimension_list=STANDARD_DIMENSIONS,
            brandworld_analysis_path=brandworld_path,
            deepseek_chat_func=deepseek_chat,
            n_versions=n_versions,
            brief_name="ballantine_poland_test"
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Enhanced gap filling completed successfully!")
        print(f"⏱️ Total duration: {duration:.1f} seconds")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Enhanced gap filling failed: {e}")
        raise

def analyze_results(result: Dict[str, Any]):
    """Analyze and display the test results"""
    print("\n📊 RESULTS ANALYSIS")
    print("="*60)
    
    # Metadata analysis
    metadata = result['metadata']
    print(f"📅 Timestamp: {metadata['timestamp']}")
    print(f"📋 Brief Length: {metadata['brief_length']} characters")
    print(f"🎯 Total Dimensions: {metadata['total_dimensions']}")
    print(f"🔄 Versions Generated: {metadata['versions_generated']}")
    print(f"✅ Versions Evaluated: {metadata['versions_evaluated']}")
    
    # Evaluation summary
    eval_summary = result['evaluation_summary']
    print(f"\n🏆 EVALUATION SCORES")
    print(f"   Best Score: {eval_summary['best_score']:.2f} / 10.0")
    print(f"   Worst Score: {eval_summary['worst_score']:.2f} / 10.0")
    print(f"   Average Score: {eval_summary['average_score']:.2f} / 10.0")
    print(f"   Score Range: {eval_summary['best_score'] - eval_summary['worst_score']:.2f}")
    
    # Top 3 versions analysis
    print(f"\n🥇 TOP 3 VERSIONS SUMMARY")
    for i, version in enumerate(result['top_3_versions'], 1):
        scores = version['evaluation']['summary_scores']
        print(f"   {i}. Version {version['version_id']}: {scores['total_score']:.2f}")
        print(f"      - Dimension Match: {scores['average_dimension_match_score']:.2f}")
        print(f"      - Context Coherence: {scores['average_coherence_score']:.2f}")
        print(f"      - Dimensions Evaluated: {scores['dimensions_evaluated']}")
    
    # File output analysis
    print(f"\n💾 OUTPUT FILES")
    saved_files = result['saved_files']
    print(f"   Saved {len(saved_files)} result files:")
    for i, filepath in enumerate(saved_files, 1):
        filename = os.path.basename(filepath)
        print(f"   {i}. {filename}")
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"      Size: {file_size:.1f} KB")

def analyze_best_version_details(result: Dict[str, Any]):
    """Analyze the best version in detail"""
    if not result['top_3_versions']:
        print("❌ No versions available for detailed analysis")
        return
    
    best_version = result['top_3_versions'][0]
    
    print(f"\n🔍 DETAILED ANALYSIS - BEST VERSION (Version {best_version['version_id']})")
    print("="*60)
    
    filled_dimensions = best_version['filled_table']['dimensions']
    sources = best_version['filled_table']['sources']
    evaluations = best_version['evaluation']['dimension_evaluations']
    
    # Count sources
    deepseek_count = sum(1 for source in sources.values() if source == 'deepseek_extraction')
    brandworld_count = sum(1 for source in sources.values() if source == 'brandworld_probability')
    no_data_count = len(sources) - deepseek_count - brandworld_count
    
    print(f"📊 FILL SOURCES:")
    print(f"   🤖 DeepSeek Extraction: {deepseek_count}")
    print(f"   🎯 Brandworld Probability: {brandworld_count}")
    print(f"   ❌ No Data: {no_data_count}")
    
    # Show top and bottom evaluated dimensions
    scored_dimensions = []
    for dim_name, evaluation in evaluations.items():
        total_score = evaluation.get('dimension_value_match_score', 0) + evaluation.get('context_coherence_score', 0)
        scored_dimensions.append((dim_name, total_score, evaluation))
    
    scored_dimensions.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n🏆 TOP 3 BEST SCORING DIMENSIONS:")
    for i, (dim_name, total_score, evaluation) in enumerate(scored_dimensions[:3], 1):
        print(f"   {i}. {dim_name}: {total_score:.1f}/10")
        print(f"      Value: {filled_dimensions.get(dim_name, 'N/A')[:50]}...")
        print(f"      Match: {evaluation.get('dimension_value_match_score', 0)}/5")
        print(f"      Coherence: {evaluation.get('context_coherence_score', 0)}/5")
    
    if len(scored_dimensions) > 3:
        print(f"\n📉 BOTTOM 3 SCORING DIMENSIONS:")
        for i, (dim_name, total_score, evaluation) in enumerate(scored_dimensions[-3:], 1):
            print(f"   {i}. {dim_name}: {total_score:.1f}/10")
            print(f"      Value: {filled_dimensions.get(dim_name, 'N/A')[:50]}...")
            print(f"      Match: {evaluation.get('dimension_value_match_score', 0)}/5")
            print(f"      Coherence: {evaluation.get('context_coherence_score', 0)}/5")

def save_test_summary(result: Dict[str, Any], test_start_time: datetime):
    """Save a comprehensive test summary"""
    test_end_time = datetime.now()
    test_duration = (test_end_time - test_start_time).total_seconds()
    
    summary = {
        'test_metadata': {
            'test_name': 'Enhanced Gap Filling - Ballantine Poland',
            'test_start_time': test_start_time.isoformat(),
            'test_end_time': test_end_time.isoformat(),
            'test_duration_seconds': test_duration,
                         'brief_source': 'Brief_Gap_Filling/test_config.py - BALLANTINE_POLAND_BRIEF',
             'dimension_source': 'Brief_Gap_Filling/test_config.py - STANDARD_DIMENSIONS',
             'brandworld_source': DEFAULT_BRANDWORLD_PATH
        },
        'test_configuration': {
                         'brief_length': len(BALLANTINE_POLAND_BRIEF),
             'total_dimensions': len(STANDARD_DIMENSIONS),
            'versions_generated': result['metadata']['versions_generated'],
            'evaluation_method': 'DeepSeek AI with dual scoring criteria'
        },
        'test_results': {
            'success': True,
            'best_score': result['evaluation_summary']['best_score'],
            'average_score': result['evaluation_summary']['average_score'],
            'files_saved': len(result['saved_files']),
            'output_files': [os.path.basename(f) for f in result['saved_files']]
        },
                 'brief_content_preview': BALLANTINE_POLAND_BRIEF[:500] + "...",
         'dimensions_tested': STANDARD_DIMENSIONS,
        'full_results': result
    }
    
    # Save summary
    summary_filename = f"Brief_Gap_Filling/test_summary_ballantine_poland_{test_start_time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Test summary saved to: {summary_filename}")
    return summary_filename

def main():
    """Main test function"""
    test_start_time = datetime.now()
    
    try:
        # Print test header
        print_test_header()
        
        # Validate inputs
        brandworld_path = validate_inputs()
        
        # Show brief and dimension previews
        print_brief_preview()
        print_dimension_list()
        
        # Run the enhanced gap filling test
        result = run_enhanced_gap_filling_test(brandworld_path, n_versions=5)
        
        # Analyze results
        analyze_results(result)
        analyze_best_version_details(result)
        
        # Save test summary
        summary_file = save_test_summary(result, test_start_time)
        
        # Final success message
        print("\n" + "="*80)
        print("🎉 TEST COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"✅ Enhanced gap filling with evaluation completed")
        print(f"📊 Best score achieved: {result['evaluation_summary']['best_score']:.2f}/10.0")
        print(f"💾 Saved {len(result['saved_files'])} result files")
        print(f"📋 Test summary: {os.path.basename(summary_file)}")
        print(f"📁 Check Brief_Gap_Filling/ folder for all output files")
        
        return result
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print(f"⏱️ Test duration before failure: {(datetime.now() - test_start_time).total_seconds():.1f} seconds")
        raise

if __name__ == "__main__":
    # Run the test
    result = main() 