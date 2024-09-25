# Cars Scraper

A Scrapy project that scrapes car listings from Cars.com, specifically targeting Kia Cadenza vehicles. This project collects details such as the car's make, model, year, price, and seller's contact information, and saves the results in a CSV format.

## Features

- Scrapes car details from Cars.com
- Supports pagination to gather multiple listings
- Exports data to a CSV file
- Configurable settings for request limits and delays

## Requirements

- Python 3.11
- Scrapy

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/cars-scraper.git
   cd cars-scraper
   pip install -r requirements.txt
   ```
   
## Run the Spider

- scrapy crawl cars -o output.csv
