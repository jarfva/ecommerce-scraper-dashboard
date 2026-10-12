# 🚀 E-Commerce Web Scraper & Market Intelligence Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![BeautifulSoup](https://img.shields.io/badge/Library-BeautifulSoup4-orange.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![Pandas](https://img.shields.io/badge/Data-Pandas%20%7C%20OpenPyXL-brightgreen.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> Production-grade Python web scraping pipeline that extracts e-commerce product catalogs, performs data cleaning, exports executive-styled Excel spreadsheets with KPI summaries, and visualizes datasets in an interactive web dashboard.

---

## 📌 Project Overview
Many e-commerce brands, agencies, and market researchers waste dozens of manual hours every week tracking competitor prices and product availability. This automated pipeline demonstrates an end-to-end extraction and reporting solution:

1. **Automated Scraping**: Multi-page traversal with polite crawling delays, custom browser headers, and exponential retry handling.
2. **Structured Cleaning**: Converts raw HTML into clean numeric data types (prices, star ratings, stock availability).
3. **Agency-Grade Excel Export**: Styled with custom typography, auto-fit columns, zebra-striping, auto-filters, and an Executive Summary sheet featuring KPI calculation cards.
4. **Interactive Web Dashboard**: A lightweight, responsive dark-mode dashboard built with Tailwind CSS and Chart.js for instant filtering, search, and data visualization.

---

## 🛠️ Architecture & Tech Stack

```
[ Target Website / Catalog ]
            │ (HTTP Requests + Headers + Retries)
            ▼
[ Scraper Engine (BeautifulSoup4 + Requests) ]
            │ (Extracted Records)
            ▼
[ Data Processing & Normalization (Pandas) ]
      ┌─────┴────────────────────────┐
      ▼                              ▼
[ Styled Excel Exporter ]    [ Interactive Web Dashboard ]
  • Executive KPI Sheet        • Live Search & Filter Bar
  • Formatted Catalog Sheet    • Rating Distribution (Chart.js)
  • Auto-Filters & Styling     • Responsive Dark Mode UI
```

- **Language**: Python 3.12+
- **Extraction**: `requests`, `beautifulsoup4`
- **Data Engineering**: `pandas`, `openpyxl`
- **Frontend / Dashboard**: HTML5, Tailwind CSS, Chart.js, FontAwesome

---

## 📊 Key Deliverables

| Deliverable | Description | Format |
| :--- | :--- | :--- |
| **Clean Raw Data** | Raw dataset backup | `.csv` |
| **Executive Excel Report** | Corporate Navy themed report with KPI summary cards & auto-filters | `.xlsx` |
| **Interactive Dashboard** | Standalone visual dashboard for client presentation & fast analysis | `.html` |

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jarfva/ecommerce-scraper-dashboard.git
   cd ecommerce-scraper-dashboard
   ```

2. **Install required dependencies:**
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl
   ```

3. **Run the full automated pipeline:**
   ```bash
   python main.py
   ```

4. **View results:**
   - Open `scraped_catalog_report.xlsx` in Microsoft Excel or Google Sheets.
   - Open `dashboard.html` in any web browser to explore the interactive visualizer.

---

## 👨‍💻 Author
**Fajar Setya (@jarfva)**
* Full-Stack Developer & Python Automation Specialist
* Freelance Profiles: [Fastwork](https://fastwork.id/user/jarfva) | [Fiverr](https://www.fiverr.com/jarfva) | [Upwork](https://www.upwork.com/freelancers/~01f02c11dadbf80c0a)
