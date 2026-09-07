"""
FastAPI Request & Response Schemas for UPI-Shield REST API.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., description="SMS, WhatsApp, or payment note message text to analyze.")


class UPIAnalysisRequest(BaseModel):
    uri: str = Field(..., description="upi://pay payment intent URI string.")


class SignalDetail(BaseModel):
    name: str
    display_name: str
    score: float
    detected: bool
    evidence: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    score: float
    risk_level: str
    triggered_signals: List[str]
    indicators: Dict[str, float]
    signals: List[SignalDetail]
    explanation_summary: str
    reasons: List[str]
    evidence: List[str]
    recommendation_en: str
    recommendation_hi: str
    action_bullets_en: List[str]
    action_bullets_hi: List[str]
    extracted_context: Dict


class UPIAnalysisResponse(BaseModel):
    is_valid: bool
    payee_vpa: Optional[str] = None
    payee_name: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    transaction_note: Optional[str] = None
    raw_uri: str
    errors: List[str] = Field(default_factory=list)
    risk_analysis: Optional[AnalysisResponse] = None


class ImageAnalysisResponse(BaseModel):
    ocr_success: bool
    extracted_text: str = ""
    ocr_error: Optional[str] = None
    risk_analysis: Optional[AnalysisResponse] = None
    process_time_ms: Optional[float] = None
