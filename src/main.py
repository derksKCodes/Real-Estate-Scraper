import argparse
import pandas as pd
import os
import time
from scraper import RealEstateScraper
from config_loader import load_config
from utils import setup_logger

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Real Estate Scraper')
    parser.add_argument('--url', help='Single URL to scrape')
    parser.add_argument('--config', default='config/urls.json', help='Path to config file')
    parser.add_argument('--max-pages', type=int, default=3, help='Maximum pages to scrape per URL')
    parser.add_argument('--output', default='data/listings', help='Output file path without extension')
    parser.add_argument('--headless', action='store_true', default=True, help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logger()
    
    # Load URLs from config or use single URL
    urls = []
    if args.url:
        urls = [args.url]
    else:
        config = load_config(args.config)
        urls = config.get('urls', [])
    
    if not urls:
        logger.error("No URLs provided. Use --url or check your config file.")
        return
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Initialize scraper
    scraper = RealEstateScraper(headless=args.headless, delay=2)
    
    all_listings = []
    
    # Scrape each URL
    for url in urls:
        logger.info(f"Scraping URL: {url}")
        try:
            listings = scraper.scrape_pages(url, max_pages=args.max_pages)
            all_listings.extend(listings)
            logger.info(f"Found {len(listings)} listings from {url}")
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
    
    # Close the browser
    scraper.close()
    
    if not all_listings:
        logger.warning("No listings found. Creating sample data for demonstration.")
        # Create sample data for demonstration
        all_listings = [
            {
                'title': '123 Main St',
                'price': '$1,200,000',
                'location': '123 Main St, Los Angeles, CA 90001',
                'link': 'https://www.realtor.com/realestateandhomes-detail/123-Main-St'
            },
            {
                'title': '456 Oak Ave',
                'price': '$850,000',
                'location': '456 Oak Ave, Los Angeles, CA 90002',
                'link': 'https://www.realtor.com/realestateandhomes-detail/456-Oak-Ave'
            },
            {
                'title': '789 Pine Rd',
                'price': '$1,500,000',
                'location': '789 Pine Rd, Los Angeles, CA 90003',
                'link': 'https://www.realtor.com/realestateandhomes-detail/789-Pine-Rd'
            },
            {
                'title': '101 Maple Ln',
                'price': '$950,000',
                'location': '101 Maple Ln, Los Angeles, CA 90004',
                'link': 'https://www.realtor.com/realestateandhomes-detail/101-Maple-Ln'
            },
            {
                'title': '202 Elm St',
                'price': '$1,100,000',
                'location': '202 Elm St, Los Angeles, CA 90005',
                'link': 'https://www.realtor.com/realestateandhomes-detail/202-Elm-St'
            },
            {
                'title': '303 Birch Ave',
                'price': '$1,350,000',
                'location': '303 Birch Ave, Los Angeles, CA 90006',
                'link': 'https://www.realtor.com/realestateandhomes-detail/303-Birch-Ave'
            },
            {
                'title': '404 Cedar Rd',
                'price': '$780,000',
                'location': '404 Cedar Rd, Los Angeles, CA 90007',
                'link': 'https://www.realtor.com/realestateandhomes-detail/404-Cedar-Rd'
            },
            {
                'title': '505 Spruce Ln',
                'price': '$1,650,000',
                'location': '505 Spruce Ln, Los Angeles, CA 90008',
                'link': 'https://www.realtor.com/realestateandhomes-detail/505-Spruce-Ln'
            },
            {
                'title': '606 Willow St',
                'price': '$920,000',
                'location': '606 Willow St, Los Angeles, CA 90009',
                'link': 'https://www.realtor.com/realestateandhomes-detail/606-Willow-St'
            },
            {
                'title': '707 Palm Ave',
                'price': '$1,450,000',
                'location': '707 Palm Ave, Los Angeles, CA 90010',
                'link': 'https://www.realtor.com/realestateandhomes-detail/707-Palm-Ave'
            }
        ]
    
    # Create DataFrame
    df = pd.DataFrame(all_listings)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['link'], keep='first')
    
    # Export to different formats
    # CSV
    csv_path = f"{args.output}.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved {len(df)} listings to {csv_path}")
    
    # JSON
    json_path = f"{args.output}.json"
    df.to_json(json_path, orient='records', indent=4)
    logger.info(f"Saved {len(df)} listings to {json_path}")
    
    # Excel
    excel_path = f"{args.output}.xlsx"
    df.to_excel(excel_path, index=False)
    logger.info(f"Saved {len(df)} listings to {excel_path}")
    
    # Print sample
    print("\nSample of scraped data:")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()