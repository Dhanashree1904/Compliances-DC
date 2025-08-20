import requests
from bs4 import BeautifulSoup
import csv
import os
import json
from datetime import datetime
from urllib.parse import urljoin

# File paths
CSV_FILE = "compliance_updates.csv"
SEEN_FILE = "seen_updates.json"

# Load previously seen updates
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r") as f:
        seen_updates = json.load(f)
else:
    seen_updates = {}

# Compliance websites
SITES = {
    "Indian Compliance": "https://www.meity.gov.in/whats-new",
    "GDPR": "https://gdpr-info.eu/news/",
    "FERPA": "https://studentprivacy.ed.gov/whats-new",
    "NIST": "https://www.nist.gov/news-events/news"
}

def fetch_meity(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    item = soup.select_one(".view-content .views-row")
    if item:
        title = item.get_text(strip=True)
        link = urljoin(url, item.find("a")["href"]) if item.find("a") else url
        return title, link
    return None, None

def fetch_gdpr(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    item = soup.select_one("article h2 a")
    if item:
        return item.get_text(strip=True), item["href"]
    return None, None

def fetch_ferpa(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    item = soup.select_one(".view-content .views-row a")
    if item:
        title = item.get_text(strip=True)
        link = urljoin(url, item["href"])
        return title, link
    return None, None

def fetch_nist(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    item = soup.select_one("article h3 a")
    if item:
        return item.get_text(strip=True), urljoin(url, item["href"])
    return None, None

SCRAPERS = {
    "Indian Compliance": fetch_meity,
    "GDPR": fetch_gdpr,
    "FERPA": fetch_ferpa,
    "NIST": fetch_nist
}

# Ensure CSV exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Source", "Title", "Link", "Status"])

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    for source, url in SITES.items():
        title, link = SCRAPERS[source](url)

        if not title:  # if scraper failed
            writer.writerow([timestamp, source, "No updates found", "NA", "No new update"])
            continue

        # Get last seen update for this source
        last_seen = seen_updates.get(source)

        if last_seen != title:
            # New update found
            writer.writerow([timestamp, source, title, link, "NEW UPDATE FOUND"])
            seen_updates[source] = title
        else:
            # No new update
            writer.writerow([timestamp, source, "No updates found", "NA", "No new update"])

# Save updated seen updates
with open(SEEN_FILE, "w") as f:
    json.dump(seen_updates, f, indent=2)

print("Compliance check complete. Logged to CSV.")

