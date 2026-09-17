# src/parser.py

import csv
import os
from bs4 import BeautifulSoup
from src.pdf_extractor import parse_and_save_pdf

LINKS_CSV_PATH = "data/pdf_links.csv"


def extract_links(html_content: str) -> list:
  """Extracts all links and text from the HTML page."""
  if not html_content:
    return []

  soup = BeautifulSoup(html_content, "html.parser")
  links = soup.find_all(
      "a",
      href=True,
      string=lambda t: t and "daily market report" in t.lower(),
  )

  parsed_links = []
  for link in links:
    text = link.get_text(strip=True)
    href = link["href"]
    parsed_links.append((text, href))

  return parsed_links


def export_links_to_csv(links: list, csv_path: str = LINKS_CSV_PATH) -> None:
  """Saves (text, url) link pairs to a CSV file for later/independent processing."""
  os.makedirs(os.path.dirname(csv_path), exist_ok=True)
  with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "url"])
    writer.writerows(links)
  print(f"Exported {len(links)} link(s) to {csv_path}")


if __name__ == "__main__":
  from src.scraper import fetch_page_html

  html = fetch_page_html()
  links = extract_links(html)
  print(f"\nFound {len(links)} Daily Market Report links on the page:\n" + "-" * 40)

  # Filter specifically for PDF links
  target_pdf_links = [
      (text, href)
      for text, href in links
      if "daily market report" in text.lower() and href.endswith(".pdf")
  ]

  for text, href in links:
    print(f"Text: '{text}' --> URL: {href}")

  # Export the filtered PDF links to a CSV file
  export_links_to_csv(target_pdf_links)

  print(f"\nProcessing {len(target_pdf_links)} target PDF(s) into CSV...")
  for text, url in target_pdf_links:
    parse_and_save_pdf(url)