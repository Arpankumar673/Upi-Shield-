"""
Risk Engine for UPI-Shield.
Calculates transparent aggregated risk score (0-100), applies contextual co-occurrence adjustments,
and maps scores to risk level bands (LOW, MEDIUM, HIGH, CRITICAL).
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from src.config import (
    DEFAULT_SIGNAL_WEIGHTS,
    SCORE_THRESHOLDS,
    CONTEXTUAL_BOOST_CONFIG,
    RISK_LEVEL_LOW,
    RISK_LEVEL_MEDIUM,
    RISK_LEVEL_HIGH,
    RISK_LEVEL_CRITICAL,
)
from src.detection.detector import DetectionResult


class RiskResult(BaseModel):
    score: float  # 0.0 to 100.0
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    signal_contributions: Dict[str, float] = Field(default_factory=dict)
    triggered_signals: List[str] = Field(default_factory=list)
    contextual_adjustment: float = 0.0
    explanation_summary: str = ""


class RiskEngine:
    """Aggregates signal detection results into a transparent, bounded risk score."""

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        thresholds: Optional[Dict[str, float]] = None,
        boost_config: Optional[Dict[str, float]] = None,
    ):
        self.weights = weights or DEFAULT_SIGNAL_WEIGHTS
        self.thresholds = thresholds or SCORE_THRESHOLDS
        self.boost_config = boost_config or CONTEXTUAL_BOOST_CONFIG

    def calculate_risk(self, detection_result: DetectionResult) -> RiskResult:
        if not detection_result or not detection_result.indicators:
            return self._empty_risk_result()

        signal_contributions: Dict[str, float] = {}
        base_score = 0.0
        triggered_signals: List[str] = []

        # 1. Calculate Weighted Contributions for Each Signal
        for key, weight in self.weights.items():
            indicator_confidence = detection_result.indicators.get(key, 0.0)
            contribution = round(indicator_confidence * weight * 100.0, 2)
            signal_contributions[key] = contribution
            base_score += contribution

        # Identify Triggered Signals (from signals list or indicators >= threshold)
        for signal in detection_result.signals:
            if signal.detected:
                triggered_signals.append(signal.name)

        # 2. Contextual Adjustment for Co-Occurring Signals
        contextual_adjustment = self._calculate_contextual_boost(triggered_signals, detection_result)

        # Direct credential request floor: Any active credential disclosure request must reach at least MEDIUM risk (36.0/100)
        if "credential_request" in triggered_signals:
            min_credential_score = 36.0
            if (base_score + contextual_adjustment) < min_credential_score:
                contextual_adjustment = round(min_credential_score - base_score, 1)

        # 3. Calculate Final Clamped Score (0.0 to 100.0)
        unclamped_score = base_score + contextual_adjustment
        final_score = min(100.0, max(0.0, round(unclamped_score, 1)))

        # 4. Map Score to Risk Level Band
        risk_level = self._map_score_to_level(final_score)

        # 5. Build Explanation Summary
        summary = self._build_scoring_summary(
            final_score, risk_level, triggered_signals, base_score, contextual_adjustment
        )

        return RiskResult(
            score=final_score,
            risk_level=risk_level,
            signal_contributions=signal_contributions,
            triggered_signals=triggered_signals,
            contextual_adjustment=round(contextual_adjustment, 1),
            explanation_summary=summary,
        )

    def _calculate_contextual_boost(
        self, triggered_signals: List[str], detection_result: DetectionResult
    ) -> float:
        min_triggered = int(self.boost_config.get("min_triggered_signals", 2))
        boost_per_signal = float(self.boost_config.get("boost_per_additional_signal", 5.0))
        max_boost = float(self.boost_config.get("max_contextual_boost", 15.0))

        triggered_count = len(triggered_signals)

        # Standalone direct credential request boost
        # Ensures direct OTP/PIN disclosure requests reach MEDIUM risk (15.0 base + 21.0 boost = 36.0 pts)
        if triggered_count == 1 and "credential_request" in triggered_signals:
            has_urls = detection_result.metadata.get("has_urls", False)
            return 26.0 if has_urls else 21.0

        boost = 0.0

        # Multi-signal co-occurrence boost
        if triggered_count >= min_triggered:
            boost += (triggered_count - 1) * boost_per_signal

        # Suspicious URL link context boost when combined with deception triggers
        has_urls = detection_result.metadata.get("has_urls", False)
        if has_urls and triggered_count >= 1:
            boost += 5.0

        return min(max_boost, boost)

    def _map_score_to_level(self, score: float) -> str:
        """Explicit boundary mapping for score thresholds."""
        low_limit = self.thresholds.get(RISK_LEVEL_LOW, 30.0)
        med_limit = self.thresholds.get(RISK_LEVEL_MEDIUM, 60.0)
        high_limit = self.thresholds.get(RISK_LEVEL_HIGH, 80.0)

        if score <= low_limit:
            return RISK_LEVEL_LOW
        elif score <= med_limit:
            return RISK_LEVEL_MEDIUM
        elif score <= high_limit:
            return RISK_LEVEL_HIGH
        else:
            return RISK_LEVEL_CRITICAL

    def _build_scoring_summary(
        self,
        score: float,
        level: str,
        triggered_signals: List[str],
        base_score: float,
        boost: float,
    ) -> str:
        if not triggered_signals:
            return f"Low Threat Score of {score}/100. No active deception signals detected."

        sig_names = ", ".join([s.replace("_", " ").title() for s in triggered_signals])
        boost_str = f" including +{boost:.1f} pts co-occurrence adjustment" if boost > 0 else ""
        return (
            f"Evaluated Risk Level: {level} ({score}/100). "
            f"Triggered Signals: {sig_names}{boost_str}."
        )

    def _empty_risk_result(self) -> RiskResult:
        empty_contribs = {k: 0.0 for k in self.weights.keys()}
        return RiskResult(
            score=0.0,
            risk_level=RISK_LEVEL_LOW,
            signal_contributions=empty_contribs,
            triggered_signals=[],
            contextual_adjustment=0.0,
            explanation_summary="No message content provided.",
        )
