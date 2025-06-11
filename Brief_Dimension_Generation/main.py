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

# Example usage and main execution
if __name__ == "__main__":
    # Display available briefs
    print("Brief Dimension Generation System")
    print("=" * 40)
    list_available_briefs()
    
    # Example: Process specific briefs (modify this list as needed)
    example_brief_names = ['abs_china']
    
    print(f"\nExample: Processing {len(example_brief_names)} briefs...")
    results = main(example_brief_names)
    
    # You can also call with different combinations:
    # results = main(['abs_valentine', 'abs_ocean_spray'])
    # results = main(['oaken_glow', 'abs_pride'])
    # results = main(list(AVAILABLE_BRIEFS.keys()))  # Process all briefs