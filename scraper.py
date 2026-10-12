"""
Smart Web Scraper & Data Extraction Pipeline
Author: Fajar Setya (@jarfva)
Description: Production-ready Python web scraping script with retry mechanisms,
custom headers, structured data parsing, and multi-page crawling.
"""

import time
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Scraper")

BASE_URL = "http://books.toscrape.com/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_page(url, retries=3, delay=1):
    """Fetches HTML content with error handling and retry mechanism."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                return response.text
            logger.warning(f"Status code {response.status_code} for {url}. Attempt {attempt}/{retries}")
        except requests.RequestException as e:
            logger.warning(f"Request failed: {e}. Attempt {attempt}/{retries}")
        time.sleep(delay)
    return None


def parse_page(html, current_url):
    """Parses book listings from HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    products = []

    articles = soup.find_all("article", class_="product_pod")
    for article in articles:
        # Title
        title_tag = article.h3.find("a")
        title = title_tag.get("title", title_tag.text.strip())
        relative_link = title_tag.get("href")
        product_url = urljoin(current_url, relative_link)

        # Image URL
        img_tag = article.find("img", class_="thumbnail")
        img_relative = img_tag.get("src") if img_tag else ""
        image_url = urljoin(current_url, img_relative)

        # Price
        price_tag = article.find("p", class_="price_color")
        price_text = price_tag.text.strip() if price_tag else "£0.00"
        # Remove currency symbol
        price_clean = float(price_text.replace("£", "").replace("Â", "").strip())

        # Rating
        rating_classes = article.find("p", class_="star-rating").get("class", [])
        rating_word = next((c for c in rating_classes if c in RATING_MAP), "None")
        rating = RATING_MAP.get(rating_word, 0)

        # Availability
        availability_tag = article.find("p", class_="instock availability")
        availability = availability_tag.text.strip() if availability_tag else "Unknown"

        products.append({
            "title": title,
            "price_gbp": price_clean,
            "rating": rating,
            "stars": "★" * rating + "☆" * (5 - rating),
            "availability": availability,
            "image_url": image_url,
            "product_url": product_url
        })

    # Check for next page
    next_li = soup.find("li", class_="next")
    next_url = None
    if next_li and next_li.find("a"):
        next_rel = next_li.find("a").get("href")
        next_url = urljoin(current_url, next_rel)

    return products, next_url


def scrape_catalog(max_pages=5):
    """Orchestrates multi-page catalog scraping."""
    logger.info(f"Starting scraping pipeline (Crawling up to {max_pages} pages)...")
    current_url = START_URL
    all_products = []
    page_count = 0

    while current_url and page_count < max_pages:
        page_count += 1
        logger.info(f"Scraping Page {page_count}: {current_url}")
        html = fetch_page(current_url)
        if not html:
            logger.error(f"Failed to retrieve {current_url}. Stopping crawl.")
            break

        products, next_url = parse_page(html, current_url)
        all_products.extend(products)
        logger.info(f"Page {page_count} parsed: {len(products)} items found.")
        current_url = next_url
        time.sleep(0.5)  # Polite crawling delay

    df = pd.DataFrame(all_products)
    logger.info(f"Scraping finished. Total items extracted: {len(df)}")
    return df


if __name__ == "__main__":
    df = scrape_catalog(max_pages=3)
    print(df.head())
