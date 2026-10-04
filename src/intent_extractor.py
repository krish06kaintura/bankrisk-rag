import re
from typing import Tuple, Optional, List, Dict, Any

class SmartIntentExtractor:
    """
    Context-Aware Intent & Entity Extractor.
    Automatically infers target bank(s) and fiscal year(s) from natural language
    without blindly locking filters when comparisons or trends are requested.
    """
    BANK_PATTERNS = {
        "HDFC": [r"\bhdfc\b", r"\bhdfs\b", r"\bhdfc\s+bank\b"],
        "ICICI": [r"\bicici\b", r"\bicic\b", r"\bicici\s+bank\b"],
        "SBI": [r"\bsbi\b", r"\bstate\s+bank\b", r"\bstate\s+bank\s+of\s+india\b"]
    }

    MULTI_YEAR_TREND_KEYWORDS = [
        r"\btrend\b", r"\bevolv(e|ed|ing|ution)\b", r"\bgrowth\b", r"\bhistory\b",
        r"\bhistorical\b", r"\bover\s+the\s+years\b", r"\bacross\s+(all\s+)?years\b",
        r"\bev(e)?ry\s+(other\s+)?years?\b", r"\b(other|all|past|previous|prior)\s+years?\b", r"\bcomp(are|aring)\s+.*years?\b", 
        r"\bfrom\s+\d{2,4}\s+to\s+\d{2,4}\b", r"\bbetween\s+\d{2,4}\s+and\s+\d{2,4}\b"
    ]

    CROSS_BANK_KEYWORDS = [
        r"\bacross\s+(all\s+)?banks\b", r"\ball\s+banks\b", r"\bboth\s+banks\b",
        r"\bwhich\s+bank\b", r"\bwho\s+had\s+higher\b", r"\bwho\s+had\s+lower\b",
        r"\bcompare\s+.*(between|against|with)\s+(hdfc|icici|sbi|other\s+bank)"
    ]

    @classmethod
    def extract_intent(
        cls, 
        query: str, 
        explicit_bank: Optional[str] = None, 
        explicit_year: Optional[int] = None
    ) -> Dict[str, Any]:
        lowered = query.lower()
        
        # 1. Detect Banks in Query
        detected_banks = []
        for bank_name, patterns in cls.BANK_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, lowered):
                    detected_banks.append(bank_name)
                    break

        # 2. Detect Years in Query (2023-2026, FY23-FY26)
        detected_years = []
        raw_year_matches = re.findall(r"\b(?:20(2[3-6])|fy\s*(?:20)?(2[3-6]))\b", lowered)
        for match in raw_year_matches:
            two_digit = match[0] or match[1]
            if two_digit:
                detected_years.append(int("20" + two_digit))
        
        detected_years = sorted(list(set(detected_years)))

        # 3. Check for Trend / Multi-Year Context
        is_multi_year_trend = any(re.search(pat, lowered) for pat in cls.MULTI_YEAR_TREND_KEYWORDS)
        if len(detected_years) > 1:
            is_multi_year_trend = True

        # 4. Check for Cross-Bank Comparative Context
        is_cross_bank = any(re.search(pat, lowered) for pat in cls.CROSS_BANK_KEYWORDS)
        if len(detected_banks) > 1:
            is_cross_bank = True

        # 5. Resolve Final Bank Filter
        final_bank = None
        if explicit_bank and explicit_bank.upper() != "ALL":
            final_bank = explicit_bank.upper()
        else:
            # If cross-bank comparison requested or multiple banks detected, keep open
            if is_cross_bank:
                final_bank = None
            elif len(detected_banks) == 1:
                # Exactly one bank mentioned and not comparing across banks
                final_bank = detected_banks[0]
            else:
                final_bank = None

        # 6. Resolve Final Year Filter
        final_year = None
        if explicit_year and str(explicit_year).upper() != "ALL":
            try:
                final_year = int(explicit_year)
            except ValueError:
                final_year = None
        else:
            # If multi-year trend requested or multiple years detected, keep open
            if is_multi_year_trend:
                final_year = None
            elif len(detected_years) == 1:
                # Exactly one year targeted and not asking for trend
                final_year = detected_years[0]
            else:
                final_year = None

        intent_desc = "TARGETED_QUERY"
        if is_cross_bank and is_multi_year_trend:
            intent_desc = "CROSS_BANK_MULTI_YEAR_TREND"
        elif is_cross_bank:
            intent_desc = "CROSS_BANK_COMPARISON"
        elif is_multi_year_trend:
            intent_desc = "MULTI_YEAR_TREND"

        return {
            "query": query,
            "detected_banks": detected_banks,
            "detected_years": detected_years,
            "is_cross_bank": is_cross_bank,
            "is_multi_year_trend": is_multi_year_trend,
            "resolved_bank": final_bank,
            "resolved_year": final_year,
            "intent_description": intent_desc
        }

if __name__ == "__main__":
    test_queries = [
        "what is the NPA of hdfs bank in 2026",
        "compare hdfc 2026 w evry other year of same bank",
        "compare gross npa between hdfc and icici in 2026",
        "how did liquidity coverage ratio evolve from 2023 to 2026 for sbi",
        "what was the CAR ratio for all banks in FY25?"
    ]
    
    print("="*75)
    print("           TESTING SMART INTENT & CONTEXT-AWARE EXTRACTION")
    print("="*75)
    for q in test_queries:
        res = SmartIntentExtractor.extract_intent(q)
        print(f"\nQUERY: '{q}'")
        print(f"  Detected Banks: {res['detected_banks']} | Detected Years: {res['detected_years']}")
        print(f"  Intent:         {res['intent_description']}")
        print(f"  RESOLVED:       Bank={res['resolved_bank'] or 'ALL'}, Year={res['resolved_year'] or 'ALL'}")

