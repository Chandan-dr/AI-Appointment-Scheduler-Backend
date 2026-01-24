from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
import io

from app.ocr import extract_text_from_image
from app.schemas import TextInput, TextExtractionResponse

from app.extractor import extract_entities
from app.schemas import (
    EntityExtractionRequest,
    EntityExtractionResponse
)

from app.normalizer import normalize_datetime
from app.schemas import (
    NormalizationRequest,
    NormalizationResponse
)

from app.guardrails import check_guardrails
from app.schemas import AppointmentRequest, AppointmentResponse

app = FastAPI(title="AI Appointment Scheduler")

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/extract-text/from-text", response_model=TextExtractionResponse)
async def extract_text_from_text(payload: TextInput):
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text input cannot be empty"
        )

    return {
        "raw_text": payload.text.strip(),
        "confidence": 0.90
    }

@app.post("/extract-text/from-image", response_model=TextExtractionResponse)
async def extract_text_from_image_api(image: UploadFile = File(...)):
    if image.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        raise HTTPException(
            status_code=415,
            detail="Only PNG and JPEG images are supported"
        )

    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        img.verify()
        img = Image.open(io.BytesIO(contents))  # reopen after verify
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )

    text, confidence = extract_text_from_image(img)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in image"
        )

    return {
        "raw_text": text,
        "confidence": confidence
    }
@app.post("/extract-entities", response_model=EntityExtractionResponse)
async def extract_entities_api(payload: EntityExtractionRequest):
    if not payload.raw_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Raw text cannot be empty"
        )

    entities, confidence = extract_entities(payload.raw_text)

    if not any(entities.values()):
        raise HTTPException(
            status_code=400,
            detail="No entities could be extracted"
        )

    return {
        "entities": entities,
        "entities_confidence": confidence
    }


@app.post("/normalize", response_model=NormalizationResponse)
async def normalize_api(payload: NormalizationRequest):
    normalized, confidence = normalize_datetime(
        payload.date_phrase,
        payload.time_phrase
    )

    if not normalized["date"]:
        raise HTTPException(
            status_code=400,
            detail="Unable to normalize date/time"
        )

    return {
        "normalized": normalized,
        "normalization_confidence": confidence
    }


@app.post("/appointment", 
          response_model=AppointmentResponse,
            response_model_exclude_none=True)

async def create_appointment(payload: AppointmentRequest):
    raw_text = payload.raw_text.strip()

    if not raw_text:
        raise HTTPException(
            status_code=400,
            detail="Raw text cannot be empty"
        )

    # Step 1: Entity Extraction
    entities, entity_confidence = extract_entities(raw_text)

    # Step 2: Normalization
    normalized, normalization_confidence = normalize_datetime(
        entities.get("date_phrase"),
        entities.get("time_phrase")
    )
    time_provided = bool(entities.get("time_phrase"))

    # Step 3: Guardrails
    guardrail_result = check_guardrails(
        department=entities.get("department"),
        normalized=normalized,
        entity_confidence=entity_confidence,
        normalization_confidence=normalization_confidence,
        time_provided=time_provided
)


    if guardrail_result["status"] != "ok":
        return guardrail_result

    # Step 4: Final Appointment Object
    appointment = {
        "department": entities["department"].capitalize(),
        "date": normalized["date"],
        "time": normalized["time"],
        "tz": normalized["tz"]
    }

    return {
        "appointment": appointment,
        "status": "ok"
    }
