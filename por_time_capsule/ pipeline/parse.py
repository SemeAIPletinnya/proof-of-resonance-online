import re

def clean_text(text: str) -> str:
    """Basic clean-up."""
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_comments(raw):
    """Extract structured comments from raw HN-like text."""
    if isinstance(raw, dict) and "comments" in raw:
        return raw["comments"]

    # fallback — split by heuristics
    return [c.strip() for c in raw.split(".") if len(c) > 20]

