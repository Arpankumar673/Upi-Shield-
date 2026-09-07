"""
Unit & Integration Tests for UPI Intent Parser (Phase 4).
Tests URI validation, URL decoding, parameter extraction, and context integration.
"""

from src.upi.upi_parser import UPIParser, UPIIntentData
from src.preprocessing.text_processor import TextProcessor
from src.detection.detector import SignalDetector
from src.scoring.risk_engine import RiskEngine


def test_valid_basic_upi_uri():
    parser = UPIParser()
    res = parser.parse_uri("upi://pay?pa=test@upi")
    assert res.is_valid is True
    assert res.payee_vpa == "test@upi"
    assert res.payee_name is None
    assert res.amount is None


def test_upi_uri_with_all_parameters():
    parser = UPIParser()
    uri = "upi://pay?pa=merchant@paytm&pn=Electricity%20Board&am=2999.00&cu=INR&tn=Bill%20disconnection%20payment"
    res = parser.parse_uri(uri)

    assert res.is_valid is True
    assert res.payee_vpa == "merchant@paytm"
    assert res.payee_name == "Electricity Board"
    assert res.amount == "2999.00"
    assert res.currency == "INR"
    assert res.transaction_note == "Bill disconnection payment"


def test_url_encoded_parameters():
    parser = UPIParser()
    res = parser.parse_uri("upi://pay?pa=user%40okaxis&pn=John%20Doe&tn=Refund%20verification%20fee")
    assert res.is_valid is True
    assert res.payee_vpa == "user@okaxis"
    assert res.payee_name == "John Doe"
    assert res.transaction_note == "Refund verification fee"


def test_missing_optional_parameters():
    parser = UPIParser()
    res = parser.parse_uri("upi://pay?pa=shop@ybl")
    assert res.is_valid is True
    assert res.payee_vpa == "shop@ybl"
    assert res.payee_name is None
    assert res.amount is None
    assert res.transaction_note is None


def test_invalid_scheme():
    parser = UPIParser()
    res = parser.parse_uri("https://pay?pa=test@upi")
    assert res.is_valid is False
    assert any("Invalid UPI scheme" in err for err in res.errors)


def test_malformed_uri():
    parser = UPIParser()
    res = parser.parse_uri("upi://pay?invalid_no_vpa")
    assert res.is_valid is False
    assert any("Missing required payee VPA" in err for err in res.errors)


def test_invalid_amount_format():
    parser = UPIParser()
    res = parser.parse_uri("upi://pay?pa=user@upi&am=not_a_number")
    assert res.is_valid is False
    assert any("Invalid numeric amount" in err for err in res.errors)


def test_normal_upi_uri_not_automatically_scam():
    parser = UPIParser()
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    uri = "upi://pay?pa=friend@ybl&pn=Alex&am=500.00&cu=INR&tn=Dinner%20share"
    intent_data = parser.parse_uri(uri)
    assert intent_data.is_valid is True

    context_text = intent_data.get_message_context()
    processed = processor.process(context_text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score <= 30.0
    assert risk.risk_level == "LOW"


def test_suspicious_verification_upi_uri():
    parser = UPIParser()
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    uri = "upi://pay?pa=kycupdate@upi&pn=KYC%20Verification&am=1999&cu=INR&tn=Urgent%20KYC%20verification"
    intent_data = parser.parse_uri(uri)
    assert intent_data.is_valid is True

    context_text = intent_data.get_message_context()
    processed = processor.process(context_text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score >= 31.0
    assert risk.risk_level in ("MEDIUM", "HIGH")
    assert any(sig in risk.triggered_signals for sig in ("urgency", "credential_request"))


def test_refund_verification_upi_uri():
    parser = UPIParser()
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    uri = "upi://pay?pa=refundverify@upi&pn=Refund%20Verification&am=4999&cu=INR"
    intent_data = parser.parse_uri(uri)
    assert intent_data.is_valid is True

    context_text = intent_data.get_message_context()
    processed = processor.process(context_text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score >= 31.0
    assert risk.risk_level in ("MEDIUM", "HIGH")
    assert any(sig in risk.triggered_signals for sig in ("credential_request", "reward_manipulation"))


def test_account_block_prevention_upi_uri():
    parser = UPIParser()
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    uri = "upi://pay?pa=support@upi&pn=Account%20Block%20Prevention&am=999&cu=INR&tn=Pay%20to%20unblock%20account"
    intent_data = parser.parse_uri(uri)
    assert intent_data.is_valid is True

    context_text = intent_data.get_message_context()
    processed = processor.process(context_text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score >= 31.0
    assert risk.risk_level in ("MEDIUM", "HIGH")
    assert any(sig in risk.triggered_signals for sig in ("threat", "payment_pressure"))

