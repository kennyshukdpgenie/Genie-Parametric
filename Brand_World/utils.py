import json
import re
import os
from typing import List, Set
import sys

# Add parent directory to path to import from root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.text_splitter import RecursiveCharacterTextSplitter
import pdfplumber

# Basic stop words (minimal set for basic filtering)
BASIC_STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 
    'with', 'would', 'can', 'could', 'should', 'may', 'might', 'must', 'shall',
    'this', 'these', 'those', 'they', 'them', 'their', 'there', 'where', 'when',
    'why', 'how', 'what', 'who', 'which', 'i', 'you', 'we', 'our', 'your', 'my',
    'me', 'him', 'her', 'us', 'or', 'but', 'if', 'then', 'than', 'so', 'very',
    'just', 'now', 'only', 'also', 'not', 'no', 'yes', 'do', 'does', 'did',
    'have', 'had', 'get', 'got', 'go', 'went', 'come', 'came', 'take', 'took',
    'make', 'made', 'see', 'saw', 'know', 'knew', 'think', 'thought', 'say', 'said'
}

def extract_and_split_pdf(pdf_filename, brandword_folder="files/brandword"):
    """
    Extract text from PDF and split into manageable chunks
    
    Args:
        pdf_filename: Name of the PDF file
        brandword_folder: Path to the brandword folder
    
    Returns:
        List of text chunks
    """
    # Construct full path to PDF
    pdf_path = os.path.join(brandword_folder, pdf_filename)
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    print(f"Extracting text from: {pdf_filename}")
    
    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
    print(f"Extracted {len(full_text)} characters from PDF")
    
    # Split into chunks for processing
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Larger chunks since we're just extracting words
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(full_text)
    
    print(f"Split into {len(chunks)} chunks for processing")
    return chunks

def clean_and_extract_words(text: str) -> Set[str]:
    """
    Extract clean, distinct words from text
    
    Args:
        text: Input text string
    
    Returns:
        Set of distinct cleaned words
    """
    if not text or text.strip() == '':
        return set()
    
    # Convert to lowercase and extract words (letters only)
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter out stop words, very short words, and keep only meaningful words
    meaningful_words = set()
    for word in words:
        if (len(word) > 2 and  # Keep words longer than 2 characters
            word not in BASIC_STOP_WORDS and  # Remove basic stop words
            word.isalpha()):  # Only alphabetic words
            meaningful_words.add(word)
    
    return meaningful_words

def extract_distinct_words_from_chunks(chunks: List[str]) -> Set[str]:
    """
    Extract all distinct words from a list of text chunks
    
    Args:
        chunks: List of text chunks
    
    Returns:
        Set of all distinct words found across all chunks
    """
    all_words = set()
    
    print(f"Processing {len(chunks)} chunks to extract distinct words...")
    
    for i, chunk in enumerate(chunks):
        chunk_words = clean_and_extract_words(chunk)
        all_words.update(chunk_words)
        
        if (i + 1) % 10 == 0:  # Progress update every 10 chunks
            print(f"Processed {i + 1}/{len(chunks)} chunks - Found {len(all_words)} unique words so far")
    
    print(f"Completed processing all chunks - Total unique words: {len(all_words)}")
    return all_words

def save_distinct_words_to_json(distinct_words: Set[str], pdf_filename: str, output_filename: str = None):
    """
    Save the list of distinct words to a JSON file
    
    Args:
        distinct_words: Set of distinct words
        pdf_filename: Name of the source PDF file
        output_filename: Name of output JSON file (auto-generated if None)
    
    Returns:
        Dictionary with the results and metadata
    """
    if output_filename is None:
        # Auto-generate filename based on PDF name
        base_name = os.path.splitext(pdf_filename)[0]
        output_filename = f"Brand_World/{base_name}_distinct_words.json"
    
    # Convert set to sorted list for JSON serialization
    word_list = sorted(list(distinct_words))
    
    # Create results dictionary
    results = {
        'metadata': {
            'source_pdf': pdf_filename,
            'total_distinct_words': len(word_list),
            'extraction_timestamp': __import__('datetime').datetime.now().isoformat(),
            'description': 'Distinct words extracted from PDF (stop words removed, min 3 characters)'
        },
        'distinct_words': word_list
    }
    
    # Save to JSON file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDistinct words saved to '{output_filename}'")
    return results

def list_available_pdfs(brandword_folder="files/brandword"):
    """
    List all available PDF files in the brandword folder
    
    Args:
        brandword_folder: Path to the brandword folder
    
    Returns:
        List of PDF filenames
    """
    if os.path.exists(brandword_folder):
        pdf_files = [f for f in os.listdir(brandword_folder) if f.endswith('.pdf')]
        return pdf_files
    else:
        print(f"Brandword folder not found: {brandword_folder}")
        return []
