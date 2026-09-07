"""
Unit & Integration Tests for Phase 3 Risk Scoring, Threshold Boundaries, Explanations & Bilingual Guidance.
"""

from src.config import (
    SCORE_THRESHOLDS,
    RISK_LEVEL_LOW,
    RISK_LEVEL_MEDIUM,
    RISK_LEVEL_HIGH,
    RISK_LEVEL_CRITICAL,
)
from src.preprocessing.text_processor import TextProcessor
from src.detection.detector import SignalDetector
from src.scoring.risk_engine import RiskEngine, RiskResult
from src.explanations.explainer import Explainer
from src.guidance.guidance_engine import GuidanceEngine
from data.sample_messages import SAMPLE_MESSAGES


def test_no_signals_low_risk():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    processed = processor.process("Hey Rohan, I'll send you ₹500 tomorrow.")
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score == 0.0
    assert risk.risk_level == RISK_LEVEL_LOW
    assert len(risk.triggered_signals) == 0


def test_urgency_threat_payment_critical_risk():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    text = (
        "URGENT! Notice from Electricity Department: Your power connection will be disconnected in 2 hours. "
        "Pay ₹2,999 immediately to avoid legal action."
    )
    processed = processor.process(text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score > 80.0
    assert risk.risk_level == RISK_LEVEL_CRITICAL
    assert "urgency" in risk.triggered_signals
    assert "threat" in risk.triggered_signals
    assert "payment_pressure" in risk.triggered_signals
    assert risk.contextual_adjustment > 0.0


def test_credential_request_payment_pressure():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    text = "Share your 6-digit UPI PIN and OTP immediately with customer support to pay ₹5,000."
    processed = processor.process(text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score >= 50.0
    assert "credential_request" in risk.triggered_signals
    assert "payment_pressure" in risk.triggered_signals


def test_reward_manipulation_with_url():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    text = "Congratulations! You won ₹1,500 cashback reward. Click http://claim-reward.xyz to claim before today."
    processed = processor.process(text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score >= 10.0
    assert "reward_manipulation" in risk.triggered_signals


def test_score_threshold_boundaries():
    risk_engine = RiskEngine()

    assert risk_engine._map_score_to_level(0) == RISK_LEVEL_LOW
    assert risk_engine._map_score_to_level(30) == RISK_LEVEL_LOW
    assert risk_engine._map_score_to_level(30.01) == RISK_LEVEL_MEDIUM
    assert risk_engine._map_score_to_level(31) == RISK_LEVEL_MEDIUM
    assert risk_engine._map_score_to_level(60) == RISK_LEVEL_MEDIUM
    assert risk_engine._map_score_to_level(60.01) == RISK_LEVEL_HIGH
    assert risk_engine._map_score_to_level(61) == RISK_LEVEL_HIGH
    assert risk_engine._map_score_to_level(80) == RISK_LEVEL_HIGH
    assert risk_engine._map_score_to_level(80.01) == RISK_LEVEL_CRITICAL
    assert risk_engine._map_score_to_level(81) == RISK_LEVEL_CRITICAL
    assert risk_engine._map_score_to_level(100) == RISK_LEVEL_CRITICAL


def test_score_never_below_zero_or_above_100():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    # Empty text
    processed_empty = processor.process("")
    detection_empty = detector.analyze(processed_empty)
    risk_empty = risk_engine.calculate_risk(detection_empty)
    assert risk_empty.score == 0.0

    # Hyper-extreme text with all scam triggers
    extreme_text = (
        "URGENT! Notice from Bank Security Department and Police Officer: "
        "Your account is frozen. Pay ₹10,000 immediately via UPI PIN and share OTP. "
        "Otherwise electricity will be disconnected within 10 minutes and legal action will be taken. "
        "Click http://claim-refund.xyz to claim cashback of ₹5,000 before 11:59!"
    )
    processed_ext = processor.process(extreme_text)
    detection_ext = detector.analyze(processed_ext)
    risk_ext = risk_engine.calculate_risk(detection_ext)

    assert risk_ext.score >= 80.0
    assert risk_ext.score <= 100.0
    assert risk_ext.risk_level == RISK_LEVEL_CRITICAL


def test_signal_contributions_dict():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    processed = processor.process(SAMPLE_MESSAGES["Electricity Bill Disconnection Threat (High/Critical)"])
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert isinstance(risk.signal_contributions, dict)
    assert "urgency" in risk.signal_contributions
    assert "threat" in risk.signal_contributions
    assert "authority" in risk.signal_contributions


def test_explainer_output():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    explainer = Explainer()

    processed = processor.process(SAMPLE_MESSAGES["Electricity Bill Disconnection Threat (High/Critical)"])
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)
    explanation = explainer.explain(detection, risk)

    assert len(explanation.reasons) > 0
    assert "CRITICAL" in explanation.summary or "HIGH" in explanation.summary or "Risk" in explanation.summary


def test_bilingual_guidance_all_levels():
    guidance_engine = GuidanceEngine()

    for level in [RISK_LEVEL_LOW, RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL]:
        res = guidance_engine.generate_guidance(level)
        assert res.risk_level == level
        assert len(res.recommendation_en) > 10
        assert len(res.recommendation_hi) > 10
        assert len(res.action_bullet_points_en) > 0
        assert len(res.action_bullet_points_hi) > 0


def test_safe_benign_message_remains_low_risk():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()

    text = SAMPLE_MESSAGES["Safe Transfer (Low Risk)"]
    processed = processor.process(text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)

    assert risk.score <= 30.0
    assert risk.risk_level == RISK_LEVEL_LOW


# --- PHASE 5.1 CALIBRATION REGRESSION TESTS ---

def test_part_f_1_otp_and_account_blocking():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Your UPI account will be blocked. Share the OTP to complete verification."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert "threat" in risk.triggered_signals
    assert "credential_request" in risk.triggered_signals
    assert risk.risk_level in (RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH)


def test_part_f_2_cashback_and_suspicious_link():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Congratulations! You won ₹1,500 cashback. Click the link http://reward-claim.xyz to claim your reward."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert "reward_manipulation" in risk.triggered_signals
    assert risk.risk_level in (RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH)


def test_part_f_3_refund_and_verification_pressure():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Refund pending. Complete verification using the link below."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert len(risk.triggered_signals) >= 1


def test_part_f_4_payment_and_electricity_threat():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "URGENT! Your electricity connection will be disconnected today. Pay ₹2,999 immediately."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert risk.risk_level in (RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL)


def test_part_f_5_authority_and_otp_request():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Notice from Bank Security Department: Send the OTP to verify your identity."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert "authority" in risk.triggered_signals
    assert "credential_request" in risk.triggered_signals


def test_part_f_6_benign_cashback_conversation():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "I received ₹50 cashback on my mobile recharge yesterday."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert risk.risk_level == RISK_LEVEL_LOW


def test_part_f_7_normal_upi_uri():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Transaction note: Dinner share. Payee VPA: merchant@ybl. Payment Amount requested: INR 200.00."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert risk.risk_level == RISK_LEVEL_LOW


def test_part_f_8_isolated_otp_pin_mention():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "I forgot my phone screen lock PIN."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))
    assert risk.risk_level == RISK_LEVEL_LOW


# --- URGENT CALIBRATION FIX TESTS (DIRECT OTP & CREDENTIAL DISCLOSURE) ---

def test_direct_otp_sharing_request_medium_risk():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Your account verification is pending. Share the 6-digit OTP you received to complete the verification process."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))

    assert "credential_request" in risk.triggered_signals
    assert risk.score >= 31.0
    assert risk.risk_level in (RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH)


def test_otp_informational_warning_low_risk():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text1 = "Never share your OTP with anyone."
    risk1 = risk_engine.calculate_risk(detector.analyze(processor.process(text1)))

    assert "credential_request" not in risk1.triggered_signals
    assert risk1.score <= 30.0
    assert risk1.risk_level == RISK_LEVEL_LOW

    text2 = "Do not share your OTP with bank officials."
    risk2 = risk_engine.calculate_risk(detector.analyze(processor.process(text2)))
    assert risk2.risk_level == RISK_LEVEL_LOW


def test_otp_plus_threat_medium_or_high_risk():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Your UPI account will be blocked within 2 hours. Share the OTP to verify."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))

    assert "threat" in risk.triggered_signals
    assert "credential_request" in risk.triggered_signals
    assert risk.risk_level in (RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH)


def test_otp_plus_refund_high_risk():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "URGENT: Your refund of ₹4,999 is pending verification. Share your OTP to receive the refund."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))

    assert "reward_manipulation" in risk.triggered_signals or "urgency" in risk.triggered_signals
    assert "credential_request" in risk.triggered_signals
    assert risk.risk_level in (RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH)


def test_otp_plus_account_blocking_medium_or_high():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    text = "Your UPI account will be blocked. Share the OTP to complete verification."
    risk = risk_engine.calculate_risk(detector.analyze(processor.process(text)))

    assert "threat" in risk.triggered_signals
    assert "credential_request" in risk.triggered_signals
    assert risk.risk_level in (RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH)


