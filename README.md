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
  
## Installation

1. Clone the repository:
`git clone https://github.com/preyesh2002/black-pepper-price-scraper.git`
`cd black-pepper-price-scraper`

2. Install the required dependencies:
`pip install requests beautifulsoup4 pdfplumber pandas`

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
└── README.md## Usage

```
To execute the pipeline manually, run the parser module from the root directory. The script will fetch the latest HTML, identify target PDFs, parse the rates, and update the master CSV:

`python src/parser.py`

### Output Data Format (`ipsta_rates.csv`)

| date | spot_differential | garbled_open | garbled_high | garbled_low | garbled_close | ungarbled_open | gl500_close | trade_volume_tons |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-09-17 | MINUS ONE HUNDRED | 72300 | 72300 | 72300 | 72300 | 70300 | 69300 | 34 |

## Configuration

No external API keys are required to run this scraper. Ensure that your execution environment has write access to the root directory so the script can successfully append data to `ipsta_rates.csv` and `data/pdf_links.csv`.

## Roadmap

* **Cloud Automation:** Implement GitHub Actions scheduled workflows to execute the scraping pipeline daily at 8:00 PM IST autonomously.
* **Data Visualization:** Connect `ipsta_rates.csv` to a Streamlit dashboard to track moving averages and price volatility over time.

## Contributing

Contributions are welcome. If you find a bug in the PDF extraction logic (e.g., if IPSTA changes their PDF layout) or want to add visualization features:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.


## License

Distributed under the MIT License. See `LICENSE` for more information.



## Contact

Preyesh C P - [GitHub Profile](https://github.com/preyesh2002)

Project Link: [https://github.com/preyesh2002/black-pepper-price-scraper](https://github.com/preyesh2002/black-pepper-price-scraper)








