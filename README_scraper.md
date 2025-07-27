# Aven Support Page Scraper

This project provides two Python scripts to scrape FAQ questions and answers from the Aven support page (https://www.aven.com/support):

1. **Selenium Version** (`aven_support_scraper.py`) - Uses browser automation for dynamic content
2. **Requests Version** (`aven_support_scraper_requests.py`) - Uses HTTP requests for static content (no browser required)

## Features

- Extracts FAQ questions and answers from the Aven support page
- Handles dynamic content and lazy-loaded elements
- Multiple extraction strategies (text-based and DOM-based)
- Saves results in both JSON and text formats
- Comprehensive logging and error handling
- Configurable headless mode

## Prerequisites

### For Selenium Version:
1. **Python 3.7+** installed on your system
2. **Chrome browser** installed
3. **ChromeDriver** (will be automatically managed by webdriver-manager)

### For Requests Version:
1. **Python 3.7+** installed on your system
2. **No browser required** - works with HTTP requests only

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. The script will automatically download and manage ChromeDriver for you.

## Usage

### Option 1: Selenium Version (Recommended for dynamic content)

Run the Selenium scraper:
```bash
python aven_support_scraper.py
```

Or test it:
```bash
python test_scraper.py
```

### Option 2: Requests Version (No browser required)

Run the requests-based scraper:
```bash
python aven_support_scraper_requests.py
```

Or test it:
```bash
python test_scraper_requests.py
```

### Custom Usage

#### Selenium Version:
```python
from aven_support_scraper import AvenSupportScraper

# Create scraper instance
scraper = AvenSupportScraper(headless=False)  # Set to False to see the browser

# Scrape the FAQ content
faq_items = scraper.scrape()

# Save results
scraper.save_to_json(faq_items, "my_faq_data.json")
scraper.save_to_txt(faq_items, "my_faq_data.txt")
```

#### Requests Version:
```python
from aven_support_scraper_requests import AvenSupportScraperRequests

# Create scraper instance
scraper = AvenSupportScraperRequests()

# Scrape the FAQ content
faq_items = scraper.scrape()

# Save results
scraper.save_to_json(faq_items, "my_faq_data.json")
scraper.save_to_txt(faq_items, "my_faq_data.txt")
```

## Output Format

The scraper returns a list of dictionaries, where each dictionary contains:

```json
{
  "question": "The FAQ question text",
  "answer": "The corresponding answer text", 
  "source_url": "https://www.aven.com/support"
}
```

## Output Files

### Selenium Version:
1. **`aven_support_faq.json`** - Structured JSON data
2. **`aven_support_faq.txt`** - Human-readable text format

### Requests Version:
1. **`aven_support_faq_requests.json`** - Structured JSON data
2. **`aven_support_faq_requests.txt`** - Human-readable text format

## Configuration Options

### Headless Mode
- Set `headless=True` (default) to run without opening a browser window
- Set `headless=False` to see the browser in action (useful for debugging)

### Timeout Settings
- Modify the `timeout` parameter in `wait_for_page_load()` method
- Default is 30 seconds

## Troubleshooting

### Common Issues

#### Selenium Version:
1. **Chrome not found**: Install Google Chrome browser from https://www.google.com/chrome/
2. **ChromeDriver not found**: The script uses webdriver-manager to automatically download ChromeDriver. Make sure you have internet connectivity.
3. **Page not loading**: The script includes multiple fallback strategies. If the page structure changes, the script will attempt different extraction methods.

#### Requests Version:
1. **No FAQ items found**: The content might be loaded dynamically with JavaScript. Try the Selenium version instead.
2. **Network errors**: Check your internet connection and firewall settings.
3. **Page structure changes**: The website might have updated its HTML structure.

### Which Version to Use?

- **Use Selenium Version** if:
  - The website uses JavaScript to load content
  - You need to interact with dynamic elements
  - The requests version doesn't find content

- **Use Requests Version** if:
  - You don't have Chrome installed
  - You want faster execution
  - The content is static HTML

### Debug Mode

#### Selenium Version:
To debug issues, run the scraper in non-headless mode:
```python
scraper = AvenSupportScraper(headless=False)
```

This will open a browser window so you can see what's happening.

#### Requests Version:
To debug issues, you can print the HTML content:
```python
scraper = AvenSupportScraperRequests()
html_content = scraper.fetch_page()
print(html_content[:1000])  # Print first 1000 characters
```

## Logging

The script provides detailed logging output including:
- Page load status
- Content extraction progress
- Number of items found
- Any errors encountered

## Legal Considerations

- This scraper is for educational and personal use
- Always respect the website's robots.txt file
- Consider implementing delays between requests if scraping multiple pages
- Check the website's terms of service before scraping

## Dependencies

### Selenium Version:
- `selenium>=4.15.0` - Web automation framework
- `webdriver-manager>=4.0.0` - Automatic WebDriver management

### Requests Version:
- `requests>=2.31.0` - HTTP library
- `beautifulsoup4>=4.12.0` - HTML parsing
- `lxml>=4.9.0` - XML/HTML parser

## License

This script is provided as-is for educational purposes. Use responsibly and in accordance with the target website's terms of service. 