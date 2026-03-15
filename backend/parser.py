"""
Rule-based parser: extracts structured fields from messy free-text purchase requests.
No AI/API keys required — uses regex and keyword lists only.
"""

import re


# --- Keyword lists ---

PRIORITY_URGENT = ["asap", "urgent", "urgently", "today", "immediately", "right now", "emergency"]
PRIORITY_LOW = ["whenever", "low prio", "low priority", "no rush", "not urgent", "eventually", "someday"]

CATEGORIES = {
    "electronics": [
        "laptop", "charger", "headphones", "headset", "mouse", "keyboard", "monitor",
        "screen", "cable", "usb", "hdmi", "webcam", "microphone", "speaker", "tablet",
        "phone", "smartphone", "battery", "adapter", "hub", "dock", "ssd", "hard drive",
        "ram", "memory", "router", "wifi",
    ],
    "office": [
        "paper", "printer paper", "stapler", "staples", "pen", "pens", "pencil", "notebook",
        "binder", "folder", "tape", "scissors", "ruler", "whiteboard", "marker", "post-it",
        "sticky notes", "envelopes", "toner", "ink cartridge", "desk",
    ],
    "appliances": [
        "coffee machine", "coffee maker", "kettle", "microwave", "fridge", "refrigerator",
        "dishwasher", "toaster", "blender", "fan", "heater", "air purifier", "vacuum",
        "lamp", "desk lamp",
    ],
    "furniture": [
        "chair", "desk", "table", "shelf", "shelves", "cabinet", "drawer", "couch",
        "sofa", "bookshelf", "standing desk", "monitor arm", "ergonomic",
    ],
    "cleaning": [
        "soap", "sanitizer", "hand sanitizer", "cleaning spray", "mop", "broom",
        "trash bag", "garbage bag", "sponge", "tissue", "paper towel",
    ],
}

# Regex: matches numbers followed by an optional currency word
BUDGET_PATTERN = re.compile(
    r'\b(\d+(?:[.,]\d+)?)\s*(?:chf|bucks?|fr\.?|francs?|euros?|€|\$|dollars?|gbp|£)?\b',
    re.IGNORECASE,
)

# Tighter pattern: only match when a currency word is present
BUDGET_WITH_CURRENCY = re.compile(
    r'\b(\d+(?:[.,]\d+)?)\s*(?:chf|bucks?|fr\.?|francs?|euros?|€|\$|dollars?|gbp|£)\b'
    r'|(?:budget|max|maximum|up to|under|around|about|approx\.?|≈)\s*(?:chf|€|\$|£)?\s*(\d+(?:[.,]\d+)?)',
    re.IGNORECASE,
)


def extract_budget(text: str) -> float | None:
    """Return the first budget figure found in the text, or None."""
    match = BUDGET_WITH_CURRENCY.search(text)
    if match:
        value_str = match.group(1) or match.group(2)
        return float(value_str.replace(",", "."))
    return None


def extract_priority(text: str) -> str:
    """Return 'urgent', 'low', or 'normal'."""
    lower = text.lower()
    for kw in PRIORITY_URGENT:
        if kw in lower:
            return "urgent"
    for kw in PRIORITY_LOW:
        if kw in lower:
            return "low"
    return "normal"


def extract_category(text: str) -> str:
    """Return the best-matching category name, or 'other'."""
    lower = text.lower()
    # Count keyword hits per category and return the one with the most hits
    scores: dict[str, int] = {}
    for cat, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in lower)
        if score > 0:
            scores[cat] = score
    if scores:
        return max(scores, key=lambda c: scores[c])
    return "other"


def extract_item(text: str) -> str:
    """
    Best-effort item name extraction.
    Strategy: strip common filler phrases and return the first meaningful noun phrase.
    """
    lower = text.lower()

    # Remove filler lead-ins
    fillers = [
        r"^i need\b", r"^we need\b", r"^need\b", r"^looking for\b",
        r"^please (order|get|buy|purchase)\b", r"^order\b", r"^buy\b", r"^get\b",
        r"^urgent[ly]?\b", r"^asap\b",
    ]
    cleaned = lower.strip()
    for pattern in fillers:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()

    # Remove budget / priority phrases
    cleaned = re.sub(
        r',?\s*(?:max|maximum|budget|up to|under|around|about|approx\.?)\s*\d+\s*(?:chf|bucks?|fr\.?|francs?|euros?|€|\$|dollars?)?',
        "", cleaned, flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r',?\s*\d+\s*(?:chf|bucks?|fr\.?|francs?|euros?|€|\$|dollars?)',
        "", cleaned, flags=re.IGNORECASE,
    )
    for kw in PRIORITY_URGENT + PRIORITY_LOW:
        cleaned = re.sub(r',?\s*' + re.escape(kw), "", cleaned, flags=re.IGNORECASE)

    # Remove "for <purpose>" suffixes
    cleaned = re.sub(r'\s+for\s+\w+.*$', "", cleaned, flags=re.IGNORECASE)

    # Clean up punctuation and extra whitespace
    cleaned = re.sub(r'[,;.!?]+', " ", cleaned).strip()
    cleaned = re.sub(r'\s+', " ", cleaned).strip()

    # Capitalise nicely
    return cleaned.title() if cleaned else text.strip().title()


def parse_request(raw_text: str) -> dict:
    """
    Main entry point.  Takes raw free-text and returns a structured dict.

    Example
    -------
    >>> parse_request("need headphones for calls, max 80 bucks, asap")
    {
        "item": "Headphones",
        "category": "electronics",
        "budget_chf": 80.0,
        "priority": "urgent",
        "raw_input": "need headphones for calls, max 80 bucks, asap"
    }
    """
    return {
        "item": extract_item(raw_text),
        "category": extract_category(raw_text),
        "budget_chf": extract_budget(raw_text),
        "priority": extract_priority(raw_text),
        "raw_input": raw_text.strip(),
    }
