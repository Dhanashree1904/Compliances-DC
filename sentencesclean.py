import os
import json
import nltk
from fuzzywuzzy import fuzz

# Download NLTK sentence tokenizer
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Folder containing your text files
folder_path = "scrape_outputs"

# Keywords to detect important sentences
keywords = [
    "must", "shall", "liable", "penalty", "mandatory",
    "section", "rule", "compliance", "regulation", "fine"
]

important_data = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        sentences = sent_tokenize(text)

        # Step 1: Filter by keywords
        filtered_sentences = [
            s.strip() for s in sentences
            if any(k in s.lower() for k in keywords)
        ]

        # Step 2: Remove exact duplicates
        filtered_sentences = list(set(filtered_sentences))

        # Step 3: Remove similar sentences using fuzzy matching
        unique_sentences = []
        for sentence in filtered_sentences:
            if not any(fuzz.ratio(sentence, us) > 85 for us in unique_sentences):  # 85% similarity
                unique_sentences.append(sentence)

        if unique_sentences:
            important_data.append({
                "source": filename,
                "important_sentences": unique_sentences
            })

# Save to JSON
output_path = "important_sentences_clean.json"
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(important_data, json_file, indent=2, ensure_ascii=False)

print(f"[✅] Clean important sentences saved to {output_path}")
