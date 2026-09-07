"""
Preloaded sample messages for UI demonstration & testing.
Covers all Part H demo scenarios specified in hackathon requirements.
"""

SAMPLE_MESSAGES = {
    "Safe Transfer (Low Risk)": (
        "I'll send you ₹500 tomorrow for dinner."
    ),
    "Electricity Bill Disconnection Threat (High/Critical)": (
        "URGENT! Your electricity connection will be disconnected today. Pay ₹2,999 immediately to avoid disconnection."
    ),
    "Expired Cashback Reward (Medium/High Risk)": (
        "Congratulations! You won ₹1,500 cashback. Click the link http://reward-claim.xyz to claim your reward."
    ),
    "Authority Impersonation & Transfer Demand (High Risk)": (
        "Your bank account requires urgent verification. Please contact customer support immediately."
    ),
    "OTP Credential Request (High Risk)": (
        "Your UPI account will be blocked. Share the OTP to complete verification."
    )
}
