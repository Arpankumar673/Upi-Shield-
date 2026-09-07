"""
Screenshot OCR Engine for UPI-Shield.
Extracts message text from uploaded screenshots in-memory using PIL and Tesseract OCR with graceful fallbacks.
"""

import io
from pydantic import BaseModel, Field
from typing import Optional
from PIL import Image

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"]


class OCRResult(BaseModel):
    success: bool = False
    extracted_text: str = ""
    confidence: float = 0.0
    error: Optional[str] = None
    char_count: int = 0


class OCREngine:
    """In-memory Screenshot OCR Engine with fallback error handling."""

    def __init__(self, max_size_bytes: int = MAX_IMAGE_SIZE_BYTES):
        self.max_size_bytes = max_size_bytes

    def extract_text_from_bytes(self, image_bytes: bytes, mime_type: Optional[str] = None) -> OCRResult:
        if not image_bytes:
            return OCRResult(success=False, error="No image file provided.")

        if len(image_bytes) > self.max_size_bytes:
            return OCRResult(
                success=False,
                error=f"Image file size exceeds maximum limit of {self.max_size_bytes // (1024 * 1024)}MB."
            )

        if mime_type and mime_type.lower() not in ALLOWED_MIME_TYPES:
            return OCRResult(
                success=False,
                error=f"Unsupported image format '{mime_type}'. Supported formats: PNG, JPG, JPEG, WEBP."
            )

        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()  # Check image integrity
            
            # Reopen after verify (Pillow verify requirement)
            image = Image.open(io.BytesIO(image_bytes))
        except Exception:
            return OCRResult(
                success=False,
                error="Failed to decode image file. File may be corrupted or invalid."
            )

        if not PYTESSERACT_AVAILABLE:
            return OCRResult(
                success=False,
                error="pytesseract package is not installed in the environment."
            )

        try:
            # Perform OCR in-memory
            extracted_text = pytesseract.image_to_string(image)
            cleaned = extracted_text.strip()

            if not cleaned:
                return OCRResult(
                    success=False,
                    extracted_text="",
                    error="No readable text could be extracted from the screenshot image."
                )

            return OCRResult(
                success=True,
                extracted_text=cleaned,
                confidence=0.85,
                char_count=len(cleaned)
            )

        except pytesseract.TesseractNotFoundError:
            return OCRResult(
                success=False,
                error="Tesseract-OCR engine binary is not installed or not found on system PATH."
            )
        except Exception as e:
            return OCRResult(
                success=False,
                error=f"OCR extraction encountered an error: {str(e)}"
            )
