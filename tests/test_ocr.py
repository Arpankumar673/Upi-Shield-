"""
Unit & Integration Tests for Screenshot OCR Engine (Phase 4).
Tests in-memory file decoding, format validation, size bounds, and non-crashing fallbacks.
"""

import io
from PIL import Image
from src.ocr.ocr_engine import OCREngine


def test_valid_image_format_in_memory():
    # Create a simple synthetic in-memory image
    img = Image.new("RGB", (200, 50), color=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    engine = OCREngine()
    res = engine.extract_text_from_bytes(image_bytes, mime_type="image/png")

    # Should safely process without throwing exceptions
    assert isinstance(res.success, bool)
    assert res.error is None or isinstance(res.error, str)


def test_unsupported_image_type():
    engine = OCREngine()
    res = engine.extract_text_from_bytes(b"dummy image content", mime_type="application/pdf")
    assert res.success is False
    assert "Unsupported image format" in (res.error or "")


def test_corrupt_image_bytes():
    engine = OCREngine()
    res = engine.extract_text_from_bytes(b"corrupt non-image binary data", mime_type="image/png")
    assert res.success is False
    assert "Failed to decode image file" in (res.error or "")


def test_empty_image_bytes():
    engine = OCREngine()
    res = engine.extract_text_from_bytes(b"")
    assert res.success is False
    assert "No image file provided" in (res.error or "")


def test_oversized_image_bounds():
    engine = OCREngine(max_size_bytes=100)  # Set tiny 100-byte max limit
    res = engine.extract_text_from_bytes(b"x" * 200, mime_type="image/png")
    assert res.success is False
    assert "exceeds maximum limit" in (res.error or "")
