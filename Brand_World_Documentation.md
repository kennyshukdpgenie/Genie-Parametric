# Brand World Analysis System
## Technical Documentation for Data Scientists

---

## 📋 **System Overview**

The Brand World Analysis system processes brand guideline PDFs to extract and analyze marketing dimensions using AI and TF-IDF analysis. It converts unstructured brand documents into structured, probabilistic dimension distributions for use in downstream gap-filling processes.

### **Core Purpose**
- Extract structured dimension data from brand guideline PDFs
- Create TF-IDF probability distributions for each marketing dimension  
- Generate brandworld analysis files for Brief_Gap_Filling consumption
- Enable data-driven brand knowledge utilization

---

## 🏗️ **System Architecture**

```
Brand_World/
├── main.py                           # Processing pipeline orchestration
├── utils.py                          # PDF extraction, AI processing, TF-IDF analysis
├── briefs.py                         # Brief repository (inherited from Brief_Dimension_Generation)
├── Skrewball Brand World_analysis.json   # Output: Complete analysis results
└── Skrewball Brand World_tfidf_analysis.json  # Output: TF-IDF distributions only
```

### **External Dependencies**
- `prompts.py` (root) - AI prompt templates
- `utils.py` (root) - DeepSeek API integration
- `files/brandword/` - PDF source files

---

## ⚙️ **Core Processing Pipeline**

### **Step 1: PDF Extraction & Chunking**

```python
def extract_and_split_pdf(pdf_filename, brandword_folder="files/brandword"):
    """Extract text from PDF and split into semantic chunks"""
    # Extract text using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() for page in pdf.pages)
    
    # Split into semantic chunks with overlap
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(full_text)
    return chunks
```

**Technical Flow:**
1. **PDF Text Extraction**: Uses pdfplumber to extract all text content
2. **Semantic Chunking**: Splits text into overlapping 1000-character chunks
3. **Chunk Preparation**: Creates processable text units for AI analysis

### **Step 2: AI-Powered Dimension Extraction**

```python
def process_chunks_with_deepseek(chunks, system_prompt, deepseek_chat_func):
    """Process all chunks through DeepSeek API and return structured data"""
    all_dict_data = []
    
    for i, chunk in enumerate(chunks):
        message = f'{system_prompt}, and input message is {chunk}'
        
        try:
            response = deepseek_chat_func(message)
            clean_response = response.strip('```json\n').strip('```')
            dict_data = json.loads(clean_response)
            all_dict_data.append(dict_data)
            
        except json.JSONDecodeError:
            # Create empty dict with all dimensions if parsing fails
            empty_dict = {dim: '' for dim in DIM_LIST}
            all_dict_data.append(empty_dict)
    
    return all_dict_data
```

**Processing Logic:**
1. **AI Analysis**: Each chunk processed by DeepSeek to extract dimension values
2. **JSON Parsing**: Converts AI responses to structured dictionaries
3. **Error Handling**: Creates empty dimensions on parsing failures
4. **Data Accumulation**: Builds comprehensive dataset from all chunks

### **Step 3: TF-IDF Probability Distribution Creation**

```python
def create_tfidf_distributions(all_dict_data, dimensions):
    """Create TF-IDF distributions for each dimension"""
    # Step 1: Collect and clean words for each dimension
    dimension_words = {}
    for dimension in dimensions:
        all_words = []
        for dict_data in all_dict_data:
            if dimension in dict_data and dict_data[dimension]:
                words = clean_and_tokenize_text(dict_data[dimension])
                all_words.extend(words)
        dimension_words[dimension] = all_words
    
    # Step 2: Calculate IDF scores across all dimensions
    idf_scores = calculate_idf(dimension_words)
    
    # Step 3: Calculate TF-IDF for each dimension
    for dimension in dimensions:
        words = dimension_words[dimension]
        tf_scores = calculate_tf(words)
        
        # Calculate TF-IDF scores
        tfidf_scores = {}
        for word, tf in tf_scores.items():
            idf = idf_scores.get(word, 0)
            tfidf_scores[word] = tf * idf
        
        # Create probability distribution
        total_tfidf = sum(tfidf_scores.values())
        probability_dist = {word: score/total_tfidf for word, score in tfidf_scores.items()}
```

**Mathematical Analysis:**
1. **Text Preprocessing**: Tokenization and stop word removal
2. **TF Calculation**: Term frequency within each dimension
3. **IDF Calculation**: Inverse document frequency across dimensions  
4. **TF-IDF Scoring**: Combined relevance scoring
5. **Probability Distribution**: Normalized probability weights for gap filling

---

## 📊 **Output Data Structure**

### **Standard Dimensions Analyzed**

```python
DIM_LIST = [
    'Campaign Theme', 'Marketing Objectives', 'Universal Consumer Challenge',
    'Local Consumer Challenge (Market-Specific)', 'Brand Context/Heritage',
    'Campaign Ambition/Scope', 'Target Audience (Strategic Segment)',
    'Audience Demographics/Behavior', 'Single-Minded Message', 'Tone of Voice',
    'Key Deliverables/Assets', 'Success Metrics (KPIs)', 'Mandatory Channels/Formats',
    'Representation/Inclusivity Guidelines', 'Cultural Adaptation Requirements'
]
```

### **Complete Analysis Schema**

```json
{
  "metadata": {
    "source_pdf": "Skrewball Brand World.pdf",
    "total_chunks_processed": 45,
    "dimensions_analyzed": ["Campaign Theme", "Marketing Objectives", ...],
    "analysis_type": "TF-IDF with stop word removal"
  },
  "tfidf_analysis": {
    "Campaign Theme": {
      "probability_distribution": {"whiskey": 0.15, "peanut": 0.12, "butter": 0.10, ...},
      "top_10_tfidf": [["whiskey", 2.45], ["peanut", 2.12], ...],
      "unique_words": 45,
      "raw_word_count": 123
    }
  },
  "summary": {
    "dimensions_with_data": 12,
    "total_unique_meaningful_words": 890,
    "most_active_dimensions": [["Brand Context/Heritage", 156], ...]
  }
}
```

---

## 🚀 **Usage Example**

```python
# From Brand_World/main.py
def main(pdf_filename):
    # Step 1: Extract and split PDF into chunks
    chunks = extract_and_split_pdf(pdf_filename)
    
    # Step 2: Process chunks with DeepSeek
    all_dict_data = process_chunks_with_deepseek(chunks, SYSTEM_PROMPT, deepseek_chat)
    
    # Step 3: Create word frequency distributions
    dimension_word_frequencies = create_tfidf_distributions(all_dict_data, DIM_LIST)
    
    # Step 4: Save comprehensive results to JSON
    final_results = save_results_to_json(all_dict_data, dimension_word_frequencies, pdf_filename)
    
    return final_results

# Execute
results = main("Skrewball Brand World.pdf")
```

---

## 🎯 **Core System Capabilities**

### **Primary Functions**
- ✅ **PDF Processing**: Robust text extraction and semantic chunking
- ✅ **AI Integration**: DeepSeek-powered dimension value extraction  
- ✅ **TF-IDF Analysis**: Statistical text analysis with stop word filtering
- ✅ **Probability Generation**: Creates weighted distributions for gap filling

### **Analytical Outputs**
- 📊 **Brand Knowledge Base**: Structured dimension-value mappings
- 📊 **Probability Distributions**: TF-IDF weighted word probabilities
- 📊 **Statistical Insights**: Word frequency and dimension activity analysis
- 📊 **Gap-Filling Ready Data**: Pre-computed brandworld knowledge

---

## 🔄 **Integration with Downstream Systems**

### **Data Flow**
1. **Input**: Brand guideline PDFs from `files/brandword/`
2. **Processing**: AI extraction + TF-IDF analysis
3. **Output**: JSON files with probability distributions
4. **Integration**: Brief_Gap_Filling consumes generated JSON files

### **Output Files Created**
- `{brand}_analysis.json` - Complete analysis with chunk data
- `{brand}_tfidf_analysis.json` - TF-IDF distributions only
- Used by Brief_Gap_Filling for intelligent dimension completion

This system transforms unstructured brand documents into structured, probabilistic knowledge bases that enable intelligent gap filling in marketing brief analysis. 