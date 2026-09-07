"""
Deception Signal Detection Engine for UPI-Shield.
Analyzes normalized text and metadata for 6 core scam and coercion indicators.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from src.preprocessing.text_processor import ProcessedText
from src.detection.rules import ALL_RULES, CategoryRule


class SignalScore(BaseModel):
    name: str
    display_name: str
    score: float = 0.0  # 0.0 to 1.0 confidence score
    detected: bool = False
    evidence: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)


class DetectionResult(BaseModel):
    indicators: Dict[str, float]
    signals: List[SignalScore]
    overall_detection_strength: float = 0.0
    evidence: List[str] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)


class SignalDetector:
    """Multi-category deception signal detection engine."""

    def __init__(self, detection_threshold: float = 0.3):
        self.detection_threshold = detection_threshold
        self.rules = ALL_RULES

    def analyze(self, processed_text: ProcessedText) -> DetectionResult:
        if not processed_text or not processed_text.cleaned_text:
            return self._empty_result()

        text = processed_text.normalized_text
        signals: List[SignalScore] = []
        indicators: Dict[str, float] = {}
        all_evidence: List[str] = []

        # Analyze each deception category
        for rule in self.rules:
            signal_score = self._evaluate_category(rule, text, processed_text)
            signals.append(signal_score)
            indicators[signal_score.name] = signal_score.score
            if signal_score.detected:
                all_evidence.extend(signal_score.evidence)

        # Contextual URL / Payment link boost if combined with deception signals
        if processed_text.has_urls:
            for signal in signals:
                if signal.name in ("reward_manipulation", "credential_request", "payment_pressure") and signal.score > 0:
                    signal.score = min(1.0, round(signal.score + 0.30, 2))
                    signal.detected = signal.score >= self.detection_threshold
                    indicators[signal.name] = signal.score
                    if "Suspicious URL detected alongside manipulation trigger" not in signal.reasons:
                        signal.reasons.append("Suspicious URL detected alongside manipulation trigger")

        overall_strength = max(indicators.values()) if indicators else 0.0

        metadata = {
            "char_count": processed_text.char_count,
            "word_count": processed_text.word_count,
            "has_urls": processed_text.has_urls,
            "extracted_urls": processed_text.extracted_urls,
            "has_upi_ids": processed_text.has_upi_ids,
            "extracted_upi_ids": processed_text.extracted_upi_ids,
            "has_phones": processed_text.has_phones,
            "extracted_phones": processed_text.extracted_phones,
            "has_amounts": processed_text.has_amounts,
            "extracted_amounts": processed_text.extracted_amounts,
            "detected_signal_count": sum(1 for s in signals if s.detected)
        }

        return DetectionResult(
            indicators=indicators,
            signals=signals,
            overall_detection_strength=round(overall_strength, 2),
            evidence=list(set(all_evidence)),
            metadata=metadata
        )

    def _evaluate_category(self, rule: CategoryRule, norm_text: str, processed: ProcessedText) -> SignalScore:
        primary_score = 0.0
        secondary_score = 0.0
        evidence: List[str] = []
        reasons: List[str] = []

        # Evaluate Primary Patterns
        primary_matches = 0
        for pattern, weight in rule.primary_patterns:
            matches = pattern.findall(norm_text)
            if matches:
                primary_matches += 1
                primary_score += weight
                for m in matches:
                    snippet = m if isinstance(m, str) else m[0]
                    if snippet not in evidence:
                        evidence.append(snippet)

        # Evaluate Secondary Patterns
        for pattern, weight in rule.secondary_patterns:
            matches = pattern.findall(norm_text)
            if matches:
                secondary_score += weight
                for m in matches:
                    snippet = m if isinstance(m, str) else m[0]
                    if snippet not in evidence:
                        evidence.append(snippet)

        # Contextual filtering for false-positives
        if rule.name == "credential_request":
            # Check for informational / warning negation phrases (e.g., "never share your OTP", "do not share OTP")
            import re
            informational_patterns = [
                r'\bnever\s+(?:share|tell|provide|disclose|give)\b',
                r'\bdo\s+not\s+(?:share|tell|provide|disclose|give)\b',
                r'\bdon\'t\s+(?:share|tell|provide|disclose|give)\b',
                r'\bmat\s+(?:share|batao|dalo|bhejo)\b',
                r'\bbank\s+(?:never|will\s+never)\s+(?:ask|request|call)\b',
                r'\bno\s+one\s+from\s+.*?\s+will\s+ask\b',
                r'\bcaution:?\s+never\s+share\b',
                r'\bwarning:?\s+do\s+not\s+share\b',
            ]
            if any(re.search(pat, norm_text, re.IGNORECASE) for pat in informational_patterns):
                return SignalScore(
                    name=rule.name,
                    display_name=rule.display_name,
                    score=0.0,
                    detected=False,
                    evidence=[],
                    reasons=["Informational security advice advising user not to share credentials"]
                )

            # Require share/tell/enter verb or remote access tool to avoid flagging casual mentions of "PIN"
            has_credential_verb = any(
                v in norm_text for v in [
                    "share", "tell", "enter", "send", "provide", "batao", "dalo", "bhejo",
                    "anydesk", "teamviewer", "quicksupport"
                ]
            )
            if not has_credential_verb and primary_matches == 1 and "pin" in norm_text:
                primary_score *= 0.2  # Downweight isolated word "pin"

        if rule.name == "payment_pressure":
            # Friendly mention "send you money" vs payment pressure demand
            if "i'll send" in norm_text or "i will send" in norm_text or "thanks for" in norm_text:
                primary_score *= 0.2

        # Combine scores
        total_score = primary_score + (secondary_score * 0.5)
        if primary_matches > 1:
            total_score += rule.co_occurrence_boost

        final_score = min(1.0, max(0.0, round(total_score, 2)))
        detected = final_score >= self.detection_threshold

        if detected:
            reasons.append(f"{rule.display_name} detected (Confidence: {int(final_score * 100)}%)")

        return SignalScore(
            name=rule.name,
            display_name=rule.display_name,
            score=final_score,
            detected=detected,
            evidence=evidence,
            reasons=reasons
        )

    def _apply_url_context_boost(self, signals: List[SignalScore], indicators: Dict[str, float], processed: ProcessedText):
        """Slightly boosts confidence if suspicious links accompany reward or credential claims."""
        for signal in signals:
            if signal.name in ("reward_manipulation", "credential_request", "payment_pressure") and signal.detected:
                signal.score = min(1.0, round(signal.score + 0.15, 2))
                indicators[signal.name] = signal.score
                signal.reasons.append("Suspicious URL detected alongside manipulation trigger")

    def _empty_result(self) -> DetectionResult:
        empty_indicators = {rule.name: 0.0 for rule in self.rules}
        empty_signals = [
            SignalScore(
                name=rule.name,
                display_name=rule.display_name,
                score=0.0,
                detected=False,
                evidence=[],
                reasons=[]
            ) for rule in self.rules
        ]
        return DetectionResult(
            indicators=empty_indicators,
            signals=empty_signals,
            overall_detection_strength=0.0,
            evidence=[],
            metadata={"empty": True}
        )
