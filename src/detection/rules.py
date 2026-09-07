"""
Deception Rules & Pattern Matching Definitions.
Contains contextual concepts, patterns, and scoring heuristics for the 6 core scam categories.
"""

import re
from typing import Dict, List, Tuple


class CategoryRule:
    def __init__(
        self,
        name: str,
        display_name: str,
        primary_patterns: List[Tuple[str, float]],
        secondary_patterns: List[Tuple[str, float]],
        co_occurrence_boost: float = 0.2
    ):
        self.name = name
        self.display_name = display_name
        self.primary_patterns = [
            (re.compile(pattern, re.IGNORECASE), weight) for pattern, weight in primary_patterns
        ]
        self.secondary_patterns = [
            (re.compile(pattern, re.IGNORECASE), weight) for pattern, weight in secondary_patterns
        ]
        self.co_occurrence_boost = co_occurrence_boost


# 1. URGENCY / TIME PRESSURE
URGENCY_RULE = CategoryRule(
    name="urgency",
    display_name="Urgency / Time Pressure",
    primary_patterns=[
        (r'\b(?:urgent|urgently|immediate|immediately|act now|right now|at once|last chance|final notice)\b', 0.6),
        (r'\b(?:within|in)\s+\d+\s+(?:mins?|minutes?|hours?|hrs?)\b', 0.6),
        (r'\b(?:click|open|visit)\s+.*?\b(?:to\s+)?(?:claim|receive|verify|collect|update)\b', 0.6),
        (r'\b(?:today itself|expires? (?:today|soon|in \d+)|before 11:59|turant|jaldi|abhi|aaj hi|aaj raat)\b', 0.5),
    ],
    secondary_patterns=[
        (r'\b(?:2 hours?|24 hours?|10 mins?|15 mins?|today|aaj)\b', 0.2),
        (r'\b(?:do not delay|without delay|limited time)\b', 0.3),
    ]
)

# 2. THREAT / FEAR / CONSEQUENCES
THREAT_RULE = CategoryRule(
    name="threat",
    display_name="Threat / Fear / Consequences",
    primary_patterns=[
        (r'\b(?:disconnect(?:ed|ion)?|power cut|light cut|bijli (?:kat|cut)|connection (?:cut|block))\b', 0.8),
        (r'\b(?:electricity|power|gas|water|sim)\s+connection\b', 0.5),
        (r'\b(?:account|upi|vpa|sim|card|service|access|profile)\s+(?:will\s+be\s+)?(?:blocked|frozen|suspended|deactivated|closed)\b', 0.8),
        (r'\b(?:account (?:frozen|block|blocked|suspended|terminated)|sim (?:block|blocked|deactivat))\b', 0.7),
        (r'\b(?:legal action|police (?:fir|case)|court notice|prosecution|arrest|jail|police station)\b', 0.8),
        (r'\b(?:kaat diya|block ho|band ho|freeze ho)\s*(?:jayega|gaya|dengi)\b', 0.7),
    ],
    secondary_patterns=[
        (r'\b(?:penalty|fine|permanent(?:ly)?|consequences|suspend)\b', 0.4),
        (r'\b(?:avoid|prevent|stop)\s+(?:disconnection|blocking|suspension|action)\b', 0.4),
    ]
)

# 3. AUTHORITY IMPERSONATION
AUTHORITY_RULE = CategoryRule(
    name="authority",
    display_name="Authority Impersonation",
    primary_patterns=[
        (r'\b(?:electricity (?:department|board|office)|power (?:corporation|board))\b', 0.8),
        (r'\b(?:calling from|calling on behalf of|bank security|rbi|state bank|sbi|hdfc|icici)\b', 0.7),
        (r'\b(?:bank (?:security|fraud|helpdesk|manager|officer|department)|kyc officer)\b', 0.7),
        (r'\b(?:customer support|support team|helpdesk team|service officer)\b', 0.5),
        (r'\b(?:cyber (?:cell|crime|police)|police officer|telecom department|income tax)\b', 0.7),
        (r'\b(?:notice from|official notice|department notice|bank se bol|office se bol)\b', 0.7),
    ],
    secondary_patterns=[
        (r'\b(?:official|verification team|security desk|head office|authority|gov|govt)\b', 0.4),
        (r'\b(?:manager|officer|representative|agent)\b', 0.3),
    ]
)

# 4. PAYMENT PRESSURE / MANIPULATION
PAYMENT_RULE = CategoryRule(
    name="payment_pressure",
    display_name="Payment Pressure",
    primary_patterns=[
        (r'\b(?:pay|transfer|send|deposit)\s+₹?\d+[\d,]*\b', 0.7),
        (r'\b(?:pay|transfer|send|deposit)\s+(?:immediately|now|rs\.?|₹|\d+)\b', 0.7),
        (r'\b(?:pay|transfer|bhejo|deposit)\s+₹?\d+\s+(?:immediately|now|to avoid|turant)\b', 0.8),
        (r'\b(?:scan|pay through|transfer to)\s+(?:upi|qr|vpa|account)\b', 0.6),
        (r'\b(?:paise bhejo|turant pay karo|payment karo|bill pay karo)\b', 0.7),
    ],
    secondary_patterns=[
        (r'\b(?:outstanding|due|unpaid|bill amount|pending bill)\b', 0.4),
        (r'\b(?:fee|charge|deposit|recharge)\b', 0.3),
    ]
)

# 5. CREDENTIAL / SECURITY-ACTION REQUEST
CREDENTIAL_RULE = CategoryRule(
    name="credential_request",
    display_name="Credential Request",
    primary_patterns=[
        (r'\b(?:upi pin|otp|cvv|password|security pin|card pin)\b', 0.8),
        (r'\b(?:share|tell|enter|send|provide)\s+.*?\b(?:otp|pin|cvv|password)\b', 0.9),
        (r'\b(?:otp|pin)\s+(?:batao|share karo|dalo|enter karo)\b', 0.9),
        (r'\b(?:anydesk|teamviewer|quicksupport|screen share)\b', 0.9),
    ],
    secondary_patterns=[
        (r'\b(?:verify|verification|authenticate)\s+(?:account|identity|details|security)\b', 0.4),
        (r'\b(?:click link|open link)\s+to\s+(?:verify|update|complete)\b', 0.4),
    ]
)

# 6. REWARD / REFUND / CASHBACK MANIPULATION
REWARD_RULE = CategoryRule(
    name="reward_manipulation",
    display_name="Reward / Cashback / Refund Bait",
    primary_patterns=[
        (r'\b(?:won|claim|credited|approved|pending)\s+(?:₹?\d+[\d,]*\s+)?(?:cashback|reward|lottery|refund|prize)\b', 0.7),
        (r'\b(?:cashback|reward|refund|scratch card)\s+(?:of|worth)?\s*₹?\d+|\b₹?\d+[\d,]*\s+(?:cashback|reward|refund)\b', 0.6),
        (r'\b(?:cashback|reward|refund)\s+(?:mila|claim karo|expires|pending)\b', 0.6),
        (r'\b(?:click|link)\s+to\s+(?:claim|receive|get|collect)\b', 0.6),
    ],
    secondary_patterns=[
        (r'\b(?:congratulations|congrats|lucky winner|selected)\b', 0.3),
        (r'\b(?:free|gift|bonus|reimbursement)\b', 0.2),
    ]
)

ALL_RULES = [
    URGENCY_RULE,
    THREAT_RULE,
    AUTHORITY_RULE,
    PAYMENT_RULE,
    CREDENTIAL_RULE,
    REWARD_RULE,
]
