import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from rag_pipeline import BankRiskRAG
from prompt_templates import build_rag_prompt

def run_evaluation():
    rag = BankRiskRAG("data/reports")
    
    test_suite = [
        {
            "id": "TEST-1",
            "title": "Single-Bank Targeted Metric (Pre-Filtered Retrieval)",
            "query": "What was the Gross NPA ratio and Provision Coverage Ratio for HDFC Bank in FY2025?",
            "bank": "HDFC",
            "year": 2025,
            "top_k": 2
        },
        {
            "id": "TEST-2",
            "title": "Multi-Bank Cross-Document Comparison (Global Search)",
            "query": "Compare the Liquidity Coverage Ratio (LCR) between HDFC and ICICI in FY2026.",
            "bank": None,
            "year": 2026,
            "top_k": 2
        },
        {
            "id": "TEST-3",
            "title": "Hallucination & Refusal Guardrail Test (Out-of-Bounds)",
            "query": "What was the total bonus paid to the CEO of ICICI Bank in FY2025?",
            "bank": "ICICI",
            "year": 2025,
            "top_k": 2
        }
    ]
    
    print("\n" + "#"*70)
    print("           STARTING END-TO-END SYSTEM TEST EVALUATION")
    print("#"*70)
    
    for test in test_suite:
        print("\n" + "="*70)
        print(f"[{test['id']}] {test['title']}")
        print(f"QUERY:       \"{test['query']}\"")
        print(f"FILTER:      Bank={test['bank'] or 'ALL'}, Year={test['year'] or 'ALL'}")
        print("="*70)
        
        answer, retrieved = rag.ask(
            query=test["query"],
            filter_bank=test["bank"],
            filter_year=test["year"],
            top_k=test["top_k"]
        )
        
        print("\n--- RETRIEVED CHUNKS FROM FAISS ---")
        for rank, res in enumerate(retrieved, start=1):
            c = res["chunk"]
            dist = res["distance_score"]
            print(f"[{rank}] Source: {c['bank']} FY{c['year']} (Page {c['page_number']}) | Distance: {dist:.4f}")
            print(f"    Text: {c['text'][:140]}...")
            
        print("\n--- FINAL RAG GENERATION ---")
        print(answer)

if __name__ == "__main__":
    run_evaluation()
