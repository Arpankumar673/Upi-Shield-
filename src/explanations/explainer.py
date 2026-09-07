"""
Explanation Engine for UPI-Shield.
Generates clear, explainable breakdowns of detected threat indicators, evidence matches, and signal contributions.
"""

from pydantic import BaseModel, Field
from typing import List, Dict
from src.detection.detector import DetectionResult
from src.scoring.risk_engine import RiskResult


class ExplanationResult(BaseModel):
    summary: str
    reasons: List[str] = Field(default_factory=list)
    evidence_breakdown: List[str] = Field(default_factory=list)
    signal_contributions_formatted: List[str] = Field(default_factory=list)


class Explainer:
    """Explainer engine to output human-readable risk details, evidence, and contributions."""

    def explain(self, detection_result: DetectionResult, risk_result: RiskResult) -> ExplanationResult:
        reasons: List[str] = []
        evidence_breakdown: List[str] = []
        contributions_formatted: List[str] = []

        for signal in detection_result.signals:
            if signal.detected:
                contrib_pts = risk_result.signal_contributions.get(signal.name, 0.0)
                reason_entry = f"• **{signal.display_name}**: Potential scam trigger detected (+{contrib_pts:.1f} pts)"
                reasons.append(reason_entry)

                if signal.evidence:
                    ev_str = ", ".join([f"'{e}'" for e in signal.evidence])
                    evidence_breakdown.append(f"**{signal.display_name}**: Context matches {ev_str}")

                contributions_formatted.append(f"{signal.display_name}: {contrib_pts:.1f}%")

        if risk_result.contextual_adjustment > 0:
            reasons.append(
                f"• **Co-occurring Risk Boost**: Multiple high-risk signals detected simultaneously (+{risk_result.contextual_adjustment:.1f} pts adjustment)"
            )

        if not reasons:
            summary = (
                f"Message evaluated with a Low Risk score of {risk_result.score}/100. "
                "No deceptive triggers, authority impersonation, or coercion markers were flagged."
            )
            reasons = ["No suspicious manipulation markers or coercive triggers were identified."]
        else:
            summary = (
                f"Evaluated as **{risk_result.risk_level} Risk** ({risk_result.score}/100) "
                "due to potential digital payment scam and social-engineering indicators."
            )

        return ExplanationResult(
            summary=summary,
            reasons=reasons,
            evidence_breakdown=evidence_breakdown,
            signal_contributions_formatted=contributions_formatted,
        )
