# IPSTA Black Pepper Price Scraper

An automated Python pipeline designed to monitor, scrape, and structure daily black pepper market rates from the India Pepper and Spice Trade Association (IPSTA). This tool dynamically fetches daily market report PDFs, robustly extracts table data across varying layouts, and compiles spot rates into a continuous time-series CSV for market analysis and dashboarding.

## Features

* **Dynamic Web Scraping:** Utilizes `BeautifulSoup4` to automatically locate and parse new daily market report PDFs from the IPSTA source directory.
* **Robust PDF Extraction:** Employs `pdfplumber` and flexible regex parsing to extract contract pricing (Garbled, Ungarbled, 500 GL) while seamlessly bypassing complex table grids, pipes (`|`), and formatting inconsistencies.
* **Idempotent Data Storage:** Safely appends new daily records to `ipsta_rates.csv`. Automatically checks for existing dates to prevent duplicate rows, ensuring clean time-series data.
* **Volume Tracking:** Extracts daily trade volumes alongside Open, High, Low, and Close metrics.

## Tech Stack

* **Language:** Python 3.11+
* **Libraries:** `requests`, `beautifulsoup4`, `pdfplumber`, `pandas`

## Project Structure

```text
black-pepper-price-scraper/
│
├── src/
│   ├── parser.py            # Orchestrates the web scraping and link extraction
│   └── pdf_extractor.py     # Handles PDF downloading, parsing, and CSV appending
│
├── data/
│   └── pdf_links.csv        # Log of extracted PDF target URLs
│
├── ipsta_rates.csv          # Master time-series dataset of daily market rates
└── README.md








