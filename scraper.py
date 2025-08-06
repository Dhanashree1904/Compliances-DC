import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# URL of compliance updates page
URL = "https://www.nist.gov/cyberframework"  # Replace with actual site
CSV_FILE = "compliance_updates.csv"

def scrape_updates():
    # Fetch webpage
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract updates (Adjust selectors according to site HTML)
    updates = []
    for update in soup.select(".update-item"):  # Change selector
        title = update.select_one(".update-title").get_text(strip=True)
        link = update.select_one("a")["href"]
        date = update.select_one(".update-date").get_text(strip=True)

        updates.append({
            "date": date,
            "title": title,
            "link": link,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # Save to CSV (avoid duplicates)
    df_new = pd.DataFrame(updates)

    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df_all = pd.concat([df_old, df_new]).drop_duplicates(subset=["title"]).reset_index(drop=True)
    else:
        df_all = df_new

    df_all.to_csv(CSV_FILE, index=False)
    print(f"✅ Scraped {len(updates)} updates. Total saved: {len(df_all)}")

if __name__ == "__main__":
    scrape_updates()
