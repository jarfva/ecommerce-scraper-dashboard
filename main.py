"""
Main Pipeline Runner: Web Scraping to Professional Excel & Interactive Dashboard
Author: Fajar Setya (@jarfva)
"""

import time
import os
from scraper import scrape_catalog
from excel_exporter import export_to_professional_excel
from dashboard_generator import generate_web_dashboard

def run_pipeline():
    print("=" * 60)
    print(">> SMART WEB SCRAPING & AUTOMATION PIPELINE")
    print("   Engineered by: Fajar Setya (@jarfva)")
    print("=" * 60)
    
    start_time = time.time()
    
    # 1. Scrape 5 pages (100 items)
    print("\n[Step 1/4] Extracting live data from e-commerce catalog...")
    df = scrape_catalog(max_pages=5)
    
    if df.empty:
        print("[!] Scraping returned no data. Aborting.")
        return

    # 2. Export Raw CSV
    print("\n[Step 2/4] Saving raw CSV backup...")
    csv_path = "scraped_catalog_raw.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"   -> Saved: {csv_path} ({len(df)} records)")

    # 3. Export Formatted Agency-Grade Excel
    print("\n[Step 3/4] Generating agency-grade Excel report with KPIs...")
    excel_path = "scraped_catalog_report.xlsx"
    export_to_professional_excel(df, output_path=excel_path)
    print(f"   -> Saved: {excel_path} (Formatted with Corporate Navy theme & Auto-filter)")

    # 4. Generate Interactive Web Dashboard
    print("\n[Step 4/4] Building modern interactive HTML Dashboard...")
    html_path = "dashboard.html"
    generate_web_dashboard(df, output_html=html_path, excel_filename=excel_path)
    print(f"   -> Saved: {html_path} (Ready for browser viewing & screenshotting)")

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"[SUCCESS] PIPELINE COMPLETED IN {elapsed:.2f}s!")
    print(f"   * Total Items Extracted: {len(df)}")
    print(f"   * Average Price: GBP {df['price_gbp'].mean():.2f}")
    print(f"   * Excel Report: {os.path.abspath(excel_path)}")
    print(f"   * HTML Dashboard: {os.path.abspath(html_path)}")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
