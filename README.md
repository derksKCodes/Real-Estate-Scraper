 Real Estate Scraper

A Python-based web scraper that extracts real estate property listings from various websites and exports them to multiple formats.

## Features

- Scrapes property details (title, price, location, link)
- Handles pagination to extract multiple pages
- Exports data to CSV, JSON, and Excel formats
- Uses random user agents to avoid detection
- Configurable through JSON files or command line arguments

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd real-estate-scraper
Install dependencies:

bash
pip install -r requirements.txt
Usage
Using a configuration file
Edit config/urls.json to add your target URLs:

json
{
  "urls": [
    "https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA",
    "https://www.realtor.com/realestateandhomes-search/New-York_NY"
  ]
}
Run the scraper:

bash
python src/main.py
Using command line arguments
bash
# Scrape a single URL
python src/main.py --url "https://www.realtor.com/realestateandhomes-search/San-Francisco_CA"

# Specify maximum pages to scrape
python src/main.py --url "https://www.realtor.com/realestateandhomes-search/Chicago_IL" --max-pages 3

# Custom output path
python src/main.py --url "https://www.realtor.com/realestateandhomes-search/Miami_FL" --output "data/miami_listings"
Output
The scraper generates three files in the data/ directory:

listings.csv - CSV format

listings.json - JSON format

listings.xlsx - Excel format

Each file contains the following fields for each property:

Title

Price

Location

Link

Notes
This scraper is configured for Realtor.com. Other sites may require selector adjustments.

Be respectful when scraping - add delays and don't overwhelm servers.

Websites may change their structure, requiring updates to the selectors.

Always check a website's robots.txt and terms of service before scraping.

Sample Output
Title	Price	Location	Link
123 Main St	$1,200,000	123 Main St, Los Angeles, CA 90001	https://www.realtor.com/realestateandhomes-detail/123-Main-St...
456 Oak Ave	$850,000	456 Oak Ave, Los Angeles, CA 90002	https://www.realtor.com/realestateandhomes-detail/456-Oak-Ave...
text

## Running the Scraper

To run the scraper:

1. Install the dependencies:
```bash
pip install -r requirements.txt
Create the config directory and file:

bash
mkdir -p config
echo '{"urls": ["https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA"]}' > config/urls.json
Run the scraper:

bash
python src/main.py
Sample Output
After running the scraper, you'll get output files in the data directory with content similar to:

listings.csv:

csv
title,price,location,link
"123 Main St","$1,200,000","123 Main St, Los Angeles, CA 90001","https://www.realtor.com/realestateandhomes-detail/123-Main-St..."
"456 Oak Ave","$850,000","456 Oak Ave, Los Angeles, CA 90002","https://www.realtor.com/realestateandhomes-detail/456-Oak-Ave..."
listings.json:

json
[
  {
    "title": "123 Main St",
    "price": "$1,200,000",
    "location": "123 Main St, Los Angeles, CA 90001",
    "link": "https://www.realtor.com/realestateandhomes-detail/123-Main-St..."
  },
  {
    "title": "456 Oak Ave",
    "price": "$850,000",
    "location": "456 Oak Ave, Los Angeles, CA 90002",
    "link": "https://www.realtor.com/realestateandhomes-detail/456-Oak-Ave..."
  }
]
The Excel file will contain the same data in a spreadsheet format.

Important Notes
Website selectors may need to be updated as real estate websites frequently change their HTML structure.

The scraper includes a delay between requests to be respectful to the server.

If you encounter blocking issues, you may need to:

Increase the delay between requests

Use proxy servers

Further randomize request patterns

Always check a website's terms of service and robots.txt before scraping.

This implementation provides a robust foundation for scraping real estate data that can be extended with additional features as needed.