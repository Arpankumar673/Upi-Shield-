"""
Text Preprocessing Module for UPI-Shield.
Normalizes message text and extracts key entities (URLs, UPI VPAs, phone numbers, amounts).
"""

import re
from pydantic import BaseModel, Field
from typing import List, Optional

MAX_INPUT_LENGTH = 5000

# Regex Patterns for entity extraction
URL_REGEX = re.compile(
    r'(?:https?://|www\.)[^\s<>"]+|[a-zA-Z0-9-]+\.(?:com|in|org|net|xyz|top|info|site|app|online|co|club|live|tech|me)[^\s<>"]*',
    re.IGNORECASE
)

UPI_VPA_REGEX = re.compile(
    r'\b[a-zA-Z0-9.\-_]{2,256}@(paytm|ybl|okaxis|oksbi|okicici|upi|ibl|axl|barodampay|postbank|mahb|idfcbank|kotak|apl|centralbank|federal|indus|slice|airtel|gpay|phonepe)\b',
    re.IGNORECASE
)

PHONE_REGEX = re.compile(
    r'(?:\+91[\-\s]?)?[6-9]\d{9}|\b\d{5}[\-\s]?\d{5}\b',
    re.IGNORECASE
)

CURRENCY_REGEX = re.compile(
    r'(?:₹|rs\.?|inr)\s*\d+(?:,\d+)*(?:\.\d{1,2})?|\b\d+(?:,\d+)*\s*(?:rupees|rs|inr)\b',
    re.IGNORECASE
)


class ProcessedText(BaseModel):
    raw_text: str
    cleaned_text: str
    normalized_text: str
    char_count: int
    word_count: int
    extracted_urls: List[str] = Field(default_factory=list)
    extracted_upi_ids: List[str] = Field(default_factory=list)
    extracted_phones: List[str] = Field(default_factory=list)
    extracted_amounts: List[str] = Field(default_factory=list)
    has_urls: bool = False
    has_upi_ids: bool = False
    has_phones: bool = False
    has_amounts: bool = False
    is_truncated: bool = False


class TextProcessor:
    """Normalizes input text and extracts contextual entities."""

    def __init__(self, max_length: int = MAX_INPUT_LENGTH):
        self.max_length = max_length

    def process(self, text: Optional[str]) -> ProcessedText:
        if not text:
            return ProcessedText(
                raw_text="",
                cleaned_text="",
                normalized_text="",
                char_count=0,
                word_count=0,
            )

        raw = text
        is_truncated = False
        if len(raw) > self.max_length:
            raw = raw[:self.max_length]
            is_truncated = True

        # Whitespace normalization
        cleaned = " ".join(raw.split())
        normalized = cleaned.lower()
        words = cleaned.split()

        # Entity Extraction
        urls = list(set(URL_REGEX.findall(cleaned)))
        upi_ids = list(set(UPI_VPA_REGEX.finditer(cleaned)))
        extracted_vpas = [match.group(0) for match in upi_ids]
        phones = list(set(PHONE_REGEX.findall(cleaned)))
        amounts = list(set(CURRENCY_REGEX.findall(cleaned)))

        return ProcessedText(
            raw_text=text,
            cleaned_text=cleaned,
            normalized_text=normalized,
            char_count=len(cleaned),
            word_count=len(words),
            extracted_urls=urls,
            extracted_upi_ids=extracted_vpas,
            extracted_phones=phones,
            extracted_amounts=amounts,
            has_urls=len(urls) > 0,
            has_upi_ids=len(extracted_vpas) > 0,
            has_phones=len(phones) > 0,
            has_amounts=len(amounts) > 0,
            is_truncated=is_truncated,
        )
