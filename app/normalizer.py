import pytz
from typing import Dict, Tuple, Optional
from datetime import datetime
from dateparser.search import search_dates

TIMEZONE = "Asia/Kolkata"

def normalize_datetime(
    date_phrase: Optional[str],
    time_phrase: Optional[str]
) -> Tuple[Dict[str, Optional[str]], float]:

    if not date_phrase:
        return {
            "date": None,
            "time": None,
            "tz": TIMEZONE
        }, 0.0

    tz = pytz.timezone(TIMEZONE)

    settings = {
        "TIMEZONE": TIMEZONE,
        "RETURN_AS_TIMEZONE_AWARE": True,
        "PREFER_DATES_FROM": "future",
        "RELATIVE_BASE": datetime.now(tz)
    }

    combined_text = date_phrase
    if time_phrase:
        combined_text += f" {time_phrase}"

    results = search_dates(
        combined_text,
        settings=settings,
        languages=["en"]
    )

    if not results:
        return {
            "date": None,
            "time": None,
            "tz": TIMEZONE
        }, 0.0

    parsed = results[0][1].astimezone(tz)

    normalized = {
        "date": parsed.strftime("%Y-%m-%d"),
        "time": parsed.strftime("%H:%M"),
        "tz": TIMEZONE
    }

    confidence = 0.9 if time_phrase else 0.75

    return normalized, confidence
