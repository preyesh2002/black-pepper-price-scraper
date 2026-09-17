# src/pdf_extractor.py

import os
import re
import csv
from urllib.parse import urlparse

import requests
import pdfplumber

CSV_PATH = "ipsta_rates.csv"
DOWNLOAD_DIR = "downloads"
LINKS_CSV_PATH = "data/pdf_links.csv"

FIELDS = [
    "date", "spot_differential",
    "garbled_open", "garbled_high", "garbled_low", "garbled_close",
    "ungarbled_open", "ungarbled_high", "ungarbled_low", "ungarbled_close",
    "gl500_open", "gl500_high", "gl500_low", "gl500_close",
    "trade_volume_tons", "source_url",
]

DATE_RE = re.compile(r"(\d{1,2})\.(\d{1,2})\.(\d{4})")

KEY_MAP = {
    "GARBLED": "garbled",
    "UNGARBLED": "ungarbled",
    "500 GL": "gl500",
}


def download_pdf(url: str) -> str:
    """Downloads a PDF to DOWNLOAD_DIR and returns the local file path."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    filename = os.path.basename(urlparse(url).path) or "report.pdf"
    local_path = os.path.join(DOWNLOAD_DIR, filename)

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(local_path, "wb") as f:
        f.write(response.content)

    return local_path


def extract_date(page) -> str | None:
    """
    Some IPSTA PDFs reuse an old template with a stale, invisible date
    sitting at the same spot as the real one, at a smaller font size.
    We isolate the text run that contains the word 'Date' and prefer
    the larger font size, since the real date is rendered bigger.
    """
    candidates = [c for c in page.chars if c["top"] < page.height * 0.6]

    by_size = {}
    for c in candidates:
        by_size.setdefault(round(c["size"], 1), []).append(c)

    best_match, best_size = None, -1
    for size, chars in by_size.items():
        chars_sorted = sorted(chars, key=lambda c: (round(c["top"]), c["x0"]))
        line = "".join(c["text"] for c in chars_sorted)
        if "date" in line.lower():
            m = DATE_RE.search(line)
            if m and size > best_size:
                best_match, best_size = m, size

    if best_match:
        d, mth, y = best_match.groups()
        return f"{y}-{int(mth):02d}-{int(d):02d}"
    return None


def extract_spot_differential(text: str) -> str | None:
    m = re.search(r"Spot\s*:\s*([A-Za-z ]+)", text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def parse_pdf(local_path: str, source_url: str) -> dict:
    row = {f: None for f in FIELDS}
    row["source_url"] = source_url

    with pdfplumber.open(local_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
        row["date"] = extract_date(page)
        row["spot_differential"] = extract_spot_differential(text)

        tables = page.extract_tables()
        if not tables:
            return row

        for r in tables[0]:
            if not r or not r[0]:
                continue
            label = r[0].strip().upper()
            if label in KEY_MAP:
                prefix = KEY_MAP[label]
                for col, val in zip(["open", "high", "low", "close"], r[1:5]):
                    row[f"{prefix}_{col}"] = val
            elif "TRADE" in label:
                m = re.search(r"([\d.]+)", r[1] or "")
                if m:
                    row["trade_volume_tons"] = m.group(1)

    return row


def save_row_to_csv(row: dict, csv_path: str = CSV_PATH) -> None:
    """Appends a row to the CSV, writing the header only if the file is new."""
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def parse_and_save_pdf(url: str, csv_path: str = CSV_PATH) -> dict:
    """Downloads a PDF from `url`, extracts its data, and appends it to the CSV."""
    print(f"Downloading: {url}")
    local_path = download_pdf(url)

    print(f"Parsing: {local_path}")
    row = parse_pdf(local_path, source_url=url)

    save_row_to_csv(row, csv_path)
    print(f"Saved row for date {row['date']} -> {csv_path}")

    return row


def load_links_from_csv(csv_path: str = LINKS_CSV_PATH) -> list:
    """Reads (text, url) pairs exported by parser.py."""
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        return [(row["text"], row["url"]) for row in reader]


def process_links_from_csv(links_csv_path: str = LINKS_CSV_PATH, rates_csv_path: str = CSV_PATH) -> None:
    """Processes every PDF link previously exported to a CSV file."""
    links = load_links_from_csv(links_csv_path)
    print(f"Loaded {len(links)} link(s) from {links_csv_path}")
    for text, url in links:
        parse_and_save_pdf(url, csv_path=rates_csv_path)


if __name__ == "__main__":
    # run this file directly to process a previously exported link list
    process_links_from_csv()