import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text


def classify_email(text):
    """
    Rule-based classifier (can be replaced by ML / LLM later)
    """
    if any(word in text for word in ["interview", "shortlisted", "selection", "hr round"]):
        return "INTERVIEW"

    elif any(word in text for word in ["job", "hiring", "vacancy", "opening", "career"]):
        return "ONLINE JOB"

    else:
        return "SOCIAL ADS"


def get_priority(category):
    if category == "INTERVIEW":
        return "High"
    elif category == "ONLINE JOB":
        return "Medium"
    else:
        return "Low"
