import logging
import random
from fake_useragent import UserAgent

def setup_logger():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def get_random_headers():
    """Generate random headers to avoid bot detection"""
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def clean_text(text):
    """Clean and normalize text data"""
    if text:
        return ' '.join(text.strip().split())
    return "N/A"

def format_price(price_text):
    """Extract and format price from text"""
    if not price_text or price_text == "N/A":
        return "N/A"
    
    # Remove common currency symbols and commas
    price_text = price_text.replace('$', '').replace(',', '').replace('€', '').replace('£', '')
    
    # Extract numbers
    numbers = ''.join(filter(str.isdigit, price_text))
    
    if numbers:
        return f"${int(numbers):,}"
    return "N/A"