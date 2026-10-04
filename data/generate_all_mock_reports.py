import os
import fitz  # PyMuPDF

ALL_REPORTS = {
    # ==================== HDFC BANK ====================
    "data/reports/hdfc_fy23.pdf": {
        "bank": "HDFC",
        "year": "2023",
        "pages": [
            "HDFC Bank - Annual Report FY2022-23\n\nExecutive Overview:\nHDFC Bank sustained robust balance sheet growth in FY2023 prior to the mega-merger. Total deposits grew 20.8% YoY to Rs 18,83,395 crore. Net profit rose by 19.3% to Rs 44,109 crore. Capital Adequacy Ratio (CAR) remained robust at 19.3% against regulatory minimum of 11.5%.",
            "1. Credit Risk Management (FY2023):\nAsset quality remained exceptional across commercial, rural, and retail lending. Gross Non-Performing Assets (GNPA) stood at 1.12%, while Net NPA was 0.27%. Provision Coverage Ratio (PCR) was strong at 75.8%. Total slippages were contained at 1.4% of advances.",
            "2. Liquidity and Market Risk (FY2023):\nAverage Liquidity Coverage Ratio (LCR) was 118% for the fiscal year. Net Interest Margin (NIM) stood at 4.10%. The bank maintained high credit discipline with total advances growing 16.9%."
        ]
    },
    "data/reports/hdfc_fy24.pdf": {
        "bank": "HDFC",
        "year": "2024",
        "pages": [
            "HDFC Bank - Annual Report FY2023-24\n\nExecutive Overview:\nFY2024 marked the historic merger of parent entity HDFC Limited into HDFC Bank. The combined balance sheet expanded significantly, with total advances reaching Rs 24,84,000 crore. Capital Adequacy Ratio stood at 18.8%.",
            "1. Credit Risk Management (FY2024):\nFollowing merger integration of the mortgage book, Gross NPA stood at 1.24% in FY2024, and Net NPA was 0.33%. Provision Coverage Ratio (PCR) was 74.0%. Credit costs were proactively managed at 0.42%.",
            "2. Liquidity and Market Risk (FY2024):\nThe average daily Liquidity Coverage Ratio (LCR) was 115%. Net Interest Margin (NIM) moderated to 3.63% due to high-cost wholesale liabilities of HDFC Limited being integrated onto the bank's books."
        ]
    },
    "data/reports/hdfc_fy25.pdf": {
        "bank": "HDFC",
        "year": "2025",
        "pages": [
            "HDFC Bank - Annual Report FY2024-25\n\nExecutive Overview:\nHDFC Bank delivered resilient operational performance in FY2025. Total deposits grew by 16.5% year-on-year, driven by robust retail franchise expansion. Capital Adequacy Ratio (CAR) was maintained at 18.8%.",
            "1. Credit Risk Management (FY2025):\nCredit risk remained well-contained across wholesale and retail portfolios. In FY2025, the Gross Non-Performing Assets (GNPA) stood at 1.33%, while Net NPA was 0.38%. Provision Coverage Ratio (PCR) was maintained at 74.2%.",
            "2. Liquidity and Market Risk (FY2025):\nLiquidity Coverage Ratio (LCR) averaged 112% for the fiscal year, well above the regulatory threshold of 100%. Net Interest Margin (NIM) was 3.55% as borrowing costs moderated."
        ]
    },
    "data/reports/hdfc_fy26.pdf": {
        "bank": "HDFC",
        "year": "2026",
        "pages": [
            "HDFC Bank - Annual Report FY2025-26\n\nExecutive Overview:\nIn FY2026, HDFC Bank achieved full balance-sheet optimization post-merger. Return on Assets (RoA) reached 1.95%. Digital onboarding accounted for 88% of all new accounts.",
            "1. Credit Risk Management (FY2026):\nAsset quality strengthened as Gross NPA declined to 1.22% in FY2026. Net NPA fell to 0.33%. Loan loss provisioning was increased by 15% to maintain a Provision Coverage Ratio (PCR) of 76.5%.",
            "2. Liquidity and Market Risk (FY2026):\nLiquidity Coverage Ratio (LCR) rebounded to an average of 118%. Net Interest Margin (NIM) stabilized at 3.40%. Capital Adequacy Ratio (CAR) stood at 16.5% with strong Tier 1 capital cushion."
        ]
    },

    # ==================== ICICI BANK ====================
    "data/reports/icici_fy23.pdf": {
        "bank": "ICICI",
        "year": "2023",
        "pages": [
            "ICICI Bank - Annual Report FY2022-23\n\nExecutive Summary:\nICICI Bank delivered broad-based profit growth of 36.7% in FY2023 with net profit at Rs 31,896 crore. Return on Equity (ROE) expanded to 17.5%. Capital Adequacy Ratio (CAR) stood at 18.34%.",
            "1. Credit Risk & Asset Quality (FY2023):\nAsset quality showed dramatic turnaround. Gross NPA ratio decreased to 2.81% in FY2023 (down from 3.60% in FY22). Net NPA ratio was 0.48%. Provision Coverage Ratio (PCR) reached an industry-leading 82.8%.",
            "2. Liquidity & Treasury (FY2023):\nDaily average Liquidity Coverage Ratio (LCR) was 124%. Net Interest Margin (NIM) was robust at 4.48%, benefiting from repo rate hikes and strong CASA ratio of 45.8%."
        ]
    },
    "data/reports/icici_fy24.pdf": {
        "bank": "ICICI",
        "year": "2024",
        "pages": [
            "ICICI Bank - Annual Report FY2023-24\n\nExecutive Summary:\nCore operating profit grew 18.3% YoY in FY2024. Total domestic loans grew 16.8%. Capital Adequacy Ratio was 16.63% with Common Equity Tier-1 (CET-1) at 15.9%.",
            "1. Credit Risk & Asset Quality (FY2024):\nGross Non-Performing Assets (GNPA) decreased to 2.16% in FY2024, down from 2.81% in FY2023. Net NPA improved to 0.42%. Recoveries and loan upgrades totaled Rs 5,400 crore. Provision Coverage Ratio was 80.3%.",
            "2. Liquidity & Capital Management (FY2024):\nThe average daily Liquidity Coverage Ratio (LCR) was 122%. Net Interest Margin (NIM) reached a multi-year high of 4.53% due to high-yielding retail assets."
        ]
    },
    "data/reports/icici_fy25.pdf": {
        "bank": "ICICI",
        "year": "2025",
        "pages": [
            "ICICI Bank - Annual Report FY2024-25\n\nExecutive Summary:\nICICI Bank maintained consistent risk-calibrated operating profit growth. ROE stood at 18.2%. Capital Adequacy Ratio remained safe at 16.40%.",
            "1. Credit Risk & Asset Quality (FY2025):\nCredit quality reached historic bests. Gross NPA declined to 1.95% in FY2025, while Net NPA reached 0.35%. Credit cost remained rock solid at 45 basis points. Provision Coverage Ratio was 79.5%.",
            "2. Liquidity & Market Risk (FY2025):\nLiquidity Coverage Ratio (LCR) stood at 122% on an average daily basis. Net Interest Margin (NIM) was 4.40%, reflecting resilient low-cost deposit mobilization."
        ]
    },
    "data/reports/icici_fy26.pdf": {
        "bank": "ICICI",
        "year": "2026",
        "pages": [
            "ICICI Bank - Annual Report FY2025-26\n\nExecutive Summary:\nIn FY2026, ICICI Bank sustained industry-leading profitability with ROE at 18.5%. Digital transactions accounted for 92% of total retail transactions. Capital Adequacy Ratio stood at 16.10%.",
            "1. Credit Risk & Asset Quality (FY2026):\nCredit discipline remained robust with Gross NPA declining further to 1.74% in FY2026. Net NPA fell to 0.30%. Unsecured retail underwriting was tightened. Provision Coverage Ratio (PCR) strengthened to 81.2%.",
            "2. Liquidity & Market Risk (FY2026):\nLiquidity Coverage Ratio (LCR) stood at 126% in FY2026. Net Interest Margin (NIM) was 4.25% due to competitive deposit repricing."
        ]
    },

    # ==================== STATE BANK OF INDIA (SBI) ====================
    "data/reports/sbi_fy23.pdf": {
        "bank": "SBI",
        "year": "2023",
        "pages": [
            "State Bank of India - Annual Report FY2022-23\n\nExecutive Summary:\nSBI recorded highest-ever net profit of Rs 50,232 crore in FY2023, growing 58.6% YoY. Total balance sheet crossed Rs 55 lakh crore. Capital Adequacy Ratio (CAR) stood at 14.68%.",
            "1. Credit Risk & Asset Quality (FY2023):\nGross NPA ratio dropped below 4% to 3.98% in FY2023, down from 4.91% in FY22. Net NPA was 0.67%. Provision Coverage Ratio (PCR) improved to 76.4%. Corporate credit book showed near-zero fresh slippages.",
            "2. Liquidity & Treasury (FY2023):\nSBI maintained superior systemic liquidity with average LCR of 145%, well ahead of regulatory mandates. Net Interest Margin (NIM) expanded to 3.37%."
        ]
    },
    "data/reports/sbi_fy24.pdf": {
        "bank": "SBI",
        "year": "2024",
        "pages": [
            "State Bank of India - Annual Report FY2023-24\n\nExecutive Summary:\nSBI surpassed Rs 61,000 crore in annual net profit for FY2024. Return on Assets (RoA) reached 1.04%. Capital Adequacy Ratio was 14.28% with Tier 1 capital at 12.11%.",
            "1. Credit Risk & Asset Quality (FY2024):\nAsset quality improved significantly with Gross NPA falling to 3.14% in FY2024. Net NPA dropped to 0.57%. Provision Coverage Ratio (PCR) was 75.0%. Retail personal loans maintained default rate under 0.70%.",
            "2. Liquidity & Resource Management (FY2024):\nAverage Liquidity Coverage Ratio (LCR) stood at 138%. Domestic Net Interest Margin (NIM) was 3.28% as domestic deposit costs rose across the banking system."
        ]
    },
    "data/reports/sbi_fy25.pdf": {
        "bank": "SBI",
        "year": "2025",
        "pages": [
            "State Bank of India - Annual Report FY2024-25\n\nExecutive Summary:\nSBI continued its leadership as India's largest lender, with advances crossing Rs 40 lakh crore in FY2025. RoE remained strong at 19.1%. Capital Adequacy Ratio was 14.15%.",
            "1. Credit Risk & Asset Quality (FY2025):\nGross NPA declined to 2.72% in FY2025, reaching a multi-decade low. Net NPA was 0.52%. Provision Coverage Ratio stood at 75.2%. SME loan quality showed marked improvement.",
            "2. Liquidity & Market Risk (FY2025):\nLiquidity Coverage Ratio (LCR) averaged 132% in FY2025. Net Interest Margin (NIM) was 3.22%. Low-cost CASA deposits represented 41.2% of total deposit franchise."
        ]
    },
    "data/reports/sbi_fy26.pdf": {
        "bank": "SBI",
        "year": "2026",
        "pages": [
            "State Bank of India - Annual Report FY2025-26\n\nExecutive Summary:\nIn FY2026, SBI crossed Rs 75,000 crore in net profit, propelled by digital transformation via YONO 3.0. Capital Adequacy Ratio improved to 14.30% with CET-1 at 11.20%.",
            "1. Credit Risk & Asset Quality (FY2026):\nGross NPA further contracted to 2.35% in FY2026. Net NPA fell to 0.46%. Provision Coverage Ratio (PCR) rose to 76.8%. Credit cost reduced to 32 basis points.",
            "2. Liquidity & Capital Management (FY2026):\nAverage Liquidity Coverage Ratio (LCR) was 135%. Net Interest Margin (NIM) stabilized at 3.18%. Total deposits reached Rs 52 lakh crore."
        ]
    }
}

os.makedirs("data/reports", exist_ok=True)
count = 0
for filepath, data in ALL_REPORTS.items():
    doc = fitz.open()
    for page_text in data["pages"]:
        page = doc.new_page()
        page.insert_textbox(fitz.Rect(50, 50, 550, 750), page_text, fontsize=11)
    doc.save(filepath)
    doc.close()
    count += 1
    print(f"Generated ({count}/12): {filepath}")

print(f"\nSuccessfully generated {count} financial reports covering HDFC, ICICI, and SBI across FY2023-FY2026.")

