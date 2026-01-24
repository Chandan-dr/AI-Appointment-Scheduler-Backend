import re
from typing import Dict, Tuple

DEPARTMENTS = [
    "dentist",
    "pediatrician",
    "general practitioner",
    "cardiologist",
    "doctor",
    "neurologist",
    "orthopedic",
    "psychiatrist",
    "dermatologist",
    "gynecologist",
    "ophthalmologist",
    "urologist"
]

def extract_entities(text: str) -> Tuple[Dict[str, str], float]:
    text_lower = text.lower()

    # --- Department ---
    department = None
    for dept in DEPARTMENTS:
        if dept in text_lower:
            department = dept
            break

    # --- Date Phrase ---
    date_match = re.search(
        r"(today|tomorrow|next\s+\w+|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        text_lower
    )
    date_phrase = date_match.group(0) if date_match else None

    # --- Time Phrase ---
    time_match = re.search(
        r"(\d{1,2}(:\d{2})?\s?(am|pm))",
        text_lower
    )
    time_phrase = time_match.group(0) if time_match else None

    entities = {
        "date_phrase": date_phrase,
        "time_phrase": time_phrase,
        "department": department
    }

    # Simple confidence heuristic
    extracted_count = sum(1 for v in entities.values() if v)
    confidence = round(0.6 + (0.1 * extracted_count), 2)

    return entities, confidence
