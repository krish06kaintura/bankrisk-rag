import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from ingestion import ingest_all_reports

def build_vector_database(chunks):
    print("1. Loading Embedding Model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print(f"2. Extracting text from {len(chunks)} chunks across all reports...")
    # We only want to encode the "text" part of our dictionaries, not the metadata
    texts = [chunk["text"] for chunk in chunks]
    
    print("3. Converting text to math vectors... (this may take a few seconds)")
    embeddings = model.encode(texts)
    
    dimension = embeddings.shape[1]
    
    print(f"4. Initializing FAISS Database with {dimension} dimensions...")
    index = faiss.IndexFlatL2(dimension)
    
    print("5. Adding vectors to the database...")
    index.add(np.array(embeddings))
    
    print(f"Success! Multi-Bank FAISS database now contains {index.ntotal} vectors.")
    return index, model

def search_vector_db(query, index, chunks, model, top_k=3, filter_bank=None, filter_year=None):
    filter_info = f" [Filter: Bank={filter_bank or 'ALL'}, Year={filter_year or 'ALL'}]" if (filter_bank or filter_year) else ""
    print(f"\n--- Searching for: '{query}' (top_k={top_k}){filter_info} ---")
    
    # 1. Pre-Filtering: identify matching chunk indices
    candidate_indices = []
    for idx, chunk in enumerate(chunks):
        match_bank = (filter_bank is None) or (chunk["bank"].upper() == filter_bank.upper())
        match_year = (filter_year is None) or (int(chunk["year"]) == int(filter_year))
        if match_bank and match_year:
            candidate_indices.append(idx)
            
    if not candidate_indices:
        print("No chunks match the specified metadata filter.")
        return []
        
    # 2. Convert query string into 384-D vector
    query_vector = model.encode([query])
    
    # 3. If pre-filtered subset is selected, search within valid candidates
    if len(candidate_indices) < len(chunks):
        candidate_texts = [chunks[i]["text"] for i in candidate_indices]
        candidate_embeddings = model.encode(candidate_texts)
        
        sub_index = faiss.IndexFlatL2(candidate_embeddings.shape[1])
        sub_index.add(np.array(candidate_embeddings))
        
        actual_k = min(top_k, len(candidate_indices))
        distances, indices = sub_index.search(np.array(query_vector), k=actual_k)
        
        results = []
        for i, sub_idx in enumerate(indices[0]):
            orig_idx = candidate_indices[sub_idx]
            results.append({
                "chunk": chunks[orig_idx],
                "distance_score": float(distances[0][i])
            })
        return results
    else:
        # Standard global search across all chunks
        distances, indices = index.search(np.array(query_vector), k=top_k)
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "chunk": chunks[idx],
                "distance_score": float(distances[0][i])
            })
        return results

if __name__ == "__main__":
    # --- Step A: Batch Ingest Entire Corpus ---
    all_chunks = ingest_all_reports("data/reports")
    
    # --- Step B: Build Multi-Document FAISS Index ---
    faiss_index, embedding_model = build_vector_database(all_chunks)
    
    # --- Step C: Test Pre-Filtered Search Query ---
    # Asking about NPA, but strictly enforcing HDFC + FY2025
    test_query = "What was the Gross NPA ratio?"
    search_results = search_vector_db(
        test_query, 
        faiss_index, 
        all_chunks, 
        embedding_model, 
        top_k=2,
        filter_bank="HDFC",
        filter_year=2025
    )
    
    print("\n" + "="*50)
    print("TOP PRE-FILTERED RETRIEVED CHUNKS:")
    print("="*50)
    for rank, res in enumerate(search_results, start=1):
        chunk = res["chunk"]
        print(f"\n[Rank {rank}] (Distance Score: {res['distance_score']:.4f})")
        print(f"Source: {chunk['bank']} FY{chunk['year']} (Page {chunk['page_number']})")
        print(f"Text:\n{chunk['text']}")




