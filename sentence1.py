import os
import json
import nltk

# Download NLTK sentence tokenizer once
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Folder containing your scraped .txt files
folder_path = "scrape_outputs"  # Change this to your folder

# Store extracted sentences grouped by file
output_data = []

# Loop through each file
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Split into sentences
        sentences = sent_tokenize(text)

        # Add to output
        output_data.append({
            "source": filename,
            "sentences": [s.strip() for s in sentences if len(s.strip()) > 10]  # avoid tiny fragments
        })

# Save as JSON
with open("all_sentences.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("[✅] All sentences saved to all_sentences.json")
