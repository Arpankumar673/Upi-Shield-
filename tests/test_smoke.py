"""
Modular Smoke Tests for Phase 1.
Verifies module imports, initialization, data flow, and risk level mapping.
"""

from src.config import SCORE_THRESHOLDS, RISK_LEVEL_LOW, RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL
from src.preprocessing import TextProcessor
from src.detection import SignalDetector
from src.scoring import RiskEngine
from src.explanations import Explainer
from src.guidance import GuidanceEngine
from data.sample_messages import SAMPLE_MESSAGES


def test_text_processor_smoke():
    processor = TextProcessor()
    res = processor.process("  Test SMS message   ")
    assert res.cleaned_text == "Test SMS message"
    assert res.word_count == 3
    assert res.char_count == 16


def test_end_to_end_pipeline_smoke():
    processor = TextProcessor()
    detector = SignalDetector()
    risk_engine = RiskEngine()
    explainer = Explainer()
    guidance_engine = GuidanceEngine()

    text = SAMPLE_MESSAGES["Safe Transfer (Low Risk)"]
    processed = processor.process(text)
    detection = detector.analyze(processed)
    risk = risk_engine.calculate_risk(detection)
    explanation = explainer.explain(detection, risk)
    guidance = guidance_engine.generate_guidance(risk.risk_level)

    assert risk.score >= 0.0 and risk.score <= 100.0
    assert risk.risk_level == RISK_LEVEL_LOW
    assert len(explanation.reasons) > 0
    assert "English" not in guidance.recommendation_en  # valid text
    assert len(guidance.recommendation_hi) > 0


def test_risk_level_mapping_boundaries():
    risk_engine = RiskEngine()
    assert risk_engine._map_score_to_level(0.0) == RISK_LEVEL_LOW
    assert risk_engine._map_score_to_level(30.0) == RISK_LEVEL_LOW
    assert risk_engine._map_score_to_level(31.0) == RISK_LEVEL_MEDIUM
    assert risk_engine._map_score_to_level(60.0) == RISK_LEVEL_MEDIUM
    assert risk_engine._map_score_to_level(61.0) == RISK_LEVEL_HIGH
    assert risk_engine._map_score_to_level(80.0) == RISK_LEVEL_HIGH
    assert risk_engine._map_score_to_level(85.0) == RISK_LEVEL_CRITICAL
