from sentence_transformers import CrossEncoder

class FinancialReranker:
    """
    Two-Stage Retrieval Reranker using a Cross-Encoder.
    Performs full cross-attention between user query and candidate chunks
    to resolve acronyms, negations, and subtle financial contexts.
    """
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        print("Loading Cross-Encoder Reranker model...")
        self.model = CrossEncoder(model_name)
        print("Cross-Encoder Reranker ready.")

    def rerank(self, query, candidates, top_k=3):
        if not candidates:
            return []

        # If we have fewer candidates than top_k, no need to truncate
        k = min(top_k, len(candidates))
        
        # Prepare pairs for cross-attention evaluation
        pairs = [[query, item["chunk"]["text"]] for item in candidates]
        
        # Compute joint cross-attention relevance scores
        raw_scores = self.model.predict(pairs)
        
        # Attach rerank score and track original FAISS rank
        scored_candidates = []
        for i, item in enumerate(candidates):
            item_copy = dict(item)
            item_copy["original_faiss_rank"] = i + 1
            item_copy["rerank_score"] = float(raw_scores[i])
            scored_candidates.append(item_copy)
            
        # Re-sort descending by cross-encoder score
        reranked = sorted(scored_candidates, key=lambda x: x["rerank_score"], reverse=True)
        
        # Assign new rerank position
        for new_rank, item in enumerate(reranked, start=1):
            item["rerank_position"] = new_rank

        return reranked[:k]

if __name__ == "__main__":
    # Test reranker standalone
    reranker = FinancialReranker()
    test_query = "What was the Gross NPA ratio for HDFC Bank in FY2025?"
    
    mock_candidates = [
        {
            "chunk": {
                "bank": "HDFC",
                "year": 2025,
                "page_number": 1,
                "text": "HDFC Bank - Annual Report FY2024-25 Executive Overview: Total deposits grew by 16.5%..."
            },
            "distance_score": 0.62
        },
        {
            "chunk": {
                "bank": "HDFC",
                "year": 2025,
                "page_number": 2,
                "text": "1. Credit Risk Management (FY2025): In FY2025, the Gross Non-Performing Assets (GNPA) stood at 1.33%..."
            },
            "distance_score": 1.20
        }
    ]
    
    results = reranker.rerank(test_query, mock_candidates, top_k=2)
    print("\n--- RERANKING RESULTS ---")
    for r in results:
        print(f"Rerank #{r['rerank_position']} (Original FAISS #{r['original_faiss_rank']}) | Score: {r['rerank_score']:.4f}")
        print(f"Text: {r['chunk']['text'][:80]}...\n")
