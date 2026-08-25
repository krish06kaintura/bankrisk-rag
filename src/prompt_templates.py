SYSTEM_PROMPT = """You are BankRisk RAG, an expert financial research assistant analyzing bank annual reports.

Answer the user's question strictly and exclusively using the provided CONTEXT below.

CRITICAL GUARDRAIL RULES:
1. ONLY use facts directly stated in the CONTEXT. Do NOT assume, extrapolate, or use outside knowledge.
2. If the CONTEXT does not contain enough information to answer the question, state: "I cannot find this information in the provided annual reports."
3. Every factual statement or financial metric MUST include an inline citation in the exact format: [Bank FY<Year>, Page <PageNumber>].
4. Preserve all exact financial figures, percentages, and currencies without rounding or approximation.
"""

def format_context_with_citations(retrieved_results):
    """
    Formats the retrieved chunks into a clean, structured context block with clear citation tags.
    """
    if not retrieved_results:
        return "No relevant context found."
        
    context_blocks = []
    for i, res in enumerate(retrieved_results, start=1):
        chunk = res["chunk"]
        header = f"--- SOURCE [{chunk['bank']} FY{chunk['year']}, Page {chunk['page_number']}] ---"
        body = chunk["text"].strip()
        context_blocks.append(f"{header}\n{body}")
        
    return "\n\n".join(context_blocks)

def build_rag_prompt(query, retrieved_results):
    """
    Assembles the final prompt combining System Guardrails, Structured Context, and the User Query.
    """
    context_str = format_context_with_citations(retrieved_results)
    
    user_prompt = f"""CONTEXT:
{context_str}

USER QUESTION:
{query}

FINAL ANSWER (with inline citations):"""

    return SYSTEM_PROMPT, user_prompt

if __name__ == "__main__":
    # Test formatting with mock chunk
    mock_results = [{
        "chunk": {
            "bank": "HDFC",
            "year": 2026,
            "page_number": 2,
            "text": "The Gross NPA ratio for HDFC Bank stood at 1.22% in FY2026."
        },
        "distance_score": 0.45
    }]
    
    sys_p, usr_p = build_rag_prompt("What was HDFC's GNPA in 2026?", mock_results)
    print("=== SYSTEM PROMPT ===")
    print(sys_p)
    print("\n=== ASSEMBLED USER PROMPT ===")
    print(usr_p)
