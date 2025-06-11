import sys
import os
import json
from typing import List, Dict, Any

# Add parent directory to path to import from root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import dimension_extraction_prompt
from utils import deepseek_chat
from Brief_Dimension_Generation.briefs import (
    abs_china,
    ballantine_poland, 
    Abs_Valentine,
    Codigo,
    ABS_OCEAN_SPRAY,
    Oaken_Glow,
    ABS_PRIDE
)

# Import the new gap filling functionality
from Brief_Gap_Filling.utils import main as gap_filling_main, gap_fill_with_evaluation

# Available briefs mapping
AVAILABLE_BRIEFS = {
    'abs_china': abs_china,
    'ballantine_poland': ballantine_poland,
    'abs_valentine': Abs_Valentine,
    'codigo': Codigo,
    'abs_ocean_spray': ABS_OCEAN_SPRAY,
    'oaken_glow': Oaken_Glow,
    'abs_pride': ABS_PRIDE
}

# Standard dimension list for gap filling
STANDARD_DIMENSIONS = [
    'Campaign Theme',
    'Marketing Objectives',
    'Universal Consumer Challenge',
    'Local Consumer Challenge (Market-Specific)',
    'Brand Context/Heritage',
    'Campaign Ambition/Scope',
    'Target Audience (Strategic Segment)',
    'Audience Demographics/Behavior',
    'Single-Minded Message',
    'Tone of Voice',
    'Key Deliverables/Assets',
    'Success Metrics (KPIs)',
    'Mandatory Channels/Formats',
    'Representation/Inclusivity Guidelines',
    'Cultural Adaptation Requirements'
]

def extract_dimensions_from_brief(brief_name: str, brief_content: str) -> List[str]:
    """
    Extract dimensions from a single brief using DeepSeek API
    
    Args:
        brief_name: Name of the brief
        brief_content: Content of the brief
    
    Returns:
        List of extracted dimensions
    """
    print(f"Extracting dimensions from: {brief_name}")
    
    try:
        message = f"{dimension_extraction_prompt}\n\nBrief content:\n{brief_content}"
        response = deepseek_chat(message)
        
        # Parse the response - assuming it returns dimensions in CSV format
        dimensions = [dim.strip() for dim in response.split(',') if dim.strip()]
        print(f"Extracted {len(dimensions)} dimensions from {brief_name}")
        return dimensions
        
    except Exception as e:
        print(f"Error extracting dimensions from {brief_name}: {e}")
        return []

def process_briefs(brief_names: List[str]) -> Dict[str, Any]:
    """
    Process multiple briefs to extract dimensions and create campaign dictionary
    
    Args:
        brief_names: List of brief names to process
    
    Returns:
        Dictionary containing all extracted dimensions and metadata
    """
    if not brief_names:
        raise ValueError("brief_names list cannot be empty")
    
    # Validate brief names
    invalid_briefs = [name for name in brief_names if name not in AVAILABLE_BRIEFS]
    if invalid_briefs:
        raise ValueError(f"Invalid brief names: {invalid_briefs}. Available: {list(AVAILABLE_BRIEFS.keys())}")
    
    print(f"Processing {len(brief_names)} briefs: {brief_names}")
    
    campaign_dict = {
        'metadata': {
            'total_briefs_processed': len(brief_names),
            'brief_names': brief_names,
            'analysis_timestamp': __import__('datetime').datetime.now().isoformat()
        },
        'briefs': {},
        'all_dimensions': set(),
        'dimension_frequency': {},
        'summary': {}
    }
    
    # Process each brief
    for brief_name in brief_names:
        brief_content = AVAILABLE_BRIEFS[brief_name]
        dimensions = extract_dimensions_from_brief(brief_name, brief_content)
        
        campaign_dict['briefs'][brief_name] = {
            'dimensions': dimensions,
            'dimension_count': len(dimensions),
            'brief_content_length': len(brief_content)
        }
        
        # Add to all dimensions set
        campaign_dict['all_dimensions'].update(dimensions)
        
        # Count dimension frequency
        for dimension in dimensions:
            campaign_dict['dimension_frequency'][dimension] = campaign_dict['dimension_frequency'].get(dimension, 0) + 1
    
    # Convert set to list for JSON serialization
    campaign_dict['all_dimensions'] = sorted(list(campaign_dict['all_dimensions']))
    
    # Create summary
    campaign_dict['summary'] = {
        'total_unique_dimensions': len(campaign_dict['all_dimensions']),
        'average_dimensions_per_brief': sum(data['dimension_count'] for data in campaign_dict['briefs'].values()) / len(brief_names),
        'most_common_dimensions': sorted(
            campaign_dict['dimension_frequency'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10],
        'dimensions_appearing_in_all_briefs': [
            dim for dim, freq in campaign_dict['dimension_frequency'].items() 
            if freq == len(brief_names)
        ]
    }
    
    return campaign_dict

def print_results(campaign_dict: Dict[str, Any]) -> None:
    """
    Print formatted results of dimension extraction
    
    Args:
        campaign_dict: Dictionary containing extraction results
    """
    print("\n" + "="*60)
    print("BRIEF DIMENSION EXTRACTION RESULTS")
    print("="*60)
    
    print(f"\nProcessed {campaign_dict['metadata']['total_briefs_processed']} briefs:")
    for brief_name in campaign_dict['metadata']['brief_names']:
        brief_data = campaign_dict['briefs'][brief_name]
        print(f"  • {brief_name}: {brief_data['dimension_count']} dimensions")
    
    print(f"\nTotal unique dimensions found: {campaign_dict['summary']['total_unique_dimensions']}")
    print(f"Average dimensions per brief: {campaign_dict['summary']['average_dimensions_per_brief']:.1f}")
    
    if campaign_dict['summary']['dimensions_appearing_in_all_briefs']:
        print(f"\nDimensions appearing in ALL briefs:")
        for dim in campaign_dict['summary']['dimensions_appearing_in_all_briefs']:
            print(f"  • {dim}")
    
    print(f"\nTop 10 most common dimensions:")
    for dim, freq in campaign_dict['summary']['most_common_dimensions']:
        print(f"  • {dim}: appears in {freq}/{campaign_dict['metadata']['total_briefs_processed']} briefs")

def save_results(campaign_dict: Dict[str, Any], output_filename: str = None) -> str:
    """
    Save results to JSON file
    
    Args:
        campaign_dict: Dictionary containing extraction results
        output_filename: Custom output filename (optional)
    
    Returns:
        Path to saved file
    """
    if output_filename is None:
        brief_names_str = "_".join(campaign_dict['metadata']['brief_names'])
        output_filename = f"Brief_Dimension_Generation/dimensions_{brief_names_str}.json"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(campaign_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_filename}")
    return output_filename

def list_available_briefs() -> None:
    """
    Display all available brief names
    """
    print("Available brief names:")
    for brief_name in AVAILABLE_BRIEFS.keys():
        print(f"  • {brief_name}")

def main(brief_names: List[str]) -> Dict[str, Any]:
    """
    Main function to extract dimensions from specified briefs
    
    Args:
        brief_names: List of brief names to process
    
    Returns:
        Dictionary containing all extraction results
    """
    print("Starting Brief Dimension Extraction Pipeline...")
    
    try:
        # Process briefs and extract dimensions
        campaign_dict = process_briefs(brief_names)
        
        # Print results
        print_results(campaign_dict)
        
        # Save results
        save_results(campaign_dict)
        
        print(f"\n" + "="*60)
        print("DIMENSION EXTRACTION COMPLETE")
        print("="*60)
        
        return campaign_dict
        
    except Exception as e:
        print(f"Error during processing: {e}")
        print("\nTip: Use list_available_briefs() to see available brief names")
        return {}

def gap_fill_brief(brief_name: str, 
                   dimension_list: List[str] = None,
                   brandworld_file_path: str = None,
                   use_distinct_words: bool = True) -> Dict[str, Any]:
    """
    Use gap filling to extract and fill dimensions for a specific brief (Tarik's distinct words approach)
    
    Args:
        brief_name: Name of the brief from AVAILABLE_BRIEFS
        dimension_list: List of dimensions to extract (default: STANDARD_DIMENSIONS)
        brandworld_file_path: Path to brandworld file (distinct words or legacy analysis)
        use_distinct_words: Whether to use Tarik's distinct words approach (default: True)
    
    Returns:
        Dictionary containing gap-filled results
    """
    if brief_name not in AVAILABLE_BRIEFS:
        raise ValueError(f"Brief '{brief_name}' not found. Available: {list(AVAILABLE_BRIEFS.keys())}")
    
    if dimension_list is None:
        dimension_list = STANDARD_DIMENSIONS
    
    if brandworld_file_path is None:
        # Default to using Tarik's distinct words approach with BALLANTINES data
        brandworld_file_path = "Brand_World/BALLANTINES-IBP-7_distinct_words.json"
    
    brief_content = AVAILABLE_BRIEFS[brief_name]
    
    print(f"\n🔄 Gap Filling Brief: {brief_name}")
    print(f"📋 Brief length: {len(brief_content)} characters")
    print(f"📊 Dimensions: {len(dimension_list)}")
    print(f"🎯 Brandworld source: {os.path.basename(brandworld_file_path)}")
    print(f"🔧 Method: {'Tarik''s distinct words' if use_distinct_words else 'Legacy TF-IDF'}")
    
    # Generate output filename
    output_filename = f"Brief_Gap_Filling/gap_filled_{brief_name}.json"
    
    # Run gap filling using the new approach
    result = gap_filling_main(
        brief_text=brief_content,
        dimension_list=dimension_list,
        brandworld_file_path=brandworld_file_path,
        deepseek_chat_func=deepseek_chat,
        output_filename=output_filename,
        use_distinct_words=use_distinct_words
    )
    
    return result

def compare_briefs_with_gap_filling(brief_names: List[str], 
                                  dimension_list: List[str] = None,
                                  brandworld_analysis_path: str = None) -> Dict[str, Any]:
    """
    Process multiple briefs with gap filling and compare results
    
    Args:
        brief_names: List of brief names to process
        dimension_list: List of dimensions to extract (default: STANDARD_DIMENSIONS)
        brandworld_analysis_path: Path to brandworld analysis file
    
    Returns:
        Dictionary containing comparison results
    """
    if dimension_list is None:
        dimension_list = STANDARD_DIMENSIONS
    
    if brandworld_analysis_path is None:
        brandworld_analysis_path = "Brand_World/Skrewball Brand World_analysis.json"
    
    print("\n" + "="*60)
    print("BRIEF COMPARISON WITH GAP FILLING")
    print("="*60)
    
    results = {}
    comparison_data = {
        'metadata': {
            'briefs_processed': brief_names,
            'total_dimensions': len(dimension_list),
            'brandworld_source': os.path.basename(brandworld_analysis_path),
            'timestamp': __import__('datetime').datetime.now().isoformat()
        },
        'individual_results': {},
        'comparison': {
            'dimension_fill_rates': {},
            'source_distribution': {},
            'common_filled_dimensions': [],
            'common_empty_dimensions': []
        }
    }
    
    for brief_name in brief_names:
        print(f"\n{'='*40}")
        print(f"Processing: {brief_name}")
        print(f"{'='*40}")
        
        try:
            result = gap_fill_brief(brief_name, dimension_list, brandworld_analysis_path)
            results[brief_name] = result
            comparison_data['individual_results'][brief_name] = result
            
        except Exception as e:
            print(f"❌ Error processing {brief_name}: {e}")
            continue
    
    # Generate comparison statistics
    if results:
        print(f"\n{'='*60}")
        print("COMPARISON ANALYSIS")
        print(f"{'='*60}")
        
        # Calculate fill rates per dimension
        for dim in dimension_list:
            filled_count = 0
            total_count = len(results)
            
            for brief_result in results.values():
                if brief_result['filled_table']['dimensions'][dim].strip():
                    filled_count += 1
            
            fill_rate = (filled_count / total_count) * 100 if total_count > 0 else 0
            comparison_data['comparison']['dimension_fill_rates'][dim] = fill_rate
        
        # Calculate source distribution
        source_counts = {'deepseek_extraction': 0, 'brandworld_probability': 0, 'no_data': 0}
        total_entries = len(results) * len(dimension_list)
        
        for brief_result in results.values():
            for source in brief_result['filled_table']['sources'].values():
                if source == 'deepseek_extraction':
                    source_counts['deepseek_extraction'] += 1
                elif source == 'brandworld_probability':
                    source_counts['brandworld_probability'] += 1
                else:
                    source_counts['no_data'] += 1
        
        comparison_data['comparison']['source_distribution'] = {
            source: (count / total_entries) * 100 
            for source, count in source_counts.items()
        }
        
        # Find common patterns
        all_filled = set(dimension_list)
        all_empty = set(dimension_list)
        
        for brief_result in results.values():
            brief_filled = set(brief_result['detailed_analysis']['dimensions_with_data'])
            brief_empty = set(brief_result['detailed_analysis']['empty_dimensions'])
            
            all_filled = all_filled.intersection(brief_filled)
            all_empty = all_empty.intersection(brief_empty)
        
        comparison_data['comparison']['common_filled_dimensions'] = list(all_filled)
        comparison_data['comparison']['common_empty_dimensions'] = list(all_empty)
        
        # Print summary
        print(f"\n📊 Overall Statistics:")
        print(f"  Total briefs processed: {len(results)}")
        print(f"  Average DeepSeek fill rate: {comparison_data['comparison']['source_distribution']['deepseek_extraction']:.1f}%")
        print(f"  Average Brandworld fill rate: {comparison_data['comparison']['source_distribution']['brandworld_probability']:.1f}%")
        print(f"  Average no-data rate: {comparison_data['comparison']['source_distribution']['no_data']:.1f}%")
        
        if comparison_data['comparison']['common_filled_dimensions']:
            print(f"\n✅ Dimensions filled in ALL briefs ({len(comparison_data['comparison']['common_filled_dimensions'])}):")
            for dim in comparison_data['comparison']['common_filled_dimensions']:
                print(f"  • {dim}")
        
        if comparison_data['comparison']['common_empty_dimensions']:
            print(f"\n❌ Dimensions empty in ALL briefs ({len(comparison_data['comparison']['common_empty_dimensions'])}):")
            for dim in comparison_data['comparison']['common_empty_dimensions']:
                print(f"  • {dim}")
    
    # Save comparison results
    output_filename = f"Brief_Gap_Filling/comparison_{'_'.join(brief_names)}.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Comparison results saved to: {output_filename}")
    return comparison_data

def gap_fill_brief_with_evaluation(brief_name: str, 
                                 dimension_list: List[str] = None,
                                 brandworld_analysis_path: str = None,
                                 n_versions: int = 5) -> Dict[str, Any]:
    """
    Use enhanced gap filling with evaluation to create and rank multiple versions
    
    Args:
        brief_name: Name of the brief from AVAILABLE_BRIEFS
        dimension_list: List of dimensions to extract (default: STANDARD_DIMENSIONS)
        brandworld_analysis_path: Path to brandworld analysis file
        n_versions: Number of versions to generate and evaluate
    
    Returns:
        Dictionary containing comprehensive evaluation results
    """
    if brief_name not in AVAILABLE_BRIEFS:
        raise ValueError(f"Brief '{brief_name}' not found. Available: {list(AVAILABLE_BRIEFS.keys())}")
    
    if dimension_list is None:
        dimension_list = STANDARD_DIMENSIONS
    
    if brandworld_analysis_path is None:
        brandworld_analysis_path = "Brand_World/Skrewball Brand World_analysis.json"
    
    brief_content = AVAILABLE_BRIEFS[brief_name]
    
    print(f"\n🔄 Enhanced Gap Filling with Evaluation: {brief_name}")
    print(f"📋 Brief length: {len(brief_content)} characters")
    print(f"📊 Dimensions: {len(dimension_list)}")
    print(f"🎯 Brandworld source: {os.path.basename(brandworld_analysis_path)}")
    print(f"🔢 Versions to generate: {n_versions}")
    
    # Run enhanced gap filling with evaluation
    result = gap_fill_with_evaluation(
        brief_text=brief_content,
        dimension_list=dimension_list,
        brandworld_analysis_path=brandworld_analysis_path,
        deepseek_chat_func=deepseek_chat,
        n_versions=n_versions,
        brief_name=brief_name
    )
    
    return result

def compare_briefs_with_enhanced_evaluation(brief_names: List[str], 
                                          dimension_list: List[str] = None,
                                          brandworld_analysis_path: str = None,
                                          n_versions: int = 5) -> Dict[str, Any]:
    """
    Process multiple briefs with enhanced gap filling and evaluation
    
    Args:
        brief_names: List of brief names to process
        dimension_list: List of dimensions to extract (default: STANDARD_DIMENSIONS)
        brandworld_analysis_path: Path to brandworld analysis file
        n_versions: Number of versions to generate per brief
    
    Returns:
        Dictionary containing comprehensive comparison results
    """
    if dimension_list is None:
        dimension_list = STANDARD_DIMENSIONS
    
    if brandworld_analysis_path is None:
        brandworld_analysis_path = "Brand_World/Skrewball Brand World_analysis.json"
    
    print("\n" + "="*80)
    print("ENHANCED BRIEF COMPARISON WITH EVALUATION")
    print("="*80)
    
    results = {}
    comparison_data = {
        'metadata': {
            'briefs_processed': brief_names,
            'total_dimensions': len(dimension_list),
            'versions_per_brief': n_versions,
            'brandworld_source': os.path.basename(brandworld_analysis_path),
            'timestamp': __import__('datetime').datetime.now().isoformat()
        },
        'individual_results': {},
        'cross_brief_analysis': {
            'best_scores_by_brief': {},
            'average_scores_by_brief': {},
            'best_overall_version': None
        }
    }
    
    all_top_versions = []
    
    for brief_name in brief_names:
        print(f"\n{'='*60}")
        print(f"Processing: {brief_name}")
        print(f"{'='*60}")
        
        try:
            result = gap_fill_brief_with_evaluation(
                brief_name, dimension_list, brandworld_analysis_path, n_versions
            )
            results[brief_name] = result
            comparison_data['individual_results'][brief_name] = result
            
            # Extract top version for cross-brief comparison
            if result['top_3_versions']:
                best_version = result['top_3_versions'][0]
                best_score = best_version['evaluation']['summary_scores']['total_score']
                avg_score = result['evaluation_summary']['average_score']
                
                comparison_data['cross_brief_analysis']['best_scores_by_brief'][brief_name] = best_score
                comparison_data['cross_brief_analysis']['average_scores_by_brief'][brief_name] = avg_score
                
                # Add brief name to version for cross-comparison
                best_version['brief_name'] = brief_name
                all_top_versions.append(best_version)
            
        except Exception as e:
            print(f"❌ Error processing {brief_name}: {e}")
            continue
    
    # Find overall best version across all briefs
    if all_top_versions:
        all_top_versions.sort(key=lambda x: x['evaluation']['summary_scores']['total_score'], reverse=True)
        comparison_data['cross_brief_analysis']['best_overall_version'] = all_top_versions[0]
        
        print(f"\n{'='*80}")
        print("CROSS-BRIEF ANALYSIS")
        print(f"{'='*80}")
        
        print(f"\n🏆 Best Scores by Brief:")
        for brief_name, score in comparison_data['cross_brief_analysis']['best_scores_by_brief'].items():
            print(f"  • {brief_name}: {score:.2f}")
        
        print(f"\n📊 Average Scores by Brief:")
        for brief_name, score in comparison_data['cross_brief_analysis']['average_scores_by_brief'].items():
            print(f"  • {brief_name}: {score:.2f}")
        
        best_overall = comparison_data['cross_brief_analysis']['best_overall_version']
        print(f"\n👑 Overall Best Version:")
        print(f"  Brief: {best_overall['brief_name']}")
        print(f"  Version ID: {best_overall['version_id']}")
        print(f"  Score: {best_overall['evaluation']['summary_scores']['total_score']:.2f}")
    
    # Save comprehensive comparison results
    output_filename = f"Brief_Gap_Filling/enhanced_comparison_{'_'.join(brief_names)}.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Enhanced comparison results saved to: {output_filename}")
    return comparison_data

# Example usage and main execution
if __name__ == "__main__":
    # Display available briefs
    print("Brief Gap Filling System")
    print("=" * 40)
    list_available_briefs()
    
    print("\n🔧 Available Functions:")
    print("1. gap_fill_brief(brief_name) - Fill single brief")
    print("2. compare_briefs_with_gap_filling(brief_names) - Compare multiple briefs")
    print("3. gap_fill_brief_with_evaluation(brief_name, n_versions) - Enhanced evaluation (NEW)")
    print("4. compare_briefs_with_enhanced_evaluation(brief_names, n_versions) - Multi-brief evaluation (NEW)")
    print("5. main(brief_names) - Original dimension extraction")
    
    # Example 1: Single brief gap filling
    print(f"\n{'='*60}")
    print("EXAMPLE 1: Single Brief Gap Filling")
    print(f"{'='*60}")
    
    try:
        result = gap_fill_brief('ballantine_poland')
        print("✅ Single brief gap filling completed!")
    except Exception as e:
        print(f"❌ Single brief example failed: {e}")
    
    # Example 2: Multiple brief comparison
    print(f"\n{'='*60}")
    print("EXAMPLE 2: Multiple Brief Comparison")
    print(f"{'='*60}")
    
    try:
        comparison_result = compare_briefs_with_gap_filling(['abs_china', 'ballantine_poland'])
        print("✅ Multiple brief comparison completed!")
    except Exception as e:
        print(f"❌ Multiple brief example failed: {e}")
    
    # Example 3: Enhanced gap filling with evaluation (NEW)
    print(f"\n{'='*80}")
    print("EXAMPLE 3: Enhanced Gap Filling with Evaluation")
    print(f"{'='*80}")
    
    try:
        enhanced_result = gap_fill_brief_with_evaluation('ballantine_poland', n_versions=3)
        print("✅ Enhanced gap filling with evaluation completed!")
        print(f"🏆 Best score achieved: {enhanced_result['evaluation_summary']['best_score']:.2f}")
        print(f"📁 Top 3 results saved to: {len(enhanced_result['saved_files'])} files")
    except Exception as e:
        print(f"❌ Enhanced gap filling example failed: {e}")
    
    # Example 4: Enhanced multi-brief comparison (NEW)
    print(f"\n{'='*80}")
    print("EXAMPLE 4: Enhanced Multi-Brief Comparison")
    print(f"{'='*80}")
    
    try:
        enhanced_comparison = compare_briefs_with_enhanced_evaluation(
            ['abs_china', 'ballantine_poland'], n_versions=3
        )
        print("✅ Enhanced multi-brief comparison completed!")
        
        if enhanced_comparison['cross_brief_analysis']['best_overall_version']:
            best = enhanced_comparison['cross_brief_analysis']['best_overall_version']
            print(f"👑 Overall best: {best['brief_name']} (Score: {best['evaluation']['summary_scores']['total_score']:.2f})")
    except Exception as e:
        print(f"❌ Enhanced multi-brief comparison failed: {e}")