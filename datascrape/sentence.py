import os
import json
import nltk

# Download sentence tokenizer
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Folder containing your scraped text files
folder_path = "datascrape/scrape_outputs"

# Define important keywords (you can expand this list)
keywords = [
    "must", "shall", "liable", "penalty", "mandatory",
    "section", "rule", "compliance", "regulation", "fine"
]

important_data = []

# Loop through all text files
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Split into sentences
        sentences = sent_tokenize(text)

        # Filter important sentences by keyword
        important_sentences = [
            sentence.strip() for sentence in sentences
            if any(keyword in sentence.lower() for keyword in keywords)
        ]

        # Store results only if important sentences found
        if important_sentences:
            important_data.append({
                "source": filename,
                "important_sentences": important_sentences
            })

# Save results to JSON
output_path = "important_sentences.json"
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(important_data, json_file, indent=2, ensure_ascii=False)

print(f"[✅] Extracted important sentences saved to {output_path}")
