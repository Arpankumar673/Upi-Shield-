"""
Unit & Integration Tests for Phase 2 Preprocessing & Detection Engine.
Tests all 6 deception categories, entity extraction, multi-signal detection, Hinglish, edge cases, and isolated keywords.
"""

from src.preprocessing.text_processor import TextProcessor
from src.detection.detector import SignalDetector, DetectionResult


def test_safe_benign_message():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Hey Rohan, I'll send you ₹500 tomorrow for the dinner we had yesterday."
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert isinstance(res, DetectionResult)
    assert res.overall_detection_strength == 0.0
    assert not any(s.detected for s in res.signals)


def test_urgency_detection():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "URGENT! Action required within 2 hours or your request will expire today!"
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert res.indicators["urgency"] >= 0.5
    urgency_signal = next(s for s in res.signals if s.name == "urgency")
    assert urgency_signal.detected is True


def test_threat_detection():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Your electricity connection will be disconnected today due to non-payment. Legal action will be taken."
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert res.indicators["threat"] >= 0.5
    threat_signal = next(s for s in res.signals if s.name == "threat")
    assert threat_signal.detected is True


def test_authority_impersonation_detection():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Notice from Bank Security Department: Customer support officer verifying account security."
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert res.indicators["authority"] >= 0.4
    auth_signal = next(s for s in res.signals if s.name == "authority")
    assert auth_signal.detected is True


def test_payment_pressure_detection():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Pay ₹2,999 immediately via UPI QR to avoid penalty fees."
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert res.indicators["payment_pressure"] >= 0.5
    pay_signal = next(s for s in res.signals if s.name == "payment_pressure")
    assert pay_signal.detected is True


def test_credential_request_detection():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Share your 6-digit UPI PIN and OTP immediately with the caller to complete verification."
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert res.indicators["credential_request"] >= 0.7
    cred_signal = next(s for s in res.signals if s.name == "credential_request")
    assert cred_signal.detected is True


def test_reward_refund_manipulation_detection():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Congratulations! You won ₹1,500 cashback reward. Click http://claim-reward.xyz to claim before today."
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert res.indicators["reward_manipulation"] >= 0.5
    rew_signal = next(s for s in res.signals if s.name == "reward_manipulation")
    assert rew_signal.detected is True


def test_multiple_signals_simultaneous():
    processor = TextProcessor()
    detector = SignalDetector()
    text = (
        "URGENT! Notice from Electricity Department: Your power connection will be disconnected in 2 hours. "
        "Pay ₹2,999 immediately to avoid legal action."
    )
    processed = processor.process(text)
    res = detector.analyze(processed)

    detected_categories = [s.name for s in res.signals if s.detected]
    assert "urgency" in detected_categories
    assert "threat" in detected_categories
    assert "authority" in detected_categories
    assert "payment_pressure" in detected_categories
    assert len(detected_categories) >= 3


def test_hinglish_hindi_scam_detection():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Bijli bill update nahi hua hai, aaj raat connection kat jayega. Abhi turant paise bhejo."
    processed = processor.process(text)
    res = detector.analyze(processed)

    detected_categories = [s.name for s in res.signals if s.detected]
    assert "threat" in detected_categories or "urgency" in detected_categories or "payment_pressure" in detected_categories


def test_empty_input():
    processor = TextProcessor()
    detector = SignalDetector()
    processed = processor.process("")
    res = detector.analyze(processed)

    assert res.overall_detection_strength == 0.0
    assert not any(s.detected for s in res.signals)
    assert res.metadata.get("empty") is True


def test_long_input():
    processor = TextProcessor()
    detector = SignalDetector()
    text = "Normal message content. " * 500  # > 10,000 chars
    processed = processor.process(text)
    res = detector.analyze(processed)

    assert processed.is_truncated is True
    assert isinstance(res, DetectionResult)


def test_url_extraction_and_signal():
    processor = TextProcessor()
    text = "Verify your account details at http://security-update-bank.com/login"
    processed = processor.process(text)

    assert processed.has_urls is True
    assert "http://security-update-bank.com/login" in processed.extracted_urls


def test_upi_vpa_extraction():
    processor = TextProcessor()
    text = "Transfer the fee to merchant.verify@paytm or receiver@ybl to unfreeze your account."
    processed = processor.process(text)

    assert processed.has_upi_ids is True
    assert "merchant.verify@paytm" in processed.extracted_upi_ids or "receiver@ybl" in processed.extracted_upi_ids


def test_isolated_keyword_false_positive():
    processor = TextProcessor()
    detector = SignalDetector()
    # Casual use of the word "pin" or "payment" without scam context
    text1 = "I forgot the screen lock PIN of my Android phone."
    processed1 = processor.process(text1)
    res1 = detector.analyze(processed1)
    cred_signal = next(s for s in res1.signals if s.name == "credential_request")
    assert cred_signal.detected is False

    text2 = "Thank you for making a payment for your grocery order."
    processed2 = processor.process(text2)
    res2 = detector.analyze(processed2)
    pay_signal = next(s for s in res2.signals if s.name == "payment_pressure")
    assert pay_signal.detected is False
