import requests
import fitz  # PyMuPDF
import os
from classifier import classify_text

pdf_source = "Companies.pdf"

def scrape_pdf(source):
    try:
        if source.startswith("http"):
            print(f"[+] Downloading PDF from: {source}")
            pdf_bytes = requests.get(source).content
            pdf_path = "temp_download.pdf"
            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)
        else:
            pdf_path = source

        print(f"[+] Extracting text from: {pdf_path}")
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if source.startswith("http") and os.path.exists(pdf_path):
            os.remove(pdf_path)

        return text

    except Exception as e:
        return f"[!] Error scraping PDF: {e}"

content = scrape_pdf(pdf_source)

# Classify extracted content
classified = classify_text(content)

# Write all categories into one single output file
with open("companies_output.txt", "w", encoding="utf-8") as f:
    f.write(f"📄 PDF Source: {pdf_source}\n\n")
    for category, sentences in classified.items():
        f.write(f"\n==== {category.upper()} ====\n\n")
        for line in sentences:
            f.write(f"- {line.strip()}\n")

print("[+] All classified PDF content saved to output.txt")
