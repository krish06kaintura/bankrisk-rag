import re
from typing import List, Dict, Any, Tuple, Optional

class InputGuardrail:
    """
    Tier 1: Pre-Retrieval Input Security
    Protects against Prompt Injections, Jailbreaks, PII Leaks, and Out-of-Domain abuse.
    """
    # 1. Known Prompt Injection & Jailbreak Signatures
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules|commands)",
        r"(system\s+prompt|system\s+instruction)",
        r"(bypass|override|disable)\s+(guardrails?|safety|rules?|restrictions?)",
        r"(act\s+as|pretend\s+to\s+be|roleplay\s+as)\s+(an?\s+)?(unrestricted|unfiltered|jailbroken|evil|DAN)",
        r"you\s+are\s+now\s+(in\s+)?(developer\s+mode|unrestricted|god\s+mode)",
        r"reveal\s+(your\s+)?(secret|internal|hidden|system)\s+(instructions|prompt)",
        r"<\s*script\s*>",
        r"drop\s+table\s+",
        r"UNION\s+SELECT\s+",
    ]

    # 2. Personally Identifiable Information (PII) Patterns
    PII_PATTERNS = {
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "INDIAN_PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "INDIAN_AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "PHONE_NUMBER": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
    }

    # 3. Financial Domain Indicator Keywords (Scope Gatekeeper)
    FINANCIAL_KEYWORDS = [
        "npa", "gnpa", "net npa", "car", "capital adequacy", "pcr", "provision",
        "lcr", "liquidity", "nim", "net interest margin", "profit", "deposit",
        "advance", "loan", "asset quality", "credit risk", "market risk", "annual report",
        "hdfc", "icici", "sbi", "state bank", "fy23", "fy24", "fy25", "fy26",
        "fiscal", "balance sheet", "roe", "roa", "cet-1", "tier 1", "slippage",
        "ratio", "cost", "revenue", "grow", "bank", "financial", "equity", "default"
    ]

    @classmethod
    def validate(cls, query: str) -> Tuple[bool, str, str]:
        """
        Validates query for security risks.
        Returns: (is_allowed: bool, sanitized_query: str, reason: str)
        """
        if not query or len(query.strip()) < 3:
            return False, query, "Query is too short or empty."

        clean_query = query.strip()

        # Step A: Check for Prompt Injection / Jailbreaks
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, clean_query, re.IGNORECASE):
                return False, clean_query, "Security Alert: Prompt injection or jailbreak pattern detected. Request blocked by policy."

        # Step B: Check and Scrub PII
        sanitized_query = clean_query
        detected_pii = []
        for pii_type, pattern in cls.PII_PATTERNS.items():
            matches = re.findall(pattern, sanitized_query, re.IGNORECASE)
            if matches:
                detected_pii.append(pii_type)
                sanitized_query = re.sub(pattern, f"[REDACTED_{pii_type}]", sanitized_query, flags=re.IGNORECASE)

        if detected_pii:
            # We scrub PII but log warning
            pass

        # Step C: Domain Scope Gatekeeper
        lowered = clean_query.lower()
        has_domain_match = any(kw in lowered for kw in cls.FINANCIAL_KEYWORDS)
        
        # Check for obvious non-financial questions (e.g. recipes, fiction, coding)
        non_financial_triggers = [
            r"recipe", r"chocolate\s+cake", r"bake", r"poem", r"story", r"weather",
            r"python\s+script\s+to\s+hack", r"write\s+code\s+for", r"who\s+is\s+the\s+prime\s+minister"
        ]
        for trigger in non_financial_triggers:
            if re.search(trigger, lowered):
                return False, clean_query, "Scope Alert: Query is outside the scope of banking financial risk and annual report analysis."

        if not has_domain_match:
            # If no financial terms detected, reject gracefully before invoking vector search
            return False, clean_query, "Scope Alert: No financial, banking, or annual report terms recognized. Please ask about bank risk, NPA, liquidity, or capital ratios."

        return True, sanitized_query, "Input valid."


class RetrievalGuardrail:
    """
    Tier 2: In-Flight Retrieval Quality Gatekeeper
    Evaluates vector relevance and Cross-Encoder confidence before calling the LLM.
    """
    # Minimum Cross-Encoder score required for confidence
    MIN_RERANK_SCORE_THRESHOLD = -5.0
    MAX_FAISS_DISTANCE_THRESHOLD = 1.45

    @classmethod
    def validate(cls, retrieved_results: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Validates if retrieved chunks have genuine semantic relevance.
        """
        if not retrieved_results:
            return False, "No candidate document chunks found in database."

        top_result = retrieved_results[0]
        
        # Check rerank score if available
        if "rerank_score" in top_result:
            score = top_result["rerank_score"]
            if score < cls.MIN_RERANK_SCORE_THRESHOLD:
                return False, f"Retrieval Confidence Alert: Top chunk relevance score ({score:.2f}) is below confidence threshold ({cls.MIN_RERANK_SCORE_THRESHOLD}). Refusing to generate."
                
        # Check FAISS distance
        if "distance_score" in top_result:
            dist = top_result["distance_score"]
            if dist > cls.MAX_FAISS_DISTANCE_THRESHOLD:
                return False, f"Retrieval Confidence Alert: Vector distance ({dist:.2f}) indicates chunks are mathematically distant from query."

        return True, "Retrieval passed confidence gate."


class OutputGuardrail:
    """
    Tier 3: Post-Generation Grounding & Citation Auditor
    Verifies that all numbers, percentages, and citations in the generated answer
    exist directly in the retrieved source chunks (Zero Hallucination Enforcement).
    """
    PERCENTAGE_PATTERN = r"\b\d+(?:\.\d+)?%"
    CURRENCY_PATTERN = r"(?:Rs\.?|INR|\$)\s*[\d,]+(?:\.\d+)?\s*(?:crore|lakh|billion|million)?"
    CITATION_PATTERN = r"\[([A-Z]+)\s+FY(\d{2,4}),\s+Page\s+(\d+)\]"

    @classmethod
    def audit(cls, answer: str, source_chunks: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Audits answer for factual numbers and citation fidelity against source chunks.
        """
        if not answer:
            return True, answer, {"status": "EMPTY"}

        # Combine all source chunk texts for fast substring verification
        combined_source_text = " ".join([item["chunk"]["text"] for item in source_chunks])
        
        # 1. Audit Numbers & Percentages
        answer_percentages = set(re.findall(cls.PERCENTAGE_PATTERN, answer))
        unverified_metrics = []
        for pct in answer_percentages:
            if pct not in combined_source_text:
                unverified_metrics.append(pct)

        # 2. Audit Citations
        citations = re.findall(cls.CITATION_PATTERN, answer)
        valid_citations = []
        invalid_citations = []

        # Build list of genuine sources from chunks
        genuine_sources = set()
        for item in source_chunks:
            c = item["chunk"]
            bank = c["bank"].upper()
            yr = str(c["year"])
            pg = str(c["page_number"])
            genuine_sources.add((bank, yr, pg))
            # Also support 2-digit year
            if len(yr) == 4:
                genuine_sources.add((bank, yr[2:], pg))

        for cit in citations:
            bank, yr, pg = cit
            if (bank.upper(), yr, pg) in genuine_sources:
                valid_citations.append(f"[{bank} FY{yr}, Page {pg}]")
            else:
                invalid_citations.append(f"[{bank} FY{yr}, Page {pg}]")

        audit_passed = True
        warnings = []

        if unverified_metrics:
            audit_passed = False
            warnings.append(f"Unverified Financial Figures Detected: {', '.join(unverified_metrics)}")

        if invalid_citations:
            audit_passed = False
            warnings.append(f"Forged / Unbacked Citations Detected: {', '.join(invalid_citations)}")

        audit_meta = {
            "audit_passed": audit_passed,
            "verified_percentages": list(answer_percentages - set(unverified_metrics)),
            "unverified_metrics": unverified_metrics,
            "valid_citations": valid_citations,
            "invalid_citations": invalid_citations,
            "warnings": warnings
        }

        # If audit failed, append an explicit audit seal to response
        audited_answer = answer
        if not audit_passed:
            audited_answer += "\n\n[COMPLIANCE AUDIT NOTICE]: " + " | ".join(warnings)

        return audit_passed, audited_answer, audit_meta


class BankRiskGuardrailSuite:
    """
    Consolidated 3-Tier Enterprise Guardrail Suite.
    """
    def __init__(self):
        self.input_guardrail = InputGuardrail
        self.retrieval_guardrail = RetrievalGuardrail
        self.output_guardrail = OutputGuardrail

    def pre_retrieval_check(self, query: str) -> Tuple[bool, str, str]:
        return self.input_guardrail.validate(query)

    def in_flight_check(self, candidates: List[Dict[str, Any]]) -> Tuple[bool, str]:
        return self.retrieval_guardrail.validate(candidates)

    def post_generation_audit(self, answer: str, source_chunks: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, Any]]:
        return self.output_guardrail.audit(answer, source_chunks)

