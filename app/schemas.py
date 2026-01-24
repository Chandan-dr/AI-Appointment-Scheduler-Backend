from pydantic import BaseModel
from typing import Optional, Dict

class TextInput(BaseModel):
    text: Optional[str] = None

class TextExtractionResponse(BaseModel):
    raw_text: str
    confidence: float

class EntityExtractionRequest(BaseModel):
    raw_text: str

class EntityExtractionResponse(BaseModel):
    entities: Dict[str, Optional[str]]
    entities_confidence: float

class NormalizationRequest(BaseModel):
    date_phrase: Optional[str]
    time_phrase: Optional[str]

class NormalizationResponse(BaseModel):
    normalized: Dict[str, Optional[str]]
    normalization_confidence: float

class AppointmentRequest(BaseModel):
    raw_text: str

class AppointmentResponse(BaseModel):
    appointment: Optional[Dict[str, str]] = None
    status: str
    message: Optional[str] = None

