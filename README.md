AI-Powered Appointment Scheduler Assistant (Backend)

Overview

This project is a backend service that parses natural language or document-based appointment requests and converts them into structured scheduling data.

The system supports:

Typed text inputs
Image inputs (via OCR)
Entity extraction (date, time, department)
Date/time normalization (Asia/Kolkata)
Guardrails to handle ambiguity safely


Architecture

Client (Postman / curl / Swagger)
        |
        v
FastAPI Backend
        |
        ├── Text Input Handler
        ├── Image Input Handler (OCR)
        |
        v
Entity Extraction
        |
        v
Date & Time Normalization (Asia/Kolkata)
        |
        v
Guardrails (Ambiguity Detection)
        |
        v
Final Appointment JSON / Clarification Response


Tech Stack

Framework: FastAPI
OCR: Tesseract OCR + Pillow
NLP / Parsing: Regex + keyword extraction
Date Parsing: dateparser.search
Timezone: Asia/Kolkata
Language: Python 3.x


Project Structure

ai-appointment-scheduler/
│
├── app/
│   ├── main.py          # API endpoints
│   ├── ocr.py           # OCR and text cleaning
│   ├── extractor.py     # Entity extraction logic
│   ├── normalizer.py    # Date & time normalization
│   ├── guardrails.py    # Ambiguity detection
│   ├── schemas.py       # Pydantic models
│
├── requirements.txt
├── README.md
└── demo.mp4             # Screen recording


Setup Instructions

Clone the Repositry:
git clone <github-repo-url>
cd ai-appointment-scheduler

Create & Activate Virtual Environment (windows):
python -m venv venv
venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

Run the Server:
uvicorn app.main:app --reload

Open Swagger UI (local):
http://127.0.0.1:8000/docs


To provide a working backend demo as required, the service can be exposed using ngrok:
https://cognoscitive-exudative-tomiko.ngrok-free.dev

Swagger UI:
https://cognoscitive-exudative-tomiko.ngrok-free.dev/docs


API Endpoints (Postman)

1. Extract Text from Typed Input:

POST /extract-text/from-text

Request:
{
  "text": "Book dentist next Friday at 3pm"
}

Response:
{
  "raw_text": "Book dentist next Friday at 3pm",
  "confidence": 0.9
}

2. Extract Text from Image (OCR)

POST /extract-text/from-image

Form Data:

Key: image
Type: File
Value: image.jpg

Response
{
  "raw_text": "book dentist next friday at 3 pm",
  "confidence": 0.9
}

3. Extract Entities

POST /extract-entities

Request:
{
  "raw_text": "Book dentist next Friday at 3pm"
}

Response:
{
  "entities": {
    "date_phrase": "next friday",
    "time_phrase": "3pm",
    "department": "dentist"
  },
  "entities_confidence": 0.9
}

4. Normalize Date and Time

POST /normalize

Request:
{
  "date_phrase": "next Friday",
  "time_phrase": "3pm"
}

Response:
{
  "normalized": {
    "date": "2026-01-30",
    "time": "15:00",
    "tz": "Asia/Kolkata"
  },
  "normalization_confidence": 0.9
}

5. Final Appointment Endpoint (Pipeline + Guardrails)

POST /appointment

This endpoint performs:
Entity extraction
Date/time normalization
Guardrail validation

Valid Request
{
  "raw_text": "Book dentist next Friday at 3pm"
}

Response
{
  "appointment": {
    "department": "Dentist",
    "date": "2026-01-30",
    "time": "15:00",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
}


Missing Time (Guardrail Triggered)
{
  "raw_text": "Book dentist next Friday"
}

Response
{
  "status": "needs_clarification",
  "message": "Time could not be determined"
}


Missing Department
{
  "raw_text": "Book next Friday at 3pm"
}

Response
{
  "status": "needs_clarification",
  "message": "Department is missing or unclear"
}

The /extract-entities and /normalize endpoints are exposed primarily for modular testing and demonstration; the /appointment endpoint orchestrates the full pipeline with guardrails.


Guardrails & Safety

The system prevents incorrect scheduling by enforcing:

Mandatory department
Mandatory date
Mandatory user-provided time
Minimum confidence thresholds
If ambiguity exists, the pipeline exits early with a clarification request instead of guessing.