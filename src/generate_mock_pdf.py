import fitz
import os

def create_mock_report():
    os.makedirs(r"../data/reports", exist_ok=True)
    doc = fitz.open()

    # Page 1: Title
    page1 = doc.new_page()
    page1.insert_text((50, 70), "HDFC Bank Annual Report FY2026", fontsize=24)
    page1.insert_text((50, 120), "Management Discussion and Analysis", fontsize=16)
    page1.insert_text((50, 160), "This report outlines the financial performance, risk management,", fontsize=12)
    page1.insert_text((50, 180), "and strategic outlook for HDFC Bank for the financial year 2025-2026.", fontsize=12)

    # Page 2: Credit Risk
    page2 = doc.new_page()
    page2.insert_text((50, 50), "1. Credit Risk Management", fontsize=18)
    text_credit = """Credit risk is the primary risk for the bank. In FY2026, our risk 
framework remained resilient despite global headwinds. 

The Gross Non-Performing Assets (GNPA) ratio for HDFC Bank 
in FY2026 stood at 1.22%, representing a slight improvement from 
the previous year. The Net NPA ratio was maintained at a healthy 0.33%.

Our loan loss provisioning was proactively increased by 15% to 
buffer against unexpected stress in the unsecured lending portfolio.
The bank's strict underwriting standards have ensured that asset 
quality remains industry-leading."""
    page2.insert_text((50, 90), text_credit, fontsize=12)

    # Page 3: Liquidity & Market Risk
    page3 = doc.new_page()
    page3.insert_text((50, 50), "2. Liquidity and Market Risk", fontsize=18)
    text_liquidity = """Liquidity risk management ensures we have sufficient funds to meet 
our obligations. The Liquidity Coverage Ratio (LCR) for FY2026 
averaged 118%, which is comfortably above the regulatory 
requirement of 100%.

Market Risk:
The bank's treasury operations were affected by interest rate volatility. 
However, the Net Interest Margin (NIM) remained stable at 3.4% 
due to effective repricing of the loan book. 

Capital Adequacy Ratio (CAR) stands at 16.5%, with Tier 1 Capital 
forming the bulk of it, providing a strong cushion for future growth."""
    page3.insert_text((50, 90), text_liquidity, fontsize=12)

    doc.save(r"../data/reports/hdfc_fy26.pdf")
    print("Created data/reports/hdfc_fy26.pdf")

if __name__ == "__main__":
    create_mock_report()
