import sys
import os

# Add parent directory to path to import from root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Brand_World.utils import (
    extract_and_split_pdf,
    extract_distinct_words_from_chunks,
    save_distinct_words_to_json,
    list_available_pdfs
)

def extract_distinct_words_from_pdf(pdf_filename):
    """
    Extract distinct words from a PDF file
    
    Args:
        pdf_filename: Name of the PDF file to process from files/brandword folder
    
    Returns:
        Dictionary with extraction results
    """
    print("Starting Brand World PDF Word Extraction...")
    print(f"Target PDF: {pdf_filename}")
    
    try:
        # Step 1: Extract and split PDF into chunks
        chunks = extract_and_split_pdf(pdf_filename)
        
        # Step 2: Extract distinct words from all chunks
        distinct_words = extract_distinct_words_from_chunks(chunks)
        
        # Step 3: Save results to JSON
        results = save_distinct_words_to_json(distinct_words, pdf_filename)
        
        # Print summary
        print(f"\n" + "="*50)
        print("PDF WORD EXTRACTION COMPLETE")
        print("="*50)
        print(f"Source PDF: {pdf_filename}")
        print(f"Processed {len(chunks)} chunks")
        print(f"Found {len(distinct_words)} distinct words")
        
        # Print first 20 words as sample
        word_list = sorted(list(distinct_words))
        if word_list:
            print(f"\nSample words (first 20):")
            for i, word in enumerate(word_list[:20], 1):
                print(f"  {i:2d}. {word}")
            
            if len(word_list) > 20:
                print(f"  ... and {len(word_list) - 20} more words")
        
        return results
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Available PDF files in files/brandword:")
        available_pdfs = list_available_pdfs()
        for pdf_file in available_pdfs:
            print(f"  - {pdf_file}")
        return None
        
    except Exception as e:
        print(f"Error during processing: {e}")
        return None

def process_all_pdfs():
    """
    Process all available PDF files and extract distinct words from each
    
    Returns:
        Dictionary with results for all processed PDFs
    """
    available_pdfs = list_available_pdfs()
    
    if not available_pdfs:
        print("No PDF files found in files/brandword folder!")
        return {}
    
    print(f"Found {len(available_pdfs)} PDF files to process:")
    for pdf_file in available_pdfs:
        print(f"  - {pdf_file}")
    
    all_results = {}
    
    for i, pdf_file in enumerate(available_pdfs, 1):
        print(f"\n{'='*60}")
        print(f"Processing PDF {i}/{len(available_pdfs)}: {pdf_file}")
        print(f"{'='*60}")
        
        try:
            results = extract_distinct_words_from_pdf(pdf_file)
            if results:
                all_results[pdf_file] = results
                print(f"✅ Successfully processed {pdf_file}")
            else:
                print(f"❌ Failed to process {pdf_file}")
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {e}")
    
    # Save combined summary
    if all_results:
        summary_filename = "Brand_World/all_pdfs_word_extraction_summary.json"
        
        # Create summary statistics
        total_files = len(all_results)
        total_unique_words_across_all = set()
        
        for results in all_results.values():
            total_unique_words_across_all.update(results['distinct_words'])
        
        summary = {
            'summary': {
                'total_pdfs_processed': total_files,
                'total_unique_words_across_all_pdfs': len(total_unique_words_across_all),
                'processing_timestamp': __import__('datetime').datetime.now().isoformat()
            },
            'individual_results': {
                pdf_name: {
                    'word_count': len(results['distinct_words']),
                    'source_pdf': results['metadata']['source_pdf']
                }
                for pdf_name, results in all_results.items()
            },
            'all_unique_words': sorted(list(total_unique_words_across_all))
        }
        
        import json
        with open(summary_filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print("BATCH PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"Processed {total_files} PDF files")
        print(f"Total unique words across all files: {len(total_unique_words_across_all)}")
        print(f"Summary saved to: {summary_filename}")
    
    return all_results

# Execute the main function
if __name__ == "__main__":
    print("Brand World PDF Word Extraction Tool")
    print("=" * 40)
    
    # List available PDFs
    available_pdfs = list_available_pdfs()
    
    if available_pdfs:
        print(f"Found {len(available_pdfs)} PDF files:")
        for i, pdf_file in enumerate(available_pdfs, 1):
            print(f"  {i}. {pdf_file}")
        
        print("\nChoose processing option:")
        print("1. Process a single PDF")
        print("2. Process all PDFs")
        print("3. Exit")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\nAvailable PDFs:")
                for i, pdf_file in enumerate(available_pdfs, 1):
                    print(f"  {i}. {pdf_file}")
                
                pdf_choice = input(f"\nEnter PDF number (1-{len(available_pdfs)}): ").strip()
                
                try:
                    pdf_index = int(pdf_choice) - 1
                    if 0 <= pdf_index < len(available_pdfs):
                        selected_pdf = available_pdfs[pdf_index]
                        results = extract_distinct_words_from_pdf(selected_pdf)
                    else:
                        print("Invalid PDF number!")
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == "2":
                results = process_all_pdfs()
                
            elif choice == "3":
                print("Exiting...")
                
            else:
                print("Invalid choice!")
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No PDF files found in files/brandword folder!")
        print("Please add PDF files to the files/brandword directory.")

