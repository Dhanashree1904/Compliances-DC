# classifier.py

import re

def classify_sentence(sentence):
    s = sentence.lower()

    if any(kw in s for kw in ["must", "shall", "should", "required to", "obligated to", "prohibited from"]):
        return "Compliance Clause"
    elif any(kw in s for kw in ["means", "refers to", "includes"]) and len(s.split()) < 30:
        return "Definition"
    elif "user" in s or "employee" in s:
        return "User Responsibility"
    elif "organization" in s or "data controller" in s or "data processor" in s:
        return "Organizational Responsibility"
    elif any(kw in s for kw in ["consent", "right", "withdraw", "data principal", "access"]):
        return "Consent and Rights"
    elif any(kw in s for kw in ["penalty", "liable", "fine", "imprisonment", "punishable"]):
        return "Penalties"
    else:
        return "Other"

def classify_text(raw_text):
    results = {
        "Compliance Clause": [],
        "Definition": [],
        "User Responsibility": [],
        "Organizational Responsibility": [],
        "Consent and Rights": [],
        "Penalties": [],
        "Other": []
    }

    sentences = re.split(r'(?<=[.!?])\s+', raw_text)

    for sentence in sentences:
        category = classify_sentence(sentence)
        results[category].append(sentence.strip())

    return results
