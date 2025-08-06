# summarizer.py

import re
from collections import defaultdict

input_file = "dpdp_output.txt"
output_file = "summary_output.txt"

# Simple logic to extract categories and bullet points
def parse_output_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sections = defaultdict(list)
    current_category = "Unknown"

    for line in lines:
        if line.strip().startswith("====") and "====" in line:
            current_category = line.strip("=\n ").title()
        elif line.strip().startswith("- "):
            sections[current_category].append(line.strip("- \n"))

    return sections

# Generate basic summaries (first 3 points + total count)
def summarize_sections(sections):
    summaries = {}
    for category, bullets in sections.items():
        if not bullets:
            continue
        preview = bullets[:3]  # Top 3
        count = len(bullets)
        summary = f"{count} key points found.\n"
        summary += "\n".join(f"- {line}" for line in preview)
        if count > 3:
            summary += f"\n- ...and {count - 3} more."
        summaries[category] = summary
    return summaries

# Write the summary output
def write_summary_file(summaries, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for category, summary in summaries.items():
            f.write(f"### {category}\n\n{summary}\n\n")

# Run it
sections = parse_output_file(input_file)
summaries = summarize_sections(sections)
write_summary_file(summaries, output_file)

print(f"[+] Summary written to {output_file}")
