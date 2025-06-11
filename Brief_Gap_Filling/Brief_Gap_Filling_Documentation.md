# Brief Gap Filling System - Data Science Guide

## Table of Contents
1. [Overview & Architecture](#overview--architecture)
2. [Core Components](#core-components)
3. [Key Functions with Code Examples](#key-functions-with-code-examples)
4. [Enhanced Evaluation System](#enhanced-evaluation-system)
5. [Input/Output Data Formats](#inputoutput-data-formats)
6. [Testing & Validation](#testing--validation)
7. [Performance Metrics](#performance-metrics)
8. [Common Use Cases](#common-use-cases)
9. [Troubleshooting](#troubleshooting)

---

## Overview & Architecture

The Brief Gap Filling system is a **dual-stage intelligent completion system** for marketing briefs that combines AI extraction with probabilistic filling to ensure comprehensive dimension coverage.

### System Flow
```
Brief Text Input
      ↓
🤖 Stage 1: DeepSeek AI Extraction
      ↓
📊 Stage 2: Brandworld Probability Filling
      ↓
✅ Enhanced Evaluation (Optional)
      ↓
📁 JSON Output with Source Tracking
```

### Core Architecture Components

1. **AI Extraction Engine** (`extract_dimensions_with_deepseek`)
2. **Probability-Based Filling** (`fill_missing_dimensions`)
3. **Enhanced Evaluation System** (`evaluate_dimension_fill`)
4. **Version Generation & Ranking** (`create_multiple_gap_filled_versions`)

---

## Core Components

### 1. Main Processing Pipeline (`Brief_Gap_Filling/main.py`)

#### Key Classes & Functions:
- **`STANDARD_DIMENSIONS`**: 15 standardized marketing brief dimensions
- **`gap_fill_brief()`**: Single brief processing
- **`compare_briefs_with_gap_filling()`**: Multi-brief comparison
- **`gap_fill_brief_with_evaluation()`**: Enhanced processing with AI evaluation

### 2. Utility Functions (`Brief_Gap_Filling/utils.py`)

#### Core Processing Functions:
- **`create_gap_filling_table()`**: Main orchestration function
- **`extract_dimensions_with_deepseek()`**: AI-powered extraction
- **`fill_missing_dimensions()`**: Brandworld probability filling
- **`gap_fill_with_evaluation()`**: Enhanced pipeline with evaluation

---

## Key Functions with Code Examples

### 1. Basic Gap Filling Process

```python
from Brief_Gap_Filling.utils import main
from utils import deepseek_chat

# Standard dimension list
DIMENSIONS = [
    'Campaign Theme',
    'Marketing Objectives',
    'Universal Consumer Challenge',
    'Target Audience (Strategic Segment)',
    'Single-Minded Message',
    'Tone of Voice',
    # ... additional dimensions
]

def run_basic_gap_filling():
    """Basic gap filling example"""
    
    brief_text = """
    Create an engaging campaign for Ballantine's whiskey targeting young adults 
    in Poland. Focus on premium positioning and nightlife occasions.
    """
    
    result = main(
        brief_text=brief_text,
        dimension_list=DIMENSIONS,
        brandworld_analysis_path="files/brandword_distribution/dimensions_ballantine_poland.json",
        deepseek_chat_func=deepseek_chat,
        output_filename="my_gap_filled_brief.json"
    )
    
    return result
```

### 2. AI Extraction with DeepSeek

```python
def extract_dimensions_with_deepseek(brief_text: str, dimension_list: List[str], deepseek_chat_func) -> Dict[str, str]:
    """
    AI-powered dimension extraction using structured prompts
    """
    dimensions_str = "\n".join([f"- {dim}" for dim in dimension_list])
    
    system_prompt = f"""
You are an expert marketing brief analyzer. Extract specific information for each dimension.

Dimensions to extract:
{dimensions_str}

Return as JSON: {{"dimension": "extracted_value"}}
Use empty string "" for missing dimensions.
"""
    
    message = f"{system_prompt}\n\nBrief text:\n{brief_text}"
    
    try:
        response = deepseek_chat_func(message)
        # Clean and parse JSON response
        clean_response = response.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:-3]
        
        extracted_data = json.loads(clean_response)
        
        # Ensure all dimensions are present
        result = {dim: extracted_data.get(dim, "") for dim in dimension_list}
        
        print(f"✅ DeepSeek extracted {len([v for v in result.values() if v.strip()])} dimensions")
        return result
        
    except Exception as e:
        print(f"❌ DeepSeek extraction failed: {e}")
        return {dim: "" for dim in dimension_list}
```

### 3. Probability-Based Filling

```python
def fill_missing_dimensions(extracted_data: Dict[str, str], 
                          brandworld_analysis: Dict[str, Any],
                          dimension_list: List[str]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """
    Fill empty dimensions using brandworld probability distributions
    """
    filled_data = {}
    source_tracking = {}
    
    analysis_data = brandworld_analysis.get('tfidf_analysis', {})
    
    for dimension in dimension_list:
        extracted_value = extracted_data.get(dimension, "").strip()
        
        if extracted_value:
            # Use DeepSeek value
            filled_data[dimension] = extracted_value
            source_tracking[dimension] = "deepseek_extraction"
        else:
            # Try brandworld filling
            if dimension in analysis_data:
                dim_analysis = analysis_data[dimension]
                probability_dist = dim_analysis.get('probability_distribution', {})
                
                if probability_dist:
                    # Select words based on probability weights
                    selected_words = select_words_by_probability(probability_dist, 5)
                    filled_data[dimension] = ", ".join(selected_words)
                    source_tracking[dimension] = "brandworld_probability"
                else:
                    filled_data[dimension] = ""
                    source_tracking[dimension] = "no_data_available"
            else:
                filled_data[dimension] = ""
                source_tracking[dimension] = "dimension_not_in_brandworld"
    
    return filled_data, source_tracking
```

### 4. Probability-Weighted Word Selection

```python
def select_words_by_probability(probability_distribution: Dict[str, float], num_words: int = 5) -> List[str]:
    """
    Select words based on TF-IDF probability weights
    """
    if not probability_distribution:
        return []
    
    words = list(probability_distribution.keys())
    probabilities = list(probability_distribution.values())
    
    try:
        # Weighted random selection
        selected_words = random.choices(
            words, 
            weights=probabilities, 
            k=min(num_words, len(words))
        )
        return selected_words
    except Exception as e:
        print(f"❌ Probability selection failed: {e}")
        return random.sample(words, min(num_words, len(words)))
```

---

## Enhanced Evaluation System

### 1. Single Dimension Evaluation

```python
def evaluate_dimension_fill(dimension_name: str, 
                          fill_value: str, 
                          all_dimension_values: Dict[str, str],
                          deepseek_chat_func) -> Dict[str, Any]:
    """
    Evaluate quality of dimension filling using AI assessment
    """
    from prompts import dimension_evaluation_prompt
    
    # Create context from other dimensions
    context_dimensions = {k: v for k, v in all_dimension_values.items() 
                         if k != dimension_name and v.strip()}
    context_text = "\n".join([f"- {k}: {v}" for k, v in context_dimensions.items()])
    
    evaluation_message = f"""
{dimension_evaluation_prompt}

DIMENSION TO EVALUATE: {dimension_name}
FILL VALUE: "{fill_value}"

OTHER DIMENSIONS CONTEXT:
{context_text}
"""
    
    try:
        response = deepseek_chat_func(evaluation_message)
        # Parse evaluation response (expecting JSON with scores and reasoning)
        evaluation_data = json.loads(response.strip())
        
        return {
            'dimension': dimension_name,
            'fill_value': fill_value,
            'dimension_match_score': evaluation_data.get('dimension_match_score', 0),
            'context_coherence_score': evaluation_data.get('context_coherence_score', 0),
            'reasoning': evaluation_data.get('reasoning', ''),
            'total_score': evaluation_data.get('dimension_match_score', 0) + evaluation_data.get('context_coherence_score', 0)
        }
    except Exception as e:
        print(f"❌ Evaluation failed for {dimension_name}: {e}")
        return {
            'dimension': dimension_name,
            'fill_value': fill_value,
            'dimension_match_score': 0,
            'context_coherence_score': 0,
            'reasoning': f'Evaluation error: {e}',
            'total_score': 0
        }
```

### 2. Multi-Version Generation & Evaluation

```python
def create_multiple_gap_filled_versions(brief_text: str, 
                                      dimension_list: List[str], 
                                      brandworld_analysis_path: str,
                                      deepseek_chat_func,
                                      n_versions: int = 5) -> List[Dict[str, Any]]:
    """
    Generate multiple versions with different random seeds for comparison
    """
    print(f"🔄 Generating {n_versions} gap-filled versions...")
    
    versions = []
    for i in range(n_versions):
        # Set different random seed for each version
        random.seed(42 + i)  # Ensures reproducible but different results
        
        print(f"  Generating version {i+1}/{n_versions}...")
        
        version_result = create_gap_filling_table(
            brief_text=brief_text,
            dimension_list=dimension_list,
            brandworld_analysis_path=brandworld_analysis_path,
            deepseek_chat_func=deepseek_chat_func
        )
        
        # Add version metadata
        version_result['version_id'] = i + 1
        version_result['random_seed'] = 42 + i
        versions.append(version_result)
    
    return versions
```

### 3. Version Ranking & Selection

```python
def evaluate_gap_filled_versions(versions: List[Dict[str, Any]], 
                               deepseek_chat_func) -> List[Dict[str, Any]]:
    """
    Evaluate and rank multiple versions by quality scores
    """
    print(f"📊 Evaluating {len(versions)} versions...")
    
    evaluated_versions = []
    
    for i, version in enumerate(versions):
        print(f"  Evaluating version {i+1}...")
        
        filled_dimensions = version['filled_table']['dimensions']
        dimension_evaluations = []
        total_score = 0
        
        # Evaluate each filled dimension
        for dim_name, dim_value in filled_dimensions.items():
            if dim_value.strip():  # Only evaluate non-empty dimensions
                evaluation = evaluate_dimension_fill(
                    dimension_name=dim_name,
                    fill_value=dim_value,
                    all_dimension_values=filled_dimensions,
                    deepseek_chat_func=deepseek_chat_func
                )
                dimension_evaluations.append(evaluation)
                total_score += evaluation['total_score']
        
        # Calculate average score
        avg_score = total_score / len(dimension_evaluations) if dimension_evaluations else 0
        
        # Add evaluation metadata to version
        version['evaluation'] = {
            'total_score': total_score,
            'average_score': avg_score,
            'dimensions_evaluated': len(dimension_evaluations),
            'dimension_evaluations': dimension_evaluations,
            'evaluation_timestamp': datetime.now().isoformat()
        }
        
        evaluated_versions.append(version)
    
    # Sort by average score (descending)
    evaluated_versions.sort(key=lambda x: x['evaluation']['average_score'], reverse=True)
    
    print(f"✅ Evaluation complete. Best score: {evaluated_versions[0]['evaluation']['average_score']:.2f}")
    return evaluated_versions
```

---

## Input/Output Data Formats

### Input Requirements

#### 1. Brief Text
```python
brief_text = """
Create a premium whiskey campaign for Ballantine's targeting young professionals 
in Poland. Focus on sophisticated nightlife occasions and premium positioning.
The campaign should emphasize craft heritage and modern appeal.
"""
```

#### 2. Dimension List
```python
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
```

#### 3. Brandworld Analysis File Structure
```json
{
  "tfidf_analysis": {
    "Campaign Theme": {
      "probability_distribution": {
        "premium": 0.45,
        "sophisticated": 0.32,
        "heritage": 0.28,
        "modern": 0.25
      },
      "top_words": ["premium", "sophisticated", "heritage"],
      "total_documents": 156
    },
    "Marketing Objectives": {
      "probability_distribution": {
        "awareness": 0.38,
        "engagement": 0.35,
        "consideration": 0.31
      }
    }
  }
}
```

### Output Structure

#### Basic Gap Filling Output
```json
{
  "metadata": {
    "timestamp": "2025-01-08T10:23:45.123456",
    "brief_length": 234,
    "total_dimensions": 15,
    "brandworld_source": "dimensions_ballantine_poland.json",
    "extraction_summary": {
      "deepseek_filled": 8,
      "brandworld_filled": 5,
      "no_data": 2
    }
  },
  "filled_table": {
    "dimensions": {
      "Campaign Theme": "premium sophistication with modern appeal",
      "Marketing Objectives": "awareness, engagement, consideration",
      "Target Audience (Strategic Segment)": "young professionals aged 25-35"
    },
    "sources": {
      "Campaign Theme": "deepseek_extraction",
      "Marketing Objectives": "brandworld_probability",
      "Target Audience (Strategic Segment)": "deepseek_extraction"
    }
  },
  "detailed_analysis": {
    "dimensions_with_data": ["Campaign Theme", "Marketing Objectives"],
    "empty_dimensions": ["Success Metrics (KPIs)"],
    "source_breakdown": {
      "deepseek_extraction": ["Campaign Theme"],
      "brandworld_probability": ["Marketing Objectives"],
      "no_data_available": ["Success Metrics (KPIs)"]
    }
  }
}
```

#### Enhanced Evaluation Output
```json
{
  "evaluation": {
    "total_score": 87.5,
    "average_score": 8.75,
    "dimensions_evaluated": 10,
    "dimension_evaluations": [
      {
        "dimension": "Campaign Theme",
        "fill_value": "premium sophistication with modern appeal",
        "dimension_match_score": 5,
        "context_coherence_score": 4,
        "reasoning": "Strong alignment with dimension requirements...",
        "total_score": 9
      }
    ]
  }
}
```

---

## Testing & Validation

### 1. Basic Testing Script

```python
# test_basic_gap_filling.py
def test_basic_functionality():
    """Test basic gap filling functionality"""
    from Brief_Gap_Filling.utils import main
    from utils import deepseek_chat
    
    brief_text = "Create a fun whiskey campaign for young adults"
    
    result = main(
        brief_text=brief_text,
        dimension_list=['Campaign Theme', 'Target Audience (Strategic Segment)'],
        brandworld_analysis_path="files/brandword_distribution/dimensions_ballantine_poland.json",
        deepseek_chat_func=deepseek_chat
    )
    
    # Validate results
    assert 'filled_table' in result
    assert 'dimensions' in result['filled_table']
    assert 'sources' in result['filled_table']
    
    print("✅ Basic functionality test passed")
```

### 2. Enhanced Evaluation Testing

```python
# test_enhanced_evaluation.py
def test_enhanced_evaluation():
    """Test enhanced evaluation system"""
    from Brief_Gap_Filling.utils import gap_fill_with_evaluation
    from utils import deepseek_chat
    
    result = gap_fill_with_evaluation(
        brief_text="Premium whiskey campaign for young professionals",
        dimension_list=['Campaign Theme', 'Marketing Objectives'],
        brandworld_analysis_path="files/brandword_distribution/dimensions_ballantine_poland.json",
        deepseek_chat_func=deepseek_chat,
        n_versions=3,
        brief_name="test_brief"
    )
    
    # Validate evaluation results
    assert 'evaluation_summary' in result
    assert 'best_version' in result
    assert result['evaluation_summary']['versions_generated'] == 3
    
    print("✅ Enhanced evaluation test passed")
```

### 3. Performance Validation

```python
def validate_performance_metrics():
    """Validate system performance metrics"""
    
    # Test different brief sizes
    brief_sizes = [
        ("Short", "Create whiskey campaign"),
        ("Medium", "Create premium whiskey campaign for young professionals in Poland"),
        ("Long", """Develop comprehensive campaign for Ballantine's whiskey targeting 
                   young professionals aged 25-35 in Poland. Focus on premium positioning,
                   nightlife occasions, heritage storytelling, and modern appeal.""")
    ]
    
    for size_name, brief_text in brief_sizes:
        result = main(brief_text, STANDARD_DIMENSIONS, "path/to/analysis.json", deepseek_chat)
        
        fill_rate = len([v for v in result['filled_table']['dimensions'].values() if v.strip()]) / len(STANDARD_DIMENSIONS)
        print(f"{size_name} Brief - Fill Rate: {fill_rate:.1%}")
```

---

## Performance Metrics

### Key Performance Indicators

#### 1. Fill Rate Metrics
```python
def calculate_fill_rate(result: Dict[str, Any]) -> Dict[str, float]:
    """Calculate comprehensive fill rate metrics"""
    
    dimensions = result['filled_table']['dimensions']
    sources = result['filled_table']['sources']
    total_dims = len(dimensions)
    
    # Overall fill rate
    filled_dims = len([v for v in dimensions.values() if v.strip()])
    overall_fill_rate = filled_dims / total_dims
    
    # Source-specific fill rates
    deepseek_fills = len([s for s in sources.values() if s == "deepseek_extraction"])
    brandworld_fills = len([s for s in sources.values() if s == "brandworld_probability"])
    
    return {
        'overall_fill_rate': overall_fill_rate,
        'deepseek_success_rate': deepseek_fills / total_dims,
        'brandworld_success_rate': brandworld_fills / total_dims,
        'total_dimensions': total_dims,
        'filled_dimensions': filled_dims,
        'empty_dimensions': total_dims - filled_dims
    }
```

#### 2. Quality Metrics (Enhanced Evaluation)
```python
def calculate_quality_metrics(evaluation_data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate quality assessment metrics"""
    
    evaluations = evaluation_data['dimension_evaluations']
    
    if not evaluations:
        return {'average_score': 0, 'dimension_match_avg': 0, 'context_coherence_avg': 0}
    
    # Calculate averages
    total_score = sum(e['total_score'] for e in evaluations)
    dim_match_total = sum(e['dimension_match_score'] for e in evaluations)
    context_total = sum(e['context_coherence_score'] for e in evaluations)
    
    count = len(evaluations)
    
    return {
        'average_total_score': total_score / count,
        'dimension_match_avg': dim_match_total / count,
        'context_coherence_avg': context_total / count,
        'score_distribution': {
            'excellent (9-10)': len([e for e in evaluations if e['total_score'] >= 9]),
            'good (7-8)': len([e for e in evaluations if 7 <= e['total_score'] < 9]),
            'fair (5-6)': len([e for e in evaluations if 5 <= e['total_score'] < 7]),
            'poor (0-4)': len([e for e in evaluations if e['total_score'] < 5])
        }
    }
```

---

## Common Use Cases

### 1. Single Brief Processing

```python
def process_single_brief():
    """Process a single brief with standard dimensions"""
    from Brief_Gap_Filling.main import gap_fill_brief
    
    # Using built-in brief collection
    result = gap_fill_brief(
        brief_name='ballantine_poland',
        dimension_list=None,  # Uses STANDARD_DIMENSIONS
        brandworld_analysis_path=None  # Auto-detects path
    )
    
    print(f"Fill Rate: {result['metadata']['extraction_summary']['deepseek_filled']}/15")
    return result
```

### 2. Custom Brief with Enhanced Evaluation

```python
def process_custom_brief_with_evaluation():
    """Process custom brief with quality evaluation"""
    
    custom_brief = """
    Launch campaign for premium vodka brand targeting affluent millennials.
    Emphasize craft distillation and exclusive positioning.
    """
    
    result = gap_fill_with_evaluation(
        brief_text=custom_brief,
        dimension_list=STANDARD_DIMENSIONS,
        brandworld_analysis_path="Brand_World/vodka_analysis.json",
        deepseek_chat_func=deepseek_chat,
        n_versions=5,
        brief_name="premium_vodka_campaign"
    )
    
    # Access best performing version
    best_version = result['best_version']
    quality_score = best_version['evaluation']['average_score']
    
    print(f"Best Version Quality: {quality_score:.1f}/10.0")
    return result
```

### 3. Comparative Analysis

```python
def compare_multiple_briefs():
    """Compare gap filling performance across multiple briefs"""
    
    brief_names = ['abs_china', 'ballantine_poland', 'codigo']
    
    results = {}
    for brief_name in brief_names:
        result = gap_fill_brief(brief_name)
        
        # Calculate performance metrics
        fill_rate = calculate_fill_rate(result)
        results[brief_name] = {
            'fill_rate': fill_rate['overall_fill_rate'],
            'deepseek_success': fill_rate['deepseek_success_rate'],
            'brandworld_contribution': fill_rate['brandworld_success_rate']
        }
    
    # Display comparison
    for brief_name, metrics in results.items():
        print(f"{brief_name}: {metrics['fill_rate']:.1%} fill rate")
```

---

## Troubleshooting

### Common Issues & Solutions

#### 1. DeepSeek API Errors
```python
def handle_deepseek_errors():
    """Handle common DeepSeek API issues"""
    
    try:
        result = extract_dimensions_with_deepseek(brief_text, dimensions, deepseek_chat)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print("💡 Solution: Check DeepSeek response format")
        # Fallback to empty extraction
        result = {dim: "" for dim in dimensions}
    except Exception as e:
        print(f"❌ API error: {e}")
        print("💡 Solution: Check API key and network connectivity")
        result = {dim: "" for dim in dimensions}
    
    return result
```

#### 2. Brandworld Analysis File Issues
```python
def validate_brandworld_file(file_path: str) -> bool:
    """Validate brandworld analysis file structure"""
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Check required structure
        if 'tfidf_analysis' not in data:
            print("❌ Missing 'tfidf_analysis' key")
            return False
        
        # Check dimension structure
        for dim_name, dim_data in data['tfidf_analysis'].items():
            if 'probability_distribution' not in dim_data:
                print(f"❌ Missing probability_distribution for {dim_name}")
                return False
        
        print("✅ Brandworld file structure valid")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON format: {file_path}")
        return False
```

#### 3. Performance Optimization
```python
def optimize_processing():
    """Tips for optimizing processing performance"""
    
    # 1. Batch processing for multiple briefs
    brief_names = ['brief1', 'brief2', 'brief3']
    results = []
    
    for brief_name in brief_names:
        # Process with error handling
        try:
            result = gap_fill_brief(brief_name)
            results.append(result)
        except Exception as e:
            print(f"❌ Failed to process {brief_name}: {e}")
            continue
    
    # 2. Limit evaluation versions for faster processing
    result = gap_fill_with_evaluation(
        brief_text=brief_text,
        dimension_list=STANDARD_DIMENSIONS,
        n_versions=3,  # Reduce from default 5 for faster processing
        deepseek_chat_func=deepseek_chat
    )
    
    # 3. Use specific dimensions only
    key_dimensions = [
        'Campaign Theme',
        'Marketing Objectives', 
        'Target Audience (Strategic Segment)',
        'Single-Minded Message'
    ]
    
    result = gap_fill_brief(
        brief_name='ballantine_poland',
        dimension_list=key_dimensions  # Process only essential dimensions
    )
```

---

## Summary

The Brief Gap Filling system provides a robust, two-stage approach to completing marketing brief dimensions:

1. **🤖 AI Extraction**: DeepSeek API intelligently extracts relevant information from brief text
2. **📊 Probability Filling**: Brandworld TF-IDF analysis fills missing dimensions using weighted word selection
3. **✅ Quality Evaluation**: Enhanced evaluation system generates multiple versions and ranks by quality
4. **📁 Comprehensive Output**: Detailed JSON output with source tracking and performance metrics

### Key Benefits for Data Scientists:

- **Reproducible Results**: Controlled random seeds for consistent testing
- **Quality Metrics**: Comprehensive evaluation and ranking system  
- **Source Transparency**: Clear tracking of data sources (AI vs. probability-based)
- **Flexible Integration**: Works with any brief text and custom dimension lists
- **Performance Monitoring**: Built-in metrics for fill rates and quality assessment

The system is designed to handle real-world marketing brief scenarios while providing the transparency and control needed for data science applications. 