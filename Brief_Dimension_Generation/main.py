import sys
import os
import json
from typing import List, Dict, Any

# Add parent directory to path to import from root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import dimension_extraction_prompt
from utils import deepseek_chat
from Brief_Dimension_Generation.document_parser import (
    get_available_brief_files,
    load_brief_content,
    load_all_brief_contents,
    list_available_briefs
)

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

def process_briefs(brief_names: List[str], brief_folder: str = "files/brief") -> Dict[str, Any]:
    """
    Process multiple briefs to extract dimensions and create campaign dictionary
    
    Args:
        brief_names: List of brief names to process
        brief_folder: Path to brief folder
    
    Returns:
        Dictionary containing all extracted dimensions and metadata
    """
    if not brief_names:
        raise ValueError("brief_names list cannot be empty")
    
    # Get available briefs from files
    available_briefs = get_available_brief_files(brief_folder)
    
    # Validate brief names
    invalid_briefs = [name for name in brief_names if name not in available_briefs]
    if invalid_briefs:
        raise ValueError(f"Invalid brief names: {invalid_briefs}. Available: {list(available_briefs.keys())}")
    
    print(f"Processing {len(brief_names)} briefs: {brief_names}")
    
    campaign_dict = {
        'metadata': {
            'total_briefs_processed': len(brief_names),
            'brief_names': brief_names,
            'brief_folder': brief_folder,
            'analysis_timestamp': __import__('datetime').datetime.now().isoformat()
        },
        'briefs': {},
        'all_dimensions': set(),
        'dimension_frequency': {},
        'summary': {}
    }
    
    # Process each brief
    for brief_name in brief_names:
        try:
            brief_content = load_brief_content(brief_name, brief_folder)
            dimensions = extract_dimensions_from_brief(brief_name, brief_content)
            
            campaign_dict['briefs'][brief_name] = {
                'dimensions': dimensions,
                'dimension_count': len(dimensions),
                'brief_content_length': len(brief_content),
                'source_file': available_briefs[brief_name]
            }
            
            # Add to all dimensions set
            campaign_dict['all_dimensions'].update(dimensions)
            
            # Count dimension frequency
            for dimension in dimensions:
                campaign_dict['dimension_frequency'][dimension] = campaign_dict['dimension_frequency'].get(dimension, 0) + 1
                
        except Exception as e:
            print(f"Error processing {brief_name}: {e}")
            campaign_dict['briefs'][brief_name] = {
                'dimensions': [],
                'dimension_count': 0,
                'brief_content_length': 0,
                'source_file': available_briefs.get(brief_name, ""),
                'error': str(e)
            }
    
    # Convert set to list for JSON serialization
    campaign_dict['all_dimensions'] = sorted(list(campaign_dict['all_dimensions']))
    
    # Create summary
    successful_briefs = [name for name, data in campaign_dict['briefs'].items() if 'error' not in data]
    total_successful = len(successful_briefs)
    
    if total_successful > 0:
        campaign_dict['summary'] = {
            'total_unique_dimensions': len(campaign_dict['all_dimensions']),
            'successful_briefs': total_successful,
            'failed_briefs': len(brief_names) - total_successful,
            'average_dimensions_per_brief': sum(
                data['dimension_count'] for data in campaign_dict['briefs'].values() 
                if 'error' not in data
            ) / total_successful,
            'most_common_dimensions': sorted(
                campaign_dict['dimension_frequency'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10],
            'dimensions_appearing_in_all_briefs': [
                dim for dim, freq in campaign_dict['dimension_frequency'].items() 
                if freq == total_successful
            ]
        }
    else:
        campaign_dict['summary'] = {
            'total_unique_dimensions': 0,
            'successful_briefs': 0,
            'failed_briefs': len(brief_names),
            'average_dimensions_per_brief': 0,
            'most_common_dimensions': [],
            'dimensions_appearing_in_all_briefs': []
        }
    
    return campaign_dict

def process_all_available_briefs(brief_folder: str = "files/brief") -> Dict[str, Any]:
    """
    Process all available brief files in the folder
    
    Args:
        brief_folder: Path to brief folder
    
    Returns:
        Dictionary containing all extracted dimensions and metadata
    """
    available_briefs = get_available_brief_files(brief_folder)
    brief_names = list(available_briefs.keys())
    
    if not brief_names:
        raise ValueError(f"No brief files found in {brief_folder}")
    
    print(f"Processing all {len(brief_names)} available briefs...")
    return process_briefs(brief_names, brief_folder)

def print_results(campaign_dict: Dict[str, Any]) -> None:
    """
    Print formatted results of dimension extraction
    
    Args:
        campaign_dict: Dictionary containing extraction results
    """
    print("\n" + "="*60)
    print("BRIEF DIMENSION EXTRACTION RESULTS")
    print("="*60)
    
    print(f"\nProcessed {campaign_dict['metadata']['total_briefs_processed']} briefs from: {campaign_dict['metadata']['brief_folder']}")
    print(f"Successful: {campaign_dict['summary']['successful_briefs']}")
    print(f"Failed: {campaign_dict['summary']['failed_briefs']}")
    
    print(f"\nBrief Details:")
    for brief_name, brief_data in campaign_dict['briefs'].items():
        if 'error' in brief_data:
            print(f"  ✗ {brief_name}: ERROR - {brief_data['error']}")
        else:
            print(f"  ✓ {brief_name}: {brief_data['dimension_count']} dimensions ({brief_data['brief_content_length']} chars)")
    
    if campaign_dict['summary']['successful_briefs'] > 0:
        print(f"\nTotal unique dimensions found: {campaign_dict['summary']['total_unique_dimensions']}")
        print(f"Average dimensions per brief: {campaign_dict['summary']['average_dimensions_per_brief']:.1f}")
        
        if campaign_dict['summary']['dimensions_appearing_in_all_briefs']:
            print(f"\nDimensions appearing in ALL successful briefs:")
            for dim in campaign_dict['summary']['dimensions_appearing_in_all_briefs']:
                print(f"  • {dim}")
        
        print(f"\nTop 10 most common dimensions:")
        for dim, freq in campaign_dict['summary']['most_common_dimensions']:
            print(f"  • {dim}: appears in {freq}/{campaign_dict['summary']['successful_briefs']} briefs")

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
        brief_names_str = "_".join(campaign_dict['metadata']['brief_names'][:3])  # Limit to first 3 names
        if len(campaign_dict['metadata']['brief_names']) > 3:
            brief_names_str += f"_and_{len(campaign_dict['metadata']['brief_names']) - 3}_more"
        output_filename = f"Brief_Dimension_Generation/dimensions_{brief_names_str}.json"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(campaign_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_filename}")
    return output_filename

def main(brief_names: List[str] = None, brief_folder: str = "files/brief") -> Dict[str, Any]:
    """
    Main function to extract dimensions from specified briefs
    
    Args:
        brief_names: List of brief names to process (if None, processes all available)
        brief_folder: Path to brief folder
    
    Returns:
        Dictionary containing all extraction results
    """
    print("Starting Brief Dimension Extraction Pipeline...")
    
    try:
        # List available briefs first
        print("\nAvailable brief files:")
        list_available_briefs(brief_folder)
        
        # Process briefs
        if brief_names is None:
            print("\nProcessing all available briefs...")
            campaign_dict = process_all_available_briefs(brief_folder)
        else:
            campaign_dict = process_briefs(brief_names, brief_folder)
        
        # Display results
        print_results(campaign_dict)
        
        # Save results
        output_file = save_results(campaign_dict)
        
        print(f"\n✅ Pipeline completed successfully!")
        print(f"📊 Results saved to: {output_file}")
        
        return campaign_dict
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        raise

# Example usage and testing functions
def example_usage():
    """
    Example usage of the Brief Dimension Generation system
    """
    print("=== Brief Dimension Generation Example ===\n")
    
    # Example 1: Process specific briefs
    print("Example 1: Processing specific briefs")
    try:
        results1 = main(['abc_china_prompt', 'ai_prompt_for_poland'])
        print(f"Processed {results1['summary']['successful_briefs']} briefs successfully\n")
    except Exception as e:
        print(f"Example 1 failed: {e}\n")
    
    # Example 2: Process all available briefs
    print("Example 2: Processing all available briefs")
    try:
        results2 = main()  # Process all available briefs
        print(f"Processed {results2['summary']['successful_briefs']} briefs successfully\n")
    except Exception as e:
        print(f"Example 2 failed: {e}\n")

if __name__ == "__main__":
    # Run example usage
    example_usage()