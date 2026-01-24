from typing import Dict, Optional

def check_guardrails(
    department,
    normalized,
    entity_confidence,
    normalization_confidence,
    time_provided: bool
):
    if not department:
        return {
            "status": "needs_clarification",
            "message": "Department is missing or unclear"
        }

    if not normalized.get("date"):
        return {
            "status": "needs_clarification",
            "message": "Date could not be determined"
        }

    if not time_provided:
        return {
            "status": "needs_clarification",
            "message": "Time could not be determined"
        }

    if entity_confidence < 0.7 or normalization_confidence < 0.7:
        return {
            "status": "needs_clarification",
            "message": "Low confidence in extracted information"
        }

    return {"status": "ok"}
