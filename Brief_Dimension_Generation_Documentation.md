# Brief Dimension Generation System
## Technical Documentation for Data Scientists

---

## 📋 **System Overview**

The Brief Dimension Generation system is an AI-powered pipeline that automatically extracts parametric dimensions from marketing briefs. It analyzes brief text content using DeepSeek AI to identify consistent, measurable parameters that can be used for comparative analysis across multiple marketing campaigns.

### **Core Purpose**
- Extract standardized dimensions from unstructured marketing brief texts
- Create consistent parametric frameworks for brief comparison
- Generate structured datasets for further analysis and modeling
- Enable data-driven insights across marketing campaign briefs

---

## 🏗️ **System Architecture**

```
Brief_Dimension_Generation/
├── main.py           # Core pipeline and orchestration
├── briefs.py         # Marketing brief text repository
└── __pycache__/      # Python cache files
```

### **External Dependencies**
- `prompts.py` (root) - AI prompt templates
- `utils.py` (root) - DeepSeek API integration

---

## 🔧 **Key Components Analysis**

### **1. AI Prompt System**

The system uses a specialized prompt to guide AI extraction:

```python
# From prompts.py
dimension_extraction_prompt = """
You are an expert in marketing analysis and parametric modeling. Below is a plain-text marketing brief. Your task is to analyze the content and extract a list of key parametric dimensions that define the structure of the brief. These dimensions will be used later to build a comparative table across multiple briefs (good and bad), so consistency and granularity are important.

Please follow these rules:
- Extract only the dimensions (i.e., column names) — do not return any values.
- Focus on identifying clear, consistently measurable or comparable parameters (e.g., type of shot, camera angle, background object, position etc.).
- Avoid vague or redundant terms; aim for a consistent level of abstraction.
- Pay Special attention to photographic terms like angles or type of shot
- Return the dimensions as a flat, bullet-point list in the order they appear logically in the brief.
- Include between 10–15 core dimensions, depending on content richness.
- only return the dimensions as a list in csv format where I will put it into a datatable later, no extra words
"""
```

**Key Design Principles:**
- ✅ **Consistency**: Ensures comparable dimensions across briefs
- ✅ **Granularity**: Focuses on measurable parameters
- ✅ **Structure**: Returns CSV format for easy processing
- ✅ **Domain Focus**: Emphasizes photographic and marketing terms

### **2. Brief Repository System**

The system maintains a curated collection of marketing briefs:

```python
# From Brief_Dimension_Generation/main.py
AVAILABLE_BRIEFS = {
    'abs_china': abs_china,
    'ballantine_poland': ballantine_poland,
    'abs_valentine': Abs_Valentine,
    'codigo': Codigo,
    'abs_ocean_spray': ABS_OCEAN_SPRAY,
    'oaken_glow': Oaken_Glow,
    'abs_pride': ABS_PRIDE
}
```

**Brief Examples:**
- **abs_china**: Nightclub campaign for Absolut in Shanghai
- **ballantine_poland**: Highland Honey Hot Toddy winter campaign
- **abs_valentine**: Valentine's Day e-commerce assets
- **codigo**: Premium tequila rooftop lifestyle shots

---

## ⚙️ **Core Processing Pipeline**

### **Step 1: Dimension Extraction Function**

```python
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
```

**Technical Flow:**
1. **Input Preparation**: Combines prompt template with brief content
2. **AI Processing**: Sends to DeepSeek API for analysis
3. **Response Parsing**: Splits CSV response into dimension list
4. **Error Handling**: Returns empty list on failure with logging

### **Step 2: Multi-Brief Processing Engine**

```python
def process_briefs(brief_names: List[str]) -> Dict[str, Any]:
    """
    Process multiple briefs to extract dimensions and create campaign dictionary
    """
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
```

**Processing Logic:**
1. **Data Structure**: Creates comprehensive result dictionary
2. **Sequential Processing**: Extracts dimensions from each brief
3. **Aggregation**: Combines dimensions and calculates frequencies
4. **Metadata Tracking**: Records processing timestamps and counts

### **Step 3: Statistical Analysis Engine**

```python
# Summary generation within process_briefs()
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
```

**Analytics Computed:**
- ✅ **Total Unique Dimensions**: Cross-brief dimension diversity
- ✅ **Average Dimensions per Brief**: Complexity measurement
- ✅ **Most Common Dimensions**: Top 10 frequent parameters
- ✅ **Universal Dimensions**: Parameters appearing in ALL briefs

---

## 📊 **Output Data Structure**

### **Complete Result Schema**

```json
{
  "metadata": {
    "total_briefs_processed": 3,
    "brief_names": ["abs_china", "ballantine_poland", "codigo"],
    "analysis_timestamp": "2024-12-08T10:30:45.123456"
  },
  "briefs": {
    "abs_china": {
      "dimensions": ["Location", "Target Age", "Lighting", "Camera Angle", ...],
      "dimension_count": 12,
      "brief_content_length": 2845
    },
    "ballantine_poland": {
      "dimensions": ["Product Type", "Setting", "Season", "Target Audience", ...],
      "dimension_count": 10,
      "brief_content_length": 3024
    }
  },
  "all_dimensions": [
    "Camera Angle", "Lighting", "Location", "Product Type", "Season", 
    "Setting", "Target Age", "Target Audience", "Wardrobe"
  ],
  "dimension_frequency": {
    "Location": 2,
    "Target Audience": 3,
    "Lighting": 2,
    "Camera Angle": 1
  },
  "summary": {
    "total_unique_dimensions": 9,
    "average_dimensions_per_brief": 11.0,
    "most_common_dimensions": [
      ["Target Audience", 3],
      ["Location", 2],
      ["Lighting", 2]
    ],
    "dimensions_appearing_in_all_briefs": ["Target Audience"]
  }
}
```

---

## 🚀 **Usage Examples**

### **Single Brief Analysis**
```python
# Process one brief
results = main(['abs_china'])
```

### **Multi-Brief Comparison**
```python
# Compare multiple briefs
results = main(['abs_valentine', 'abs_ocean_spray', 'ballantine_poland'])
```

### **Full Dataset Analysis**
```python
# Process all available briefs
results = main(list(AVAILABLE_BRIEFS.keys()))
```

### **Custom Brief Set**
```python
# Analyze specific brand campaigns
whiskey_briefs = ['ballantine_poland', 'oaken_glow']
results = main(whiskey_briefs)
```

---

## 🎯 **Core System Capabilities**

### **Primary Functions**
- ✅ **AI-Powered Extraction**: Leverages DeepSeek for intelligent dimension identification
- ✅ **Standardized Output**: Consistent JSON structure for downstream processing
- ✅ **Statistical Analysis**: Built-in frequency and commonality analytics
- ✅ **Flexible Input**: Supports various brief formats and lengths

### **Analytical Insights Generated**
- 📊 **Dimension Standardization**: Creates consistent parameter vocabulary
- 📊 **Cross-Campaign Patterns**: Identifies common brief elements
- 📊 **Content Complexity**: Measures brief richness via dimension count
- 📊 **Template Extraction**: Finds universal brief structure elements

---

## 🔄 **Integration with Downstream Systems**

### **Connected Pipelines**
- **Brand_World Analysis**: Uses extracted dimensions for TF-IDF processing
- **Brief_Gap_Filling**: Leverages dimension lists for structured extraction
- **Comparative Analytics**: Feeds dimension data to analysis pipelines

### **Data Flow**
1. **Input**: Raw marketing brief texts
2. **Processing**: AI-powered dimension extraction
3. **Output**: Structured JSON with dimensions and analytics
4. **Integration**: Feeds standardized data to downstream systems

This system forms the foundation for parametric marketing brief analysis, creating structured, consistent dimension data from unstructured marketing content. 