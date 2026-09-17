

import requests
import urllib3
from src.config import HEADERS, TARGET_URL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_page_html() -> str | None:
  print(f"Fetching page from: {TARGET_URL}")
  try:
    response = requests.get(TARGET_URL, headers=HEADERS)
    response.raise_for_status()
    
    print("Successfully fetched HTML.")
    return response.text
  except Exception as e:
    print(f"Error fetching page: {e}")
    return None


if __name__ == "__main__":
  html = fetch_page_html()
  print(html)
  if html:
    print(f"Success! HTML length: {len(html)}")