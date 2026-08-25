import os
import re
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

def parse_filename_metadata(filename):
    """ 
    Extracts bank name and fiscal year from standard naming convention:
    e.g., 'hdfc_fy26.pdf' -> ('HDFC', 2026)
          'icici_fy25.pdf' -> ('ICICI', 2025)
    """
    basename = os.path.splitext(filename)[0].lower()
    parts = basename.split("_")
    bank = parts[0].upper()
    
    # Extract 2 or 4 digit year
    year_match = re.search(r"\d{2,4}", parts[1])
    if year_match:
        raw_year = year_match.group()
        year = int("20" + raw_year) if len(raw_year) == 2 else int(raw_year)
    else:
        year = 2026
        
    return bank, year

def ingest_pdf_to_pages(pdf_path, bank_name, year):
    doc = pymupdf.open(pdf_path)
    pages_data = [] # This will hold a list of all our dictionary chunks
    
    # Loop through every single page in the PDF
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip() # Loops through each page and pulls out text
        
        # Only save the page if it actually has text (ignore blank pages)
        if text:
            page_metadata = {
                "bank": bank_name,
                "year": year,
                "page_number": page_num + 1,  # 1-based indexing
                "text": text
            }
            pages_data.append(page_metadata)
            
    return pages_data

def chunk_documents(pages_data, chunk_size=500, chunk_overlap=50):
    # 1. Initialize the LangChain chunker
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    final_chunks = []
    
    # 2. Loop through our large page dictionaries
    for page in pages_data:
        small_texts = text_splitter.split_text(page["text"])
        
        # 3. Re-attach the original metadata to EACH tiny chunk
        for small_text in small_texts:
            new_chunk = {
                "text": small_text,
                "bank": page["bank"],
                "year": page["year"],
                "page_number": page["page_number"]
            }
            final_chunks.append(new_chunk)
            
    return final_chunks

def ingest_all_reports(reports_dir="data/reports"):
    """
    Discovers all PDF reports in directory and chunks them with metadata automatically.
    """
    all_chunks = []
    pdf_files = [f for f in os.listdir(reports_dir) if f.endswith(".pdf")]
    
    print(f"--- Discovering & Ingesting {len(pdf_files)} PDF Reports ---")
    for file in sorted(pdf_files):
        bank, year = parse_filename_metadata(file)
        pdf_path = os.path.join(reports_dir, file)
        
        pages = ingest_pdf_to_pages(pdf_path, bank_name=bank, year=year)
        chunks = chunk_documents(pages)
        all_chunks.extend(chunks)
        print(f"Loaded: {file:15} | Bank: {bank:6} | Year: {year} | Chunks: {len(chunks)}")
        
    print(f"Total Corpus: {len(all_chunks)} chunks from {len(pdf_files)} reports.")
    return all_chunks

if __name__ == "__main__":
    # Test batch ingestion across the whole corpus
    all_corpus_chunks = ingest_all_reports("data/reports")
    
    print("\n--- SAMPLE CHUNK FROM CORPUS ---")
    print(all_corpus_chunks[0])