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


import time

class OCRResult(BaseModel):
    success: bool = False
    extracted_text: str = ""
    confidence: float = 0.0
    error: Optional[str] = None
    char_count: int = 0
    process_time_ms: float = 0.0
    preprocess_time_ms: float = 0.0
    ocr_time_ms: float = 0.0


class OCREngine:
    """In-memory Screenshot OCR Engine with fallback error handling."""

    def __init__(self, max_size_bytes: int = MAX_IMAGE_SIZE_BYTES):
        self.max_size_bytes = max_size_bytes

    def extract_text_from_bytes(self, image_bytes: bytes, mime_type: Optional[str] = None) -> OCRResult:
        t_start = time.time()
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

        t_prep_start = time.time()
        try:
            # Single-pass image load & validation
            image = Image.open(io.BytesIO(image_bytes))
            
            # Fast proportion-preserving downscale if image exceeds max dimension (1600px)
            max_dim = 1600
            w, h = image.size
            if max(w, h) > max_dim:
                scale = max_dim / float(max(w, h))
                new_size = (int(w * scale), int(h * scale))
                resample_filter = getattr(Image, "Resampling", Image).BILINEAR
                image = image.resize(new_size, resample_filter)
            
            # Convert to grayscale to speed up Tesseract text segmentation
            image = image.convert("L")
            t_prep_end = time.time()

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

        t_ocr_start = time.time()
        try:
            # Fast single-pass OCR in-memory with tessedit_do_invert=0 to skip redundant inversion search
            fast_config = "--psm 6 -c tessedit_do_invert=0"
            extracted_text = pytesseract.image_to_string(image, config=fast_config)
            cleaned = extracted_text.strip()

            # Single fallback to PSM 3 with tessedit_do_invert=0 if PSM 6 produced empty output
            if not cleaned:
                fallback_config = "--psm 3 -c tessedit_do_invert=0"
                extracted_text = pytesseract.image_to_string(image, config=fallback_config)
                cleaned = extracted_text.strip()

            t_ocr_end = time.time()
            total_ms = (t_ocr_end - t_start) * 1000.0
            prep_ms = (t_prep_end - t_prep_start) * 1000.0
            ocr_ms = (t_ocr_end - t_ocr_start) * 1000.0

            if not cleaned:
                return OCRResult(
                    success=False,
                    extracted_text="",
                    error="No readable text could be extracted from the screenshot image.",
                    process_time_ms=round(total_ms, 2),
                    preprocess_time_ms=round(prep_ms, 2),
                    ocr_time_ms=round(ocr_ms, 2)
                )

            return OCRResult(
                success=True,
                extracted_text=cleaned,
                confidence=0.85,
                char_count=len(cleaned),
                process_time_ms=round(total_ms, 2),
                preprocess_time_ms=round(prep_ms, 2),
                ocr_time_ms=round(ocr_ms, 2)
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
