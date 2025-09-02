# src/selenium_scraper.py
import os
import time
import random
import logging
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class RealEstateScraper:
    def __init__(self, headless=True, delay=2):
        self.delay = delay
        self.headless = headless
        self.logger = self.setup_logging()
        self.driver = self.setup_driver()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("logs/scraper.log"),
                logging.StreamHandler(),
            ],
        )
        return logging.getLogger(__name__)

    def setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-quic")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-3d-apis")

        driver_path = ChromeDriverManager().install()
        driver_path = str(Path(driver_path).with_name("chromedriver.exe"))
        self.logger.info(f"Using ChromeDriver executable: {driver_path}")

        service = Service(driver_path,log_path=os.devnull)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def fetch_page(self, url, selector):
        """Fetch a page and wait for listings to load"""
        try:
            self.driver.get(url)
            time.sleep(self.delay + random.uniform(0, 2))
            WebDriverWait(self.driver, 12).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return self.driver.page_source
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def parse_listings(self, html, site="realtor"):
        """Parse listings based on site structure"""
        soup = BeautifulSoup(html, "html.parser")
        listings = []

        if site == "realtor":
            property_cards = soup.find_all("div", {"data-testid": "property-card"})
            for card in property_cards:
                try:
                    title_elem = card.find("div", {"data-testid": "property-card-address"})
                    price_elem = card.find("div", {"data-testid": "property-card-price"})
                    link_elem = card.find("a", {"data-testid": "property-card-link"})

                    title = self.clean_text(title_elem.text if title_elem else "N/A")
                    price = self.format_price(price_elem.text if price_elem else "N/A")
                    location = title  # same as address
                    link = (
                        f"https://www.realtor.com{link_elem['href']}"
                        if link_elem and link_elem.get("href")
                        else "N/A"
                    )

                    listings.append(
                        {"title": title, "price": price, "location": location, "link": link}
                    )
                except Exception as e:
                    self.logger.warning(f"Error parsing card: {e}")

        # TODO: Add Redfin selectors separately

        return listings

    def clean_text(self, text):
        return " ".join(text.strip().split()) if text else "N/A"

    def format_price(self, price_text):
        if not price_text or price_text == "N/A":
            return "N/A"
        cleaned = (
            price_text.replace("$", "")
            .replace(",", "")
            .replace("€", "")
            .replace("£", "")
        )
        digits = "".join(filter(str.isdigit, cleaned))
        return f"${int(digits):,}" if digits else "N/A"

    def scrape_pages(self, base_url, site="realtor", max_pages=3):
        all_listings = []
        selector = '[data-testid="property-card"]' if site == "realtor" else "div.HomeCard"

        for page in range(1, max_pages + 1):
            self.logger.info(f"Scraping page {page}...")
            url = f"{base_url}&pg={page}" if "?" in base_url else f"{base_url}?pg={page}"
            html = self.fetch_page(url, selector)
            if not html:
                break

            listings = self.parse_listings(html, site=site)
            all_listings.extend(listings)
            self.logger.info(f"Found {len(listings)} listings on page {page}")

            time.sleep(self.delay + random.uniform(0, 2))

            if not listings:
                break

        return all_listings

    def close(self):
        self.driver.quit()
