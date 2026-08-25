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

def search_vector_db(query, index, chunks, model, top_k=3):
    print(f"\n--- Searching for query: '{query}' (top_k={top_k}) ---")
    
    # 1. Convert user's query string into 384-D vector
    query_vector = model.encode([query])
    
    # 2. Search FAISS index for the k closest vectors
    distances, indices = index.search(np.array(query_vector), k=top_k)
    
    results = []
    # 3. Map indices back to original chunk dictionaries
    for i, idx in enumerate(indices[0]):
        matched_chunk = chunks[idx]
        distance = distances[0][i]
        results.append({
            "chunk": matched_chunk,
            "distance_score": float(distance)
        })
        
    return results

if __name__ == "__main__":
    # --- Step A: Batch Ingest Entire Corpus ---
    all_chunks = ingest_all_reports("data/reports")
    
    # --- Step B: Build Multi-Document FAISS Index ---
    faiss_index, embedding_model = build_vector_database(all_chunks)
    
    # --- Step C: Test Multi-Bank Search Query ---
    test_query = "What is the Gross NPA ratio for ICICI Bank?"
    search_results = search_vector_db(test_query, faiss_index, all_chunks, embedding_model, top_k=2)
    
    print("\n" + "="*50)
    print("TOP RETRIEVED CHUNKS:")
    print("="*50)
    for rank, res in enumerate(search_results, start=1):
        chunk = res["chunk"]
        print(f"\n[Rank {rank}] (Distance Score: {res['distance_score']:.4f})")
        print(f"Source: {chunk['bank']} FY{chunk['year']} (Page {chunk['page_number']})")
        print(f"Text:\n{chunk['text']}")



