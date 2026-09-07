"""
UPI-Shield Configuration
Thresholds, risk scoring weights, contextual adjustment parameters, and constants.
"""

from typing import Dict

# Risk Level Bands
RISK_LEVEL_LOW = "LOW"
RISK_LEVEL_MEDIUM = "MEDIUM"
RISK_LEVEL_HIGH = "HIGH"
RISK_LEVEL_CRITICAL = "CRITICAL"

# Score Thresholds (0-100)
# 0-30   -> LOW
# 31-60  -> MEDIUM
# 61-80  -> HIGH
# 81-100 -> CRITICAL
SCORE_THRESHOLDS: Dict[str, float] = {
    RISK_LEVEL_LOW: 30.0,
    RISK_LEVEL_MEDIUM: 60.0,
    RISK_LEVEL_HIGH: 80.0,
    RISK_LEVEL_CRITICAL: 100.0,
}

# Signal Weights (Sum to 1.0 / 100%)
# Configurable weights as specified in documentation TRD Section 4
DEFAULT_SIGNAL_WEIGHTS: Dict[str, float] = {
    "urgency": 0.20,             # 20%
    "threat": 0.20,              # 20%
    "authority": 0.15,           # 15%
    "payment_pressure": 0.20,    # 20%
    "credential_request": 0.15,  # 15%
    "reward_manipulation": 0.10  # 10%
}

# Multi-Signal Contextual Adjustment Parameters
CONTEXTUAL_BOOST_CONFIG: Dict[str, float] = {
    "min_triggered_signals": 2,    # Co-occurrence threshold
    "boost_per_additional_signal": 5.0,  # Points added per co-occurring trigger beyond the first
    "max_contextual_boost": 15.0   # Hard cap for contextual adjustment
}
