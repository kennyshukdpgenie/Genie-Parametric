# Brief Gap Filling System

## Overview

The Brief Gap Filling system is designed to automatically fill missing marketing brief dimensions using a two-stage approach:

1. **Primary Stage (DeepSeek)**: Extract dimension values directly from the brief text using AI
2. **Secondary Stage (Brandworld)**: Fill remaining empty dimensions using probability-weighted word selection from brandworld analysis

## Features

- ✅ **Intelligent Extraction**: Uses DeepSeek AI to extract relevant information from briefs
- 🎯 **Probability-Based Filling**: Uses TF-IDF word probability distributions from brandworld analysis
- 📊 **Source Tracking**: Tracks whether each dimension was filled by DeepSeek or brandworld data
- 💾 **Comprehensive Output**: Saves detailed JSON results with metadata and analysis
- 🔄 **Flexible Input**: Works with any brief text and custom dimension lists

## System Architecture

```
Brief Text → DeepSeek API → Extracted Dimensions
                                     ↓
Missing Dimensions → Brandworld Analysis → Probability Selection → Final Output
```

## Key Components

### 1. Core Functions (`Brief_Gap_Filling/utils.py`)

- `main()`: Main entry point for gap filling process
- `extract_dimensions_with_deepseek()`: AI-powered dimension extraction
- `fill_missing_dimensions()`: Brandworld probability-based filling
- `create_gap_filling_table()`: Complete pipeline orchestration

### 2. Integration (`Brief_Gap_Filling/main.py`)

- `gap_fill_brief()`: Process single brief from available collection
- `compare_briefs_with_gap_filling()`: Compare multiple briefs with gap filling

### 3. Test Scripts

- `test_gap_filling.py`: Comprehensive brief test
- `test_minimal_brief.py`: Minimal brief to demonstrate brandworld filling

## Usage Examples

### Basic Usage

```python
from Brief_Gap_Filling.utils import main
from utils import deepseek_chat

# Your brief text
brief_text = "Create a fun whiskey campaign for young adults..."

# Standard dimensions
dimensions = [
    'Campaign Theme',
    'Marketing Objectives',
    'Target Audience (Strategic Segment)',
    # ... add more dimensions
]

# Run gap filling
result = main(
    brief_text=brief_text,
    dimension_list=dimensions,
    brandworld_analysis_path="Brand_World/Skrewball Brand World_analysis.json",
    deepseek_chat_func=deepseek_chat
)
```

### Using Built-in Briefs

```python
from Brief_Gap_Filling.main import gap_fill_brief

# Process a specific brief
result = gap_fill_brief('ballantine_poland')

# Compare multiple briefs
comparison = compare_briefs_with_gap_filling(['abs_china', 'ballantine_poland'])
```

## Output Structure

The system produces comprehensive JSON output with the following structure:

```json
{
  "metadata": {
    "timestamp": "2025-01-07T...",
    "brief_length": 99,
    "total_dimensions": 15,
    "brandworld_source": "Skrewball Brand World_analysis.json",
    "extraction_summary": {
      "deepseek_filled": 3,
      "brandworld_filled": 8,
      "no_data": 4
    }
  },
  "filled_table": {
    "dimensions": {
      "Campaign Theme": "fun and playful",
      "Marketing Objectives": "glance, first, appetite, glance, first",
      // ... more dimensions
    },
    "sources": {
      "Campaign Theme": "deepseek_extraction",
      "Marketing Objectives": "brandworld_probability",
      // ... source tracking for each dimension
    }
  },
  "detailed_analysis": {
    "dimensions_with_data": ["Campaign Theme", "Marketing Objectives", ...],
    "empty_dimensions": ["Success Metrics (KPIs)", ...],
    "source_breakdown": {
      "deepseek_extraction": ["Campaign Theme", ...],
      "brandworld_probability": ["Marketing Objectives", ...],
      "no_data_available": ["Success Metrics (KPIs)", ...]
    }
  }
}
```

## Standard Dimensions

The system uses these 15 standard marketing brief dimensions:

1. **Campaign Theme**
2. **Marketing Objectives**
3. **Universal Consumer Challenge**
4. **Local Consumer Challenge (Market-Specific)**
5. **Brand Context/Heritage**
6. **Campaign Ambition/Scope**
7. **Target Audience (Strategic Segment)**
8. **Audience Demographics/Behavior**
9. **Single-Minded Message**
10. **Tone of Voice**
11. **Key Deliverables/Assets**
12. **Success Metrics (KPIs)**
13. **Mandatory Channels/Formats**
14. **Representation/Inclusivity Guidelines**
15. **Cultural Adaptation Requirements**

## Source Tracking

Each filled dimension is tagged with its source:

- 🤖 **`deepseek_extraction`**: Value extracted directly from brief by AI
- 🎯 **`brandworld_probability`**: Value generated from brandworld word probabilities
- ❌ **`no_data_available`**: No data available in either source
- ❌ **`dimension_not_in_brandworld`**: Dimension not present in brandworld analysis

## Performance Metrics

The system tracks several performance metrics:

- **Fill Rate**: Percentage of dimensions successfully filled
- **DeepSeek Success Rate**: Dimensions filled by AI extraction
- **Brandworld Coverage**: Dimensions filled by probability selection
- **Data Gaps**: Dimensions with no available data

## Example Results

### Comprehensive Brief (Ballantine Poland)
- 📊 **73.3% fill rate** (11/15 dimensions)
- 🤖 **11 dimensions** from DeepSeek
- 🎯 **0 dimensions** from brandworld (comprehensive brief)

### Minimal Brief
- 📊 **73.3% fill rate** (11/15 dimensions)  
- 🤖 **3 dimensions** from DeepSeek
- 🎯 **8 dimensions** from brandworld

## Requirements

- DeepSeek API access (configured in root `utils.py`)
- Brandworld analysis JSON file (from Brand_World system)
- Python packages: `json`, `os`, `sys`, `random`, `datetime`, `typing`

## File Outputs

All results are automatically saved to timestamped JSON files in the `Brief_Gap_Filling/` directory:

- `gap_filled_{brief_name}.json` - Individual brief results
- `test_ballantine_gap_filled.json` - Test results  
- `comparison_{brief1}_{brief2}.json` - Comparison results

## Integration with Existing Systems

The Brief Gap Filling system integrates seamlessly with:

- **Brand_World**: Uses TF-IDF analysis as probability source
- **Brief_Dimension_Generation**: Shares brief collection and dimension standards
- **Root Utils**: Uses `deepseek_chat` for AI processing

## Error Handling

The system includes robust error handling for:

- ❌ Missing brandworld analysis files
- ❌ DeepSeek API failures (returns empty dimensions)
- ❌ JSON parsing errors
- ❌ Invalid brief names
- ❌ Missing probability distributions

## Testing

Run the test scripts to verify functionality:

```bash
# Test comprehensive brief
python Brief_Gap_Filling/test_gap_filling.py

# Test minimal brief (demonstrates brandworld filling)
python Brief_Gap_Filling/test_minimal_brief.py
```

---

## Quick Start

1. Ensure you have a brandworld analysis file: `Brand_World/Skrewball Brand World_analysis.json`
2. Run a test: `python Brief_Gap_Filling/test_gap_filling.py`
3. Check the output JSON files for results
4. Integrate into your workflow using the provided functions

The system is designed to handle real-world scenarios where marketing briefs may be incomplete, providing intelligent gap filling based on both AI extraction and statistical probability distributions from successful brand examples. 