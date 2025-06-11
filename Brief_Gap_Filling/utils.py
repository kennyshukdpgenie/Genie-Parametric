import json
import os
import sys
import random
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Add parent directory to path to import from root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_brandworld_distinct_words(distinct_words_file_path: str) -> Dict[str, Any]:
    """
    Load brandworld distinct words JSON file (Tarik's simplified approach)
    
    Args:
        distinct_words_file_path: Path to the brandworld distinct words JSON file
    
    Returns:
        Dictionary containing the distinct words data
    """
    if not os.path.exists(distinct_words_file_path):
        raise FileNotFoundError(f"Brandworld distinct words file not found: {distinct_words_file_path}")
    
    with open(distinct_words_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_legacy_brandworld_analysis(analysis_file_path: str) -> Dict[str, Any]:
    """
    Load legacy brandworld TF-IDF analysis JSON file (for backward compatibility)
    
    Args:
        analysis_file_path: Path to the brandworld analysis JSON file
    
    Returns:
        Dictionary containing the analysis data
    """
    if not os.path.exists(analysis_file_path):
        raise FileNotFoundError(f"Brandworld analysis file not found: {analysis_file_path}")
    
    with open(analysis_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_dimensions_with_deepseek(brief_text: str, dimension_list: List[str], deepseek_chat_func) -> Dict[str, str]:
    """
    Use DeepSeek to extract dimension values from brief text
    
    Args:
        brief_text: The plain text brief
        dimension_list: List of dimensions to extract
        deepseek_chat_func: The deepseek_chat function
    
    Returns:
        Dictionary with dimension -> value mappings
    """
    print("Extracting dimensions using DeepSeek...")
    
    # Create a comprehensive prompt for dimension extraction
    dimensions_str = "\n".join([f"- {dim}" for dim in dimension_list])
    
    system_prompt = f"""
You are an expert marketing brief analyzer. Extract specific information for each dimension from the provided brief text.

For each of the following dimensions, provide the relevant information found in the brief. If a dimension is not explicitly mentioned or cannot be inferred from the brief, leave it empty.

Dimensions to extract:
{dimensions_str}

Return your response as a valid JSON object with dimension names as keys and extracted values as strings. Use empty string "" for dimensions that cannot be filled from the brief.

Example format:
{{
    "Campaign Theme": "extracted theme here",
    "Marketing Objectives": "extracted objectives here",
    "Target Audience": "",
    ...
}}
"""
    
    message = f"{system_prompt}\n\nBrief text:\n{brief_text}"
    
    try:
        response = deepseek_chat_func(message)
        # Clean the response to extract JSON
        clean_response = response.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:]
        if clean_response.endswith('```'):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()
        
        extracted_data = json.loads(clean_response)
        
        # Ensure all dimensions are present in the response
        result = {}
        for dim in dimension_list:
            result[dim] = extracted_data.get(dim, "")
        
        print(f"Successfully extracted data for {len([v for v in result.values() if v.strip()])} dimensions")
        return result
        
    except Exception as e:
        print(f"Error extracting dimensions with DeepSeek: {e}")
        # Return empty dict if extraction fails
        return {dim: "" for dim in dimension_list}

def fill_gap_with_distinct_words(dimension_name: str, 
                                distinct_words: List[str], 
                                context_dimensions: Dict[str, str],
                                deepseek_chat_func) -> Dict[str, Any]:
    """
    Fill a missing dimension using distinct words from Brand_World (Tarik's approach)
    
    Args:
        dimension_name: Name of the dimension to fill
        distinct_words: List of distinct words from brand analysis
        context_dimensions: Other filled dimensions for context
        deepseek_chat_func: The deepseek_chat function
    
    Returns:
        Dictionary with filled value and metadata
    """
    from prompts import dimension_gap_filling_prompt
    
    # Prepare context information
    context_str = ""
    for dim, value in context_dimensions.items():
        if value.strip():
            context_str += f"- {dim}: {value}\n"
    
    # Sample relevant words (limit to 20-30 words for efficiency)
    sample_size = min(30, len(distinct_words))
    sampled_words = random.sample(distinct_words, sample_size) if len(distinct_words) > sample_size else distinct_words
    words_str = ", ".join(sampled_words)
    
    message = f"""{dimension_gap_filling_prompt}

DIMENSION TO FILL: {dimension_name}

AVAILABLE BRAND WORDS: {words_str}

CONTEXT FROM OTHER DIMENSIONS:
{context_str}

Please provide a meaningful fill-in for the dimension "{dimension_name}" using words from the brand vocabulary list."""

    try:
        response = deepseek_chat_func(message)
        # Clean the response to extract JSON
        clean_response = response.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:]
        if clean_response.endswith('```'):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()
        
        result = json.loads(clean_response)
        
        # Validate the response structure
        if not all(key in result for key in ['filled_value', 'words_used_from_list', 'reasoning']):
            raise ValueError("Response missing required keys")
        
        return result
        
    except Exception as e:
        print(f"Error filling gap for dimension '{dimension_name}': {e}")
        # Fallback: randomly select 2-3 words
        fallback_words = random.sample(sampled_words, min(3, len(sampled_words)))
        return {
            'filled_value': " ".join(fallback_words),
            'words_used_from_list': fallback_words,
            'reasoning': f"Fallback fill due to API error: {str(e)}"
        }

def fill_missing_dimensions_with_distinct_words(extracted_data: Dict[str, str], 
                                              distinct_words_data: Dict[str, Any],
                                              dimension_list: List[str],
                                              deepseek_chat_func) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """
    Fill missing dimensions using distinct words from Brand_World (Tarik's approach)
    
    Args:
        extracted_data: Data extracted from DeepSeek
        distinct_words_data: Distinct words data from Brand_World
        dimension_list: List of all dimensions
        deepseek_chat_func: The deepseek_chat function
    
    Returns:
        Tuple of (filled_data, source_tracking)
    """
    print("Filling missing dimensions using distinct words from Brand_World...")
    
    filled_data = {}
    source_tracking = {}
    
    # Get distinct words list
    distinct_words = distinct_words_data.get('distinct_words', [])
    
    if not distinct_words:
        print("⚠️  No distinct words found in Brand_World data")
        return extracted_data, {dim: "no_brandworld_data" for dim in dimension_list}
    
    print(f"Using {len(distinct_words)} distinct words from Brand_World")
    
    # Identify missing dimensions
    missing_dimensions = []
    for dimension in dimension_list:
        extracted_value = extracted_data.get(dimension, "").strip()
        if extracted_value:
            filled_data[dimension] = extracted_value
            source_tracking[dimension] = "deepseek_extraction"
        else:
            missing_dimensions.append(dimension)
    
    print(f"Found {len(missing_dimensions)} missing dimensions to fill")
    
    # Fill missing dimensions using distinct words
    for dimension in missing_dimensions:
        print(f"Filling dimension: {dimension}")
        
        try:
            # Get context from already filled dimensions
            context_dimensions = {k: v for k, v in filled_data.items() if v.strip()}
            
            # Fill the gap using distinct words
            fill_result = fill_gap_with_distinct_words(
                dimension, distinct_words, context_dimensions, deepseek_chat_func
            )
            
            filled_data[dimension] = fill_result['filled_value']
            source_tracking[dimension] = "brandworld_distinct_words"
            
            print(f"  ✅ Filled '{dimension}' with: '{fill_result['filled_value']}'")
            print(f"  📝 Used words: {fill_result['words_used_from_list']}")
            
        except Exception as e:
            print(f"  ❌ Failed to fill '{dimension}': {e}")
            filled_data[dimension] = ""
            source_tracking[dimension] = "fill_failed"
    
    # Final statistics
    filled_count = len([v for v in filled_data.values() if v.strip()])
    deepseek_count = len([s for s in source_tracking.values() if s == "deepseek_extraction"])
    brandworld_count = len([s for s in source_tracking.values() if s == "brandworld_distinct_words"])
    
    print(f"\n📊 Gap Filling Results:")
    print(f"  ✅ Total filled: {filled_count}/{len(dimension_list)} dimensions")
    print(f"  🤖 From DeepSeek: {deepseek_count}")
    print(f"  📚 From Brand_World: {brandworld_count}")
    print(f"  ❌ No data: {len(dimension_list) - filled_count}")
    
    return filled_data, source_tracking

def select_words_by_probability(probability_distribution: Dict[str, float], num_words: int = 5) -> List[str]:
    """
    Select words based on probability distribution (Legacy function for backward compatibility)
    
    Args:
        probability_distribution: Dictionary of word -> probability
        num_words: Number of words to select
    
    Returns:
        List of selected words
    """
    if not probability_distribution:
        return []
    
    words = list(probability_distribution.keys())
    probabilities = list(probability_distribution.values())
    
    # Select words based on probability distribution
    try:
        selected_words = random.choices(words, weights=probabilities, k=min(num_words, len(words)))
        return selected_words
    except Exception as e:
        print(f"Error selecting words by probability: {e}")
        # Fallback to random selection
        return random.sample(words, min(num_words, len(words)))

def fill_missing_dimensions_legacy(extracted_data: Dict[str, str], 
                                 brandworld_analysis: Dict[str, Any],
                                 dimension_list: List[str]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """
    Fill missing dimensions using legacy brandworld analysis data (for backward compatibility)
    
    Args:
        extracted_data: Data extracted from DeepSeek
        brandworld_analysis: Brandworld TF-IDF analysis data
        dimension_list: List of all dimensions
    
    Returns:
        Tuple of (filled_data, source_tracking)
    """
    print("Filling missing dimensions using legacy brandworld analysis...")
    
    filled_data = {}
    source_tracking = {}
    
    # Get analysis data (support both TF-IDF and frequency analysis structures)
    analysis_data = brandworld_analysis.get('tfidf_analysis', {})
    if not analysis_data:
        analysis_data = brandworld_analysis.get('frequency_analysis', {})
    
    for dimension in dimension_list:
        extracted_value = extracted_data.get(dimension, "").strip()
        
        if extracted_value:
            # Use value from DeepSeek extraction
            filled_data[dimension] = extracted_value
            source_tracking[dimension] = "deepseek_extraction"
        else:
            # Try to fill from brandworld analysis
            if dimension in analysis_data:
                dim_analysis = analysis_data[dimension]
                
                # Support both TF-IDF and frequency analysis structures
                probability_dist = dim_analysis.get('probability_distribution', {})
                
                if probability_dist:
                    selected_words = select_words_by_probability(probability_dist, 5)
                    filled_data[dimension] = ", ".join(selected_words)
                    source_tracking[dimension] = "brandworld_probability"
                else:
                    filled_data[dimension] = ""
                    source_tracking[dimension] = "no_data_available"
            else:
                filled_data[dimension] = ""
                source_tracking[dimension] = "dimension_not_in_brandworld"
    
    filled_count = len([v for v in filled_data.values() if v.strip()])
    deepseek_count = len([s for s in source_tracking.values() if s == "deepseek_extraction"])
    brandworld_count = len([s for s in source_tracking.values() if s == "brandworld_probability"])
    
    print(f"Filled {filled_count}/{len(dimension_list)} dimensions:")
    print(f"  - From DeepSeek: {deepseek_count}")
    print(f"  - From Brandworld: {brandworld_count}")
    print(f"  - No data: {len(dimension_list) - filled_count}")
    
    return filled_data, source_tracking

def create_gap_filling_table(brief_text: str, 
                           dimension_list: List[str], 
                           brandworld_file_path: str,
                           deepseek_chat_func,
                           use_distinct_words: bool = True) -> Dict[str, Any]:
    """
    Main function to create gap-filled table for brief dimensions
    
    Args:
        brief_text: Plain text brief content
        dimension_list: List of dimensions to extract/fill
        brandworld_file_path: Path to brandworld file (distinct words or legacy analysis)
        deepseek_chat_func: The deepseek_chat function
        use_distinct_words: Whether to use Tarik's distinct words approach (default: True)
    
    Returns:
        Dictionary containing the filled table and metadata
    """
    print("="*60)
    print("BRIEF GAP FILLING PIPELINE")
    print("="*60)
    
    try:
        # Determine file type and load accordingly
        if use_distinct_words and 'distinct_words' in brandworld_file_path:
            print(f"Using Tarik's distinct words approach")
            print(f"Loading distinct words from: {brandworld_file_path}")
            brandworld_data = load_brandworld_distinct_words(brandworld_file_path)
            approach = "distinct_words"
        else:
            print(f"Using legacy TF-IDF approach")
            print(f"Loading brandworld analysis from: {brandworld_file_path}")
            brandworld_data = load_legacy_brandworld_analysis(brandworld_file_path)
            approach = "legacy_tfidf"
        
        # Extract dimensions using DeepSeek
        extracted_data = extract_dimensions_with_deepseek(brief_text, dimension_list, deepseek_chat_func)
        
        # Fill missing dimensions based on approach
        if approach == "distinct_words":
            filled_data, source_tracking = fill_missing_dimensions_with_distinct_words(
                extracted_data, brandworld_data, dimension_list, deepseek_chat_func
            )
        else:
            filled_data, source_tracking = fill_missing_dimensions_legacy(
                extracted_data, brandworld_data, dimension_list
            )
        
        # Create result object
        result = {
            'filled_table': filled_data,
            'source_tracking': source_tracking,
            'metadata': {
                'brief_text': brief_text[:200] + "..." if len(brief_text) > 200 else brief_text,
                'dimension_count': len(dimension_list),
                'filled_count': len([v for v in filled_data.values() if v.strip()]),
                'extraction_timestamp': datetime.now().isoformat(),
                'brandworld_file': brandworld_file_path,
                'approach_used': approach,
                'gap_filling_method': "Tarik's distinct words" if approach == "distinct_words" else "Legacy TF-IDF"
            }
        }
        
        print(f"\n✅ Gap filling completed using {result['metadata']['gap_filling_method']} approach")
        return result
        
    except Exception as e:
        print(f"❌ Error in gap filling pipeline: {e}")
        # Return empty result on failure
        return {
            'filled_table': {dim: "" for dim in dimension_list},
            'source_tracking': {dim: "pipeline_failed" for dim in dimension_list},
            'metadata': {
                'error': str(e),
                'extraction_timestamp': datetime.now().isoformat(),
                'brandworld_file': brandworld_file_path,
                'approach_used': "failed"
            }
        }

def print_gap_filling_results(result: Dict[str, Any]) -> None:
    """
    Print formatted results of gap filling process
    
    Args:
        result: Result dictionary from create_gap_filling_table
    """
    print("\n" + "="*60)
    print("GAP FILLING RESULTS")
    print("="*60)
    
    metadata = result['metadata']
    analysis = result['filled_table']
    source_tracking = result['source_tracking']
    
    print(f"\nProcessing Summary:")
    print(f"  Brief length: {len(metadata.get('brief_text', ''))} characters")
    print(f"  Total dimensions: {metadata['dimension_count']}")
    print(f"  Brandworld source: {os.path.basename(metadata['brandworld_file'])}")
    print(f"  Gap filling method: {metadata['gap_filling_method']}")
    
    # Calculate statistics
    deepseek_count = len([s for s in source_tracking.values() if s == "deepseek_extraction"])
    brandworld_count = len([s for s in source_tracking.values() if s in ["brandworld_distinct_words", "brandworld_probability"]])
    total_filled = len([v for v in analysis.values() if v.strip()])
    
    print(f"\nFilling Summary:")
    print(f"  🤖 DeepSeek filled: {deepseek_count}")
    print(f"  📚 Brand_World filled: {brandworld_count}")
    print(f"  ❌ No data available: {len(analysis) - total_filled}")
    print(f"  ✅ Total filled: {total_filled}/{len(analysis)}")
    
    print(f"\nDimensions with Data ({total_filled}):")
    for dim, value in analysis.items():
        if value.strip():
            source = source_tracking[dim]
            if source == "deepseek_extraction":
                source_label = "🤖 DeepSeek"
            elif source in ["brandworld_distinct_words", "brandworld_probability"]:
                source_label = "📚 Brand_World"
            else:
                source_label = "❓ Other"
            print(f"  {source_label} {dim}: {value[:100]}{'...' if len(value) > 100 else ''}")
    
    empty_count = len([v for v in analysis.values() if not v.strip()])
    if empty_count > 0:
        print(f"\nEmpty Dimensions ({empty_count}):")
        for dim, value in analysis.items():
            if not value.strip():
                print(f"  ❌ {dim}")

def save_gap_filling_results(result: Dict[str, Any], output_filename: str = None) -> str:
    """
    Save gap filling results to JSON file
    
    Args:
        result: Result dictionary from create_gap_filling_table
        output_filename: Custom output filename (optional)
    
    Returns:
        Path to saved file
    """
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"Brief_Gap_Filling/gap_filled_brief_{timestamp}.json"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nGap filling results saved to: {output_filename}")
    return output_filename

def main(brief_text: str, 
         dimension_list: List[str], 
         brandworld_file_path: str,
         deepseek_chat_func,
         output_filename: str = None,
         use_distinct_words: bool = True) -> Dict[str, Any]:
    """
    Main entry point for brief gap filling (Tarik's distinct words approach)
    
    Args:
        brief_text: Plain text brief content
        dimension_list: List of dimensions to extract/fill
        brandworld_file_path: Path to brandworld file (distinct words or legacy analysis)
        deepseek_chat_func: The deepseek_chat function
        output_filename: Custom output filename (optional)
        use_distinct_words: Whether to use Tarik's distinct words approach (default: True)
    
    Returns:
        Dictionary containing all results
    """
    try:
        # Create gap-filled table with the specified approach
        result = create_gap_filling_table(
            brief_text, dimension_list, brandworld_file_path, deepseek_chat_func, use_distinct_words
        )
        
        # Print results
        print_gap_filling_results(result)
        
        # Save results
        output_path = save_gap_filling_results(result, output_filename)
        
        return result
        
    except Exception as e:
        print(f"Error in main gap filling process: {e}")
        raise

def evaluate_dimension_fill(dimension_name: str, 
                          fill_value: str, 
                          all_dimension_values: Dict[str, str],
                          deepseek_chat_func) -> Dict[str, Any]:
    """
    Evaluate a single dimension fill-in value using DeepSeek
    
    Args:
        dimension_name: Name of the dimension being evaluated
        fill_value: The fill-in value to evaluate
        all_dimension_values: Dictionary of all dimension values in the same row
        deepseek_chat_func: The deepseek_chat function
    
    Returns:
        Dictionary containing evaluation scores and reasoning
    """
    # Import the evaluation prompt
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from prompts import dimension_evaluation_prompt
    
    # Prepare the evaluation message
    other_values_str = "\n".join([
        f"- {dim}: {val}" for dim, val in all_dimension_values.items() 
        if dim != dimension_name and val.strip()
    ])
    
    message = f"""{dimension_evaluation_prompt}

DIMENSION TO EVALUATE:
Dimension Name: {dimension_name}
Fill-in Value: {fill_value}

OTHER DIMENSION VALUES IN THE SAME ROW:
{other_values_str}
"""
    
    try:
        response = deepseek_chat_func(message)
        # Clean the response to extract JSON
        clean_response = response.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:]
        if clean_response.endswith('```'):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()
        
        evaluation_result = json.loads(clean_response)
        
        # Ensure all required fields are present
        required_fields = [
            'dimension_value_match_score', 
            'context_coherence_score',
            'dimension_value_match_reasoning',
            'context_coherence_reasoning'
        ]
        
        for field in required_fields:
            if field not in evaluation_result:
                evaluation_result[field] = 0 if 'score' in field else "Evaluation failed"
        
        return evaluation_result
        
    except Exception as e:
        print(f"Error evaluating dimension {dimension_name}: {e}")
        return {
            'dimension_value_match_score': 0,
            'context_coherence_score': 0,
            'dimension_value_match_reasoning': f"Evaluation error: {str(e)}",
            'context_coherence_reasoning': f"Evaluation error: {str(e)}"
        }

def create_multiple_gap_filled_versions(brief_text: str, 
                                      dimension_list: List[str], 
                                      brandworld_file_path: str,
                                      deepseek_chat_func,
                                      n_versions: int = 5) -> List[Dict[str, Any]]:
    """
    Create N different versions of gap-filled tables for evaluation
    
    Args:
        brief_text: Plain text brief content
        dimension_list: List of dimensions to extract/fill
        brandworld_file_path: Path to brandworld file (distinct words or legacy analysis)
        deepseek_chat_func: The deepseek_chat function
        n_versions: Number of versions to generate
    
    Returns:
        List of gap-filled results
    """
    print(f"\n🔄 Creating {n_versions} gap-filled versions for evaluation...")
    
    versions = []
    for i in range(n_versions):
        print(f"  Generating version {i+1}/{n_versions}...")
        try:
            # Set different random seed for each version to ensure variation
            random.seed(i * 42)  # Different seed for each iteration
            
            version_result = create_gap_filling_table(
                brief_text, dimension_list, brandworld_file_path, deepseek_chat_func
            )
            
            # Add version identifier
            version_result['version_id'] = i + 1
            versions.append(version_result)
            
        except Exception as e:
            print(f"    ❌ Error creating version {i+1}: {e}")
            continue
    
    print(f"✅ Successfully created {len(versions)} versions")
    return versions

def evaluate_gap_filled_versions(versions: List[Dict[str, Any]], 
                               deepseek_chat_func) -> List[Dict[str, Any]]:
    """
    Evaluate multiple gap-filled versions and rank them
    
    Args:
        versions: List of gap-filled results to evaluate
        deepseek_chat_func: The deepseek_chat function
    
    Returns:
        List of evaluated and scored versions, sorted by total score
    """
    print(f"\n📊 Evaluating {len(versions)} gap-filled versions...")
    
    evaluated_versions = []
    
    for version in versions:
        print(f"  Evaluating version {version['version_id']}...")
        
        filled_dimensions = version['filled_table']
        dimension_evaluations = {}
        total_dimension_score = 0
        total_coherence_score = 0
        total_dimensions_evaluated = 0
        
        # Evaluate each filled dimension
        for dim_name, dim_value in filled_dimensions.items():
            if dim_value.strip():  # Only evaluate non-empty dimensions
                evaluation = evaluate_dimension_fill(
                    dim_name, dim_value, filled_dimensions, deepseek_chat_func
                )
                
                dimension_evaluations[dim_name] = evaluation
                total_dimension_score += evaluation.get('dimension_value_match_score', 0)
                total_coherence_score += evaluation.get('context_coherence_score', 0)
                total_dimensions_evaluated += 1
        
        # Calculate average scores
        avg_dimension_score = total_dimension_score / max(total_dimensions_evaluated, 1)
        avg_coherence_score = total_coherence_score / max(total_dimensions_evaluated, 1)
        total_score = avg_dimension_score + avg_coherence_score
        
        # Add evaluation results to version
        version['evaluation'] = {
            'dimension_evaluations': dimension_evaluations,
            'summary_scores': {
                'average_dimension_match_score': round(avg_dimension_score, 2),
                'average_coherence_score': round(avg_coherence_score, 2),
                'total_score': round(total_score, 2),
                'dimensions_evaluated': total_dimensions_evaluated
            }
        }
        
        evaluated_versions.append(version)
        print(f"    Version {version['version_id']} - Total Score: {total_score:.2f}")
    
    # Sort by total score (highest first)
    evaluated_versions.sort(key=lambda x: x['evaluation']['summary_scores']['total_score'], reverse=True)
    
    print(f"\n🏆 Evaluation complete! Top scores:")
    for i, version in enumerate(evaluated_versions[:3]):
        score = version['evaluation']['summary_scores']['total_score']
        print(f"  {i+1}. Version {version['version_id']}: {score:.2f}")
    
    return evaluated_versions

def save_top_evaluated_results(evaluated_versions: List[Dict[str, Any]], 
                             brief_name: str = "unknown",
                             top_n: int = 3) -> List[str]:
    """
    Save the top N evaluated results as JSON files
    
    Args:
        evaluated_versions: List of evaluated versions (sorted by score)
        brief_name: Name of the brief for filename
        top_n: Number of top results to save
    
    Returns:
        List of saved file paths
    """
    print(f"\n💾 Saving top {top_n} evaluated results...")
    
    saved_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, version in enumerate(evaluated_versions[:top_n]):
        rank = i + 1
        version_id = version['version_id']
        score = version['evaluation']['summary_scores']['total_score']
        
        filename = f"Brief_Gap_Filling/top_{rank}_{brief_name}_v{version_id}_score{score:.1f}_{timestamp}.json"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(version, f, indent=2, ensure_ascii=False)
        
        saved_files.append(filename)
        print(f"  {rank}. Saved version {version_id} (score: {score:.2f}) to: {os.path.basename(filename)}")
    
    return saved_files

def gap_fill_with_evaluation(brief_text: str, 
                           dimension_list: List[str], 
                           brandworld_file_path: str,
                           deepseek_chat_func,
                           n_versions: int = 5,
                           brief_name: str = "unknown") -> Dict[str, Any]:
    """
    Complete gap filling pipeline with multiple versions and evaluation
    
    Args:
        brief_text: Plain text brief content
        dimension_list: List of dimensions to extract/fill
        brandworld_file_path: Path to brandworld file (distinct words or legacy analysis)
        deepseek_chat_func: The deepseek_chat function
        n_versions: Number of versions to generate and evaluate
        brief_name: Name of the brief for saving files
    
    Returns:
        Dictionary containing all results and evaluation data
    """
    print("="*80)
    print("ENHANCED GAP FILLING WITH EVALUATION PIPELINE")
    print("="*80)
    
    try:
        # Step 1: Create multiple versions
        versions = create_multiple_gap_filled_versions(
            brief_text, dimension_list, brandworld_file_path, deepseek_chat_func, n_versions
        )
        
        if not versions:
            raise ValueError("No gap-filled versions were successfully created")
        
        # Step 2: Evaluate all versions
        evaluated_versions = evaluate_gap_filled_versions(versions, deepseek_chat_func)
        
        # Step 3: Save top 3 results
        saved_files = save_top_evaluated_results(evaluated_versions, brief_name)
        
        # Prepare comprehensive result
        result = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'brief_name': brief_name,
                'brief_length': len(brief_text),
                'total_dimensions': len(dimension_list),
                'versions_generated': len(versions),
                'versions_evaluated': len(evaluated_versions),
                'brandworld_file': brandworld_file_path
            },
            'brief_content': brief_text,
            'dimension_list': dimension_list,
            'all_evaluated_versions': evaluated_versions,
            'top_3_versions': evaluated_versions[:3],
            'saved_files': saved_files,
            'evaluation_summary': {
                'best_score': evaluated_versions[0]['evaluation']['summary_scores']['total_score'] if evaluated_versions else 0,
                'worst_score': evaluated_versions[-1]['evaluation']['summary_scores']['total_score'] if evaluated_versions else 0,
                'average_score': sum(v['evaluation']['summary_scores']['total_score'] for v in evaluated_versions) / len(evaluated_versions) if evaluated_versions else 0
            }
        }
        
        print(f"\n🎉 Enhanced gap filling complete!")
        print(f"📊 Generated {len(versions)} versions, evaluated {len(evaluated_versions)}")
        print(f"💾 Saved top 3 results to {len(saved_files)} files")
        print(f"🏆 Best score: {result['evaluation_summary']['best_score']:.2f}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in enhanced gap filling pipeline: {e}")
        raise

if __name__ == "__main__":
    # Import deepseek_chat for standalone execution
    try:
        from utils import deepseek_chat
    except ImportError:
        print("❌ Could not import deepseek_chat. Make sure you're running from the correct directory.")
        sys.exit(1)
    
    # Example usage
    sample_brief = """
    Campaign for Skrewball Whiskey targeting young adults who love adventure and unique experiences.
    The campaign should be playful and mischievous, encouraging people to try something different.
    Focus on the peanut butter whiskey's unique flavor and the brand's rebellious spirit.
    """
    
    sample_dimensions = [
        'Campaign Theme',
        'Marketing Objectives',
        'Target Audience (Strategic Segment)',
        'Tone of Voice',
        'Brand Context/Heritage'
    ]
    
    brandworld_path = "Brand_World/Skrewball Brand World_analysis.json"
    
    if os.path.exists(brandworld_path):
        result = main(sample_brief, sample_dimensions, brandworld_path, deepseek_chat)
        print("\n✅ Gap filling completed successfully!")
    else:
        print(f"❌ Brandworld analysis file not found at: {brandworld_path}")
