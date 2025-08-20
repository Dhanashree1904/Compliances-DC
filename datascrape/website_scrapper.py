import requests
from bs4 import BeautifulSoup
from classifier import classify_text

url = "https://studentprivacy.ed.gov/ferpa"

def scrape_website(url):
    try:
        print(f"[+] Scraping website: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        main = soup.find("div", class_="entry-content") or soup.find("main") or soup.find("body")
        text = main.get_text(strip=True, separator="\n") if main else soup.get_text(strip=True, separator="\n")

        return text

    except Exception as e:
        return f"[!] Error scraping website: {e}"

content = scrape_website(url)

# Classify extracted content
classified = classify_text(content)

# Write all categories into one single output file
with open("ferpa_output.txt", "w", encoding="utf-8") as f:
    f.write(f"🌐 Website Source: {url}\n\n")
    for category, sentences in classified.items():
        f.write(f"\n==== {category.upper()} ====\n\n")
        for line in sentences:
            f.write(f"- {line.strip()}\n")

print("[+] All classified website content saved to output.txt")
