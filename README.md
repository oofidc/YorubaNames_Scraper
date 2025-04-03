
# Yorùbá Names Scraper & API

This project provides a web scraper for information from the yorubaname.com website and an accompanying Flask API to serve the scraped data.

## Features

- Scrapes Yorùbá names organized alphabetically
- Provides detailed information about individual names including:
  - Name meaning
  - Extended meaning
  - Morphology
  - Gloss (multiple parts)
  - Geolocation
  - Pronunciation URL
  - Variants

## Installation

To run this project, you'll need to install the following dependencies:
pip install beautifulsoup4 requests flask


## Usage

### Running the Scraper

To scrape all available names:
```
from YorubaNamesScraper import YorubaNamesScraper

scraper = YorubaNamesScraper() all_names = scraper.get_all_names()

for name in all_names: print(name)
```

To get information about a specific name:
```
python from YorubaNamesScraper import YorubaNamesScraper

scraper = YorubaNamesScraper() name_info = scraper.get_name_info("Oyin")

print(json.dumps(name_info, indent=2))
```


### Using the API

To use the Flask API, run the server:

bash python YorubaNamesAPI.py


Then make HTTP requests to the following endpoints:

- `GET /` - Test route
- `GET /names-by-first-character/<character>` - Get names starting with <character>
- `GET /get-all-names/` - Get all names
- `GET /name-info/<name>` - Get detailed information about <name>

Example API usage:
```
python import requests

response = requests.get('http://localhost:5000/name-info/Oyin') print(response.json())
```

## Notes

- The scraper uses BeautifulSoup for HTML parsing and requests for making HTTP requests.
- The API uses Flask to create a simple web server.
- Error handling is implemented in both the scraper and API to handle potential issues with web scraping.
- The scraper caches results to prevent overloading the target website.
- The API returns JSON responses with UTF-8 encoding to properly display special characters.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
This README provides an overview of the project, its features, installation instructions, usage examples for both the scraper and API, notes on implementation details, contribution guidelines, and licensing information. It should give users a clear understanding of how to use and contribute to the project.