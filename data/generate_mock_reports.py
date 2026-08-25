import fitz  # PyMuPDF
import os

REPORTS = {
    "data/reports/hdfc_fy25.pdf": {
        "bank": "HDFC",
        "year": "2025",
        "pages": [
            "HDFC Bank - Annual Report FY2024-25\n\nExecutive Overview:\nHDFC Bank delivered resilient operational performance in FY2025. Total deposits grew by 16.5% year-on-year, driven by robust retail franchise expansion. Capital Adequacy Ratio (CAR) remained strong at 18.8%.",
            "1. Credit Risk Management (FY2025):\nCredit risk remained well-contained across wholesale and retail portfolios. In FY2025, the Gross Non-Performing Assets (GNPA) stood at 1.33%, while Net NPA was 0.38%. Provision Coverage Ratio (PCR) was maintained at 74.2%.",
            "2. Liquidity and Market Risk (FY2025):\nLiquidity Coverage Ratio (LCR) averaged 112% for the fiscal year, well above the regulatory threshold of 100%. Net Interest Margin (NIM) was 3.55% as borrowing costs moderated."
        ]
    },
    "data/reports/icici_fy25.pdf": {
        "bank": "ICICI",
        "year": "2025",
        "pages": [
            "ICICI Bank - Annual Report FY2024-25\n\nExecutive Summary:\nICICI Bank demonstrated solid growth across all business segments in FY2025. Total advances increased by 17.2% YoY. Capital Adequacy Ratio stood at 16.63% with CET-1 ratio at 15.9%.",
            "1. Credit Risk & Asset Quality (FY2025):\nAsset quality continued to improve significantly. Gross Non-Performing Assets (GNPA) decreased to 2.16% in FY2025 (compared to 2.76% in FY2024). Net NPA was 0.42%. Recoveries and upgrades from non-performing loans totaled Rs 5,400 crore.",
            "2. Liquidity & Capital Management (FY2025):\nThe average daily Liquidity Coverage Ratio (LCR) was 122%. Net Interest Margin (NIM) for FY2025 was 4.40%, reflecting strong low-cost CASA deposit mobilization."
        ]
    },
    "data/reports/icici_fy26.pdf": {
        "bank": "ICICI",
        "year": "2026",
        "pages": [
            "ICICI Bank - Annual Report FY2025-26\n\nExecutive Summary:\nIn FY2026, ICICI Bank sustained industry-leading profitability with ROE at 18.5%. Digital transactions accounted for 92% of total retail transactions.",
            "1. Credit Risk & Asset Quality (FY2026):\nCredit discipline remained robust with Gross NPA declining further to 1.95% in FY2026. Net NPA fell to 0.35%. Credit cost was stable at 45 basis points. Unsecured retail loans were tightened with conservative underwriting.",
            "2. Liquidity & Market Risk (FY2026):\nLiquidity Coverage Ratio (LCR) stood at 126% in FY2026. Net Interest Margin (NIM) moderated slightly to 4.25% due to competitive deposit repricing."
        ]
    }
}

def generate_pdfs():
    os.makedirs("data/reports", exist_ok=True)
    for filepath, data in REPORTS.items():
        doc = fitz.open()
        for page_text in data["pages"]:
            page = doc.new_page()
            # Insert text at top of page
            page.insert_text(fitz.Point(50, 72), page_text, fontsize=12)
        doc.save(filepath)
        doc.close()
        print(f"Generated: {filepath}")

if __name__ == "__main__":
    generate_pdfs()
